#include "artery/networking/GeoNetIndication.h"
#include "artery/networking/GeoNetRequest.h"
#include "artery/nic/RadioDriverProperties.h"
#include "artery/lte/Mode4RadioDriver.h"
#include "veins/base/utils/FindModule.h"
#include "veins/modules/messages/WaveShortMessage_m.h"

#include "common/LteControlInfo.h"
#include "stack/phy/packet/cbr_m.h"

using namespace omnetpp;

namespace artery
{

Register_Class(Mode4RadioDriver)

namespace {

long convert(const vanetza::MacAddress& mac)
{
    long addr = 0;
    for (unsigned i = 0; i < mac.octets.size(); ++i) {
        addr <<= 8;
        addr |= mac.octets[i];
    }
    return addr;
}

vanetza::MacAddress convert(long addr)
{
    vanetza::MacAddress mac;
    for (unsigned i = mac.octets.size(); i > 0; --i) {
        mac.octets[i - 1] = addr & 0xff;
        addr >>= 8;
    }
    return mac;
}

int user_priority(vanetza::AccessCategory ac)
{
    using AC = vanetza::AccessCategory;
    int up = 0;
    switch (ac) {
        case AC::BK:
            up = 1;
            break;
        case AC::BE:
            up = 0;
            break;
        case AC::VI:
            up = 5;
            break;
        case AC::VO:
            up = 7;
            break;
    }
    return up;
}

const simsignal_t channelBusySignal = cComponent::registerSignal("sigChannelBusy");

} // namespace

void Mode4RadioDriver::initialize()
{
    addStartUpDelay_ = par("addStartUpDelay");
    if (addStartUpDelay_) {
        cMessage *startUpMessage = new cMessage("StartUpMsg");
        double delay = 0.001 * intuniform(0, 1000, 0);
        scheduleAt((simTime() + delay).trunc(SIMTIME_MS), startUpMessage);
        startUpComplete_ = false;
    } else {
        startUpComplete_ = true;
    }

    RadioDriverBase::initialize();
    mHost = FindModule<>::findHost(this);
    mHost->subscribe(channelBusySignal, this);

    mLowerLayerOut = gate("lowerLayerOut");
    mLowerLayerIn = gate("lowerLayerIn");

    auto properties = new RadioDriverProperties();
    properties->LinkLayerAddress = vanetza::create_mac_address(mHost->getIndex());
    // CCH used to ensure DCC configures correctly.
    properties->ServingChannel = channel::CCH;
    indicateProperties(properties);

    binder_ = getBinder();

    cModule *ue = getParentModule();
    nodeId_ = binder_->registerNode(ue, UE, 0);
    binder_->setMacNodeId(convert(properties->LinkLayerAddress), nodeId_);
}

void Mode4RadioDriver::finish()
{
    binder_->unregisterNode(nodeId_);
}

void Mode4RadioDriver::handleMessage(cMessage* msg){
    if (msg->isName("CBR")) {
        Cbr* cbrPkt = check_and_cast<Cbr*>(msg);
        double channel_load = cbrPkt->getCbr();
        delete cbrPkt;
        emit(RadioDriverBase::ChannelLoadSignal, channel_load);
    } else if (RadioDriverBase::isDataRequest(msg)) {
        handleDataRequest(msg);
    } else if (msg->getArrivalGate() == mLowerLayerIn) {
        handleDataIndication(msg);
    } else if (strcmp(msg->getName(), "StartUpMsg") == 0) {
        startUpComplete_ = true;
    } else {
        throw cRuntimeError("unexpected message");
    }
}

void Mode4RadioDriver::handleDataIndication(cMessage* packet)
{
    auto* lteControlInfo = check_and_cast<FlowControlInfoNonIp*>(packet->removeControlInfo());
    auto* indication = new GeoNetIndication();
    indication->source = convert(lteControlInfo->getSrcAddr());
    indication->destination = convert(lteControlInfo->getDstAddr());
    packet->setControlInfo(indication);
    delete lteControlInfo;

    indicateData(packet);
}

void Mode4RadioDriver::handleDataRequest(cMessage* packet)
{
    if (startUpComplete_) {
        auto request = check_and_cast<GeoNetRequest *>(packet->removeControlInfo());
        auto lteControlInfo = new FlowControlInfoNonIp();

        lteControlInfo->setSrcAddr(convert(request->source_addr));
        lteControlInfo->setDstAddr(convert(request->destination_addr));
        lteControlInfo->setPriority(user_priority(request->access_category));

        std::chrono::milliseconds lifetime_milli = std::chrono::duration_cast<std::chrono::milliseconds>(
            request->message_lifetime);

        lteControlInfo->setDuration(lifetime_milli.count());
        lteControlInfo->setCreationTime(packet->getCreationTime());

        if (request->destination_addr == vanetza::cBroadcastMacAddress) {
            lteControlInfo->setDirection(D2D_MULTI);
        }

        packet->setControlInfo(lteControlInfo);


        delete request;
        send(packet, mLowerLayerOut);
    } else {
        delete packet;
    }
}

void Mode4RadioDriver::receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t signal, bool busy, omnetpp::cObject*)
{
    ASSERT(signal == channelBusySignal);
    if (busy) {
        mChannelLoadMeasurements.busy();
    } else {
        mChannelLoadMeasurements.idle();
    }
}

} // namespace artery

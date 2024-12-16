#ifndef Mode4RADIODRIVER_H_ZJ0SI5XC
#define Mode4RADIODRIVER_H_ZJ0SI5XC

#include "artery/nic/ChannelLoadMeasurements.h"
#include "artery/nic/RadioDriverBase.h"

#include "common/LteCommon.h"
#include "corenetwork/binder/LteBinder.h"

#include <omnetpp/clistener.h>
#include <omnetpp/csimplemodule.h>

namespace artery
{

class Mode4RadioDriver : public RadioDriverBase, public omnetpp::cListener
{
	public:
		void initialize() override;
		void handleMessage(omnetpp::cMessage*) override;
		void finish() override;

	protected:
		void handleDataIndication(omnetpp::cMessage*);
		void handleDataRequest(omnetpp::cMessage*) override;
		void receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t, bool, omnetpp::cObject*) override;

	private:
		omnetpp::cModule* mHost = nullptr;
		omnetpp::cGate* mLowerLayerOut = nullptr;
		omnetpp::cGate* mLowerLayerIn = nullptr;
		ChannelLoadMeasurements mChannelLoadMeasurements;

		LteBinder* binder_;
		MacNodeId nodeId_;

		bool startUpComplete_;
		bool trafficPattern3GPP_;
		int largePacketCountDown_;
		bool addStartUpDelay_;
};

} // namespace artery

#endif /* Mode4RADIODRIVER_H_ZJ0SI5XC */


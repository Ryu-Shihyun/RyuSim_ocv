#include "artery/envmod/service/CollectivePerceptionMockMessage.h"
#include <omnetpp.h>

namespace artery
{

Register_Class(CollectivePerceptionMockMessage)

CollectivePerceptionMockMessage::CollectivePerceptionMockMessage() :
    // メンバ変数を初期化
    omnetpp::cPacket("CPM mock-up"),
    mFovContainers(std::make_shared<std::vector<FovContainer>>()),
    mObjectContainers(std::make_shared<std::vector<ObjectContainer>>()),
    mSensingIdContainers(std::make_shared<std::vector<SensingIdContainer>>())
{
}

void CollectivePerceptionMockMessage::setFovContainers(std::vector<FovContainer>&& fovs)
{
    mFovContainers = std::make_shared<std::vector<FovContainer>>(std::move(fovs));
    mExistFov = true;
}

void CollectivePerceptionMockMessage::setFovContainers(const std::vector<FovContainer>& fovs)
{
    mFovContainers = std::make_shared<std::vector<FovContainer>>(fovs);
    mExistFov = true;
}

void CollectivePerceptionMockMessage::setObjectContainers(std::vector<ObjectContainer>&& objs)
{
    mObjectContainers = std::make_shared<std::vector<ObjectContainer>>(std::move(objs));
}

void CollectivePerceptionMockMessage::setObjectContainers(const std::vector<ObjectContainer>& objs)
{
    mObjectContainers = std::make_shared<std::vector<ObjectContainer>>(objs);
}

void CollectivePerceptionMockMessage::setSensingIdContainers(std::vector<SensingIdContainer>&& objs)
{
    mSensingIdContainers = std::make_shared<std::vector<SensingIdContainer>>(std::move(objs));
}

void CollectivePerceptionMockMessage::setSensingIdContainers(const std::vector<SensingIdContainer>& objs)
{
    mSensingIdContainers = std::make_shared<std::vector<SensingIdContainer>>(objs);
}


omnetpp::cPacket* CollectivePerceptionMockMessage::dup() const
{
    return new CollectivePerceptionMockMessage(*this);
}


using namespace omnetpp;

class CpmSourceResultFilter : public cObjectResultFilter
{
protected:
    void receiveSignal(cResultFilter* prev, simtime_t_cref t, cObject* object, cObject* details) override
    {
        if (auto cpm = dynamic_cast<CollectivePerceptionMockMessage*>(object)) {
            fire(this, t, static_cast<long>(cpm->getSourceStation()), details);
        }
    }
};

Register_ResultFilter("cpmSource", CpmSourceResultFilter)

// 追加
class CpmGeneratedResultFilter : public cObjectResultFilter
{
protected:
    void receiveSignal(cResultFilter* prev, simtime_t_cref t, cObject* object, cObject* details) override
    {
        if (auto cpm = dynamic_cast<CollectivePerceptionMockMessage*>(object)) {
            fire(this, t, cpm->getCreationTime(), details);
        }
    }
};

Register_ResultFilter("cpmGenerated", CpmGeneratedResultFilter)

} // namespace artery

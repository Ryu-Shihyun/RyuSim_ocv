/*
* Artery V2X Simulation Framework
* Copyright 2019 Raphael Riebl et al.
* Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
*/

// #include "artery/envmod/sensor/FovSensor.h"
#include <math.h>
#include "artery/envmod/sensor/RadarSensor.h"
#include "artery/envmod/service/CollectivePerceptionMockMessage.h"
#include "artery/envmod/service/CollectivePerceptionMockService.h"
#include "artery/utility/IdentityRegistry.h"
#include "artery/envmod/GlobalEnvironmentModel.h"
#include "artery/utility/InitStages.h"
#include "artery/utility/PointerCheck.h"
#include <omnetpp/checkandcast.h>
#include <omnetpp/cmessage.h>
#include <omnetpp/cpacket.h>

#include <random>
#include <algorithm>
#include <vector>

#include <vanetza/btp/ports.hpp>
#include <vanetza/dcc/transmission.hpp>
#include <vanetza/dcc/transmit_rate_control.hpp>
#include <boost/units/cmath.hpp>
#include <boost/units/systems/si/prefixes.hpp>
#include "artery/envmod/EnvironmentModelObject.h"
#include <vanetza/facilities/cam_functions.hpp>
// #include <inet/common/packet/InetPacketPrinter.cc>

namespace artery
{



Define_Module(CollectivePerceptionMockService)

namespace
{

omnetpp::simsignal_t camSentSignal = omnetpp::cComponent::registerSignal("CamSent");
omnetpp::simsignal_t cpmSentSignal = omnetpp::cComponent::registerSignal("CpmSent");
omnetpp::simsignal_t cpmReceivedSignal = omnetpp::cComponent::registerSignal("CpmReceived");

} // namespace

// auto microdegree = vanetza::units::degree * boost::units::si::micro;
// auto decidegree = vanetza::units::degree * boost::units::si::deci;
// auto degree_per_second = vanetza::units::degree / vanetza::units::si::second;
// auto centimeter_per_second = vanetza::units::si::meter_per_second * boost::units::si::centi;

template<typename T, typename U>
long round(const boost::units::quantity<T>& q, const U& u)
{
	boost::units::quantity<U> v { q };
	return std::round(v.value());
}

CollectivePerceptionMockService::~CollectivePerceptionMockService()
{
    cancelAndDelete(mTrigger);
}

int CollectivePerceptionMockService::numInitStages() const
{
    return InitStages::Total;
}

// 初期化メソッド
void CollectivePerceptionMockService::initialize(int stage)
{
    if (stage == InitStages::Prepare) {
        ItsG5Service::initialize();
        mPositionProvider = &getFacilities().get_const<PositionProvider>();
        // mVehiclePositionProvider = &getFacilities().get_const<VehiclePositionProvider>(); // 追加
        mEnvironmentModel = &getFacilities().get_const<LocalEnvironmentModel>();
        mVehicleDataProvider = &getFacilities().get_const<VehicleDataProvider>();
        mIdentityRegistry = inet::getModuleFromPar<IdentityRegistry>(par("identityRegistryModule"), this);
	    mTimer = &getFacilities().get_const<Timer>();
        // GlobalEnvironmentModelへのポインタを初期化
        mGlobalEnvironmentModel = inet::getModuleFromPar<GlobalEnvironmentModel>(par("globalEnvironmentModule"), this);

        mDccProfile = par("dccProfile");
        mLengthHeader = par("lengthHeader");
        mLengthFovContainer = par("lengthFovContainer");
        mLengthObjectContainer = par("lengthObjectContainer");

        mGenerateAfterCam = par("generateAfterCam");
        mDccRestriction = par("withDccRestriction");
        mCpmOffset = par("cpmOffset");
        mCpmInterval = par("cpmInterval");
        mFovInterval = par("fovInterval");

        // vehicle dynamics thresholds
        mTimeDelta = par("timeDelta");
        mHeadingDelta = vanetza::units::Angle { par("headingDelta").doubleValue() * vanetza::units::degree };
        mPositionDelta = par("positionDelta").doubleValue() * vanetza::units::si::meter;
        mSpeedDelta = par("speedDelta").doubleValue() * vanetza::units::si::meter_per_second;

        // mIntervalFlag = par("intervalFlag");
        // mIntervalC0 = par("intervalC0");
        // mIntervalC1 = par("intervalC1");
        // mLastChanged = omnetpp::simTime();
        // mChangeInterval = par("changeInterval");
        // mAllowedSentNum = par("allowedSentNum");

        mCpmContainedCnt = par("cpmContainedCnt");
        mProposedFlag = par("proposedFlag");
        mRandomFlag = par("randomFlag");
        mOnlyCollisionTimeFlag = par("onlyCollisionTimeFlag");
        mAllFlag = par("allFlag");
        mK = par("k");
        // mFirstSent = omnetpp::SimTime {1100 + rand()%2 * 100, SIMTIME_MS };
        // std::cout << mFirstSent << "\n";
    } else if (stage == InitStages::Self) {
        mTrigger = new omnetpp::cMessage("triggger mock-up CPM");
        if (mGenerateAfterCam) {
            subscribe(camSentSignal);
        }
        mHostId = getFacilities().get_const<Identity>().host->getId();
        // 追加 sumo側でのIDを取得
        mTraciId = getFacilities().get_const<Identity>().traci;

        cpmGenerationTimeSignal = registerSignal("cpmGenerationTime");
        cpmSourceIdSignal = registerSignal("cpmSourceId");
        cpmContainedIdSignal = registerSignal("cpmContainedId");

        cpmContainedCntSignal = registerSignal("cpmContainedCnt");
        cpmContainedAllCntSignal = registerSignal("cpmContainedAllCnt");
        cpmContainedEtsiCntSignal = registerSignal("cpmContainedEtsiCnt");

        // objectPerceptionSignal = registerSignal("objectPerception");
        // objectDistanceSignal = registerSignal("objectDistance");
        aoiSignal = registerSignal("aoi");
        perceptedObjectDistanceSignal = registerSignal("perceptedObjectDistance");
        cpmReceivedCountSignal = registerSignal("cpmReceivedCount");
        perceptedObjectReletiveVelocitySignal = registerSignal("perceptedObjectReletiveVelocity");
        riskClassSignal = registerSignal("riskClass");
        collisionTimeSignal = registerSignal("collisionTime");
        perceptedVelocitySignal = registerSignal("perceptedVelocity");
        perceptedAccelerationSignal = registerSignal("perceptedAcceleration");
        perceptedYawrateSignal = registerSignal("perceptedYawrate");

        // receivedRiskSignal = registerSignal("receivedRisk");
        // cpmRecvCntSignal = registerSignal("cpmRecvCnt");
        posErrorSignal = registerSignal("posError");
        speedErrorSignal = registerSignal("speedError");
        headingErrorSignal = registerSignal("headingError");
        estimatedPosErrorSignal = registerSignal("estimatedPosError");

        // riskSignal = registerSignal("risk");
        // riskPosXSignal = registerSignal("riskPosX");
        // riskPosYSignal = registerSignal("riskPosY");
        // riskSpeedSignal = registerSignal("riskSpeed");
        // riskHeadingSignal = registerSignal("riskHeading");
        // riskAccelerationSignal = registerSignal("riskAcceleration");
        // riskYawrateSignal = registerSignal("riskYawrate");

        mLowerPosX = par("lowerPosX");
        mUpperPosX = par("upperPosX");
        mLowerPosY = par("lowerPosY");
        mUpperPosY = par("upperPosY");
    } else if (stage == InitStages::Propagate) {
        for (const Sensor* sensor : mEnvironmentModel->getSensors()) {
            // consider only sensors with a field of view
            // if (auto fovSensor = dynamic_cast<const FovSensor*>(sensor)) {
            if (auto fovSensor = dynamic_cast<const RadarSensor*>(sensor)) {
                CollectivePerceptionMockMessage::FovContainer fovContainer;
                fovContainer.sensorId = sensor->getId();
                fovContainer.position = sensor->position();
                fovContainer.fov = *(fovSensor->getFieldOfView());
                mFovContainers.emplace_back(std::move(fovContainer));
                mSensors.insert(sensor);
            } 
        }
    }
}

// self-messageを受信したら、パケットを生成
void CollectivePerceptionMockService::handleMessage(omnetpp::cMessage* msg)
{
    if (msg == mTrigger) {
        generatePacket();
    } else {
        ItsG5Service::handleMessage(msg);
    }
}

// CAMの後にCPMを送信する場合に使用するメソッド：camの送信シグナルを受信したら,self-messageをスケジュール
void CollectivePerceptionMockService::receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t signal,
        omnetpp::cObject* obj, omnetpp::cObject*)
{
    if (signal == camSentSignal) {
        scheduleAt(omnetpp::simTime() + mCpmOffset, mTrigger);
    }
}

// 前の送信タイミングに、dccによって得られた送信間隔を足した時刻に送信をスケジュール
void CollectivePerceptionMockService::trigger()
{
    // if (mFirstSent > omnetpp::simTime()) return;

    if (!mGenerateAfterCam && !mTrigger->isScheduled()) {
        if (mDccRestriction) {
            auto channel = getFacilities().get_const<MultiChannelPolicy>().primaryChannel(vanetza::aid::CP);
            auto netifc = notNullPtr(getFacilities().get_const<NetworkInterfaceTable>().select(channel));
            vanetza::dcc::TransmitRateThrottle* trc = notNullPtr(netifc->getDccEntity().getTransmitRateThrottle());
            vanetza::dcc::TransmissionLite tx { static_cast<vanetza::dcc::Profile>(mDccProfile), 0 };
            
            const omnetpp::SimTime interval = std::chrono::duration<double>(trc->interval(tx)).count();
            const omnetpp::SimTime next = omnetpp::simTime() + mCpmOffset;
            if (mTrigger->getArrivalTime() + std::max(interval, mCpmInterval) <= next) {
                scheduleAt(next, mTrigger);
                // std::cout << "dcc interval " << interval << "\n";
            }
        } else {
            // const omnetpp::SimTime interval = mIntervalFlag ? mIntervalC0 : mCpmInterval;
            const omnetpp::SimTime interval = mCpmInterval;
            // std::cout << interval << "\n";
            const omnetpp::SimTime next = omnetpp::simTime() + mCpmOffset;
            if (mTrigger->getArrivalTime() + interval <= next) {
                scheduleAt(next, mTrigger);
                // std::cout << "no dcc interval " << interval << "\n";
            }
        }
    }

    // aoiを計算して、シグナルを送信
    double offset = 0.8, thretholdD = 20.0, min_a = 4.5;
    double posX = round(mVehicleDataProvider->position().x, vanetza::units::si::meter);
    double posY = round(mVehicleDataProvider->position().y, vanetza::units::si::meter);
    // std::cout << mLowerPosX << ", " << mUpperPosX << ", " << mLowerPosY << ", " << mUpperPosY << "\n";
    std::cout << mTraciId << "\n";
    if (posX >= mLowerPosX && posX <= mUpperPosX && posY >= mLowerPosY && posY <= mUpperPosY) {
        // using TrackedObject = LocalEnvironmentModel::TrackedObject;
        for (auto object : mEnvironmentModel->allObjects()) {
            auto tracking = object.second;
            std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
            if (obj) {
                std::string targetId = obj->getExternalId();
                auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(targetId);
                if (identity) {
                    double dist = round(distance(mVehicleDataProvider->position(), obj->getVehicleData().position()), vanetza::units::si::meter);
                    double delta_vx = mVehicleDataProvider->speed().value() * sin(mVehicleDataProvider->heading().value()) - obj->getVehicleData().speed().value() * sin(obj->getVehicleData().heading().value());
                    double delta_vy = mVehicleDataProvider->speed().value() * -cos(mVehicleDataProvider->heading().value()) - obj->getVehicleData().speed().value() * -cos(obj->getVehicleData().heading().value());
                    auto reletiveVelocity = std::sqrt(delta_vx * delta_vx + delta_vy * delta_vy);
                    emit(perceptedObjectDistanceSignal, dist);
                    emit(perceptedObjectReletiveVelocitySignal, reletiveVelocity);

                    // 各センサについて、最も最近に物体を認識したセンサをもとに、AoIを計算
                    omnetpp::SimTime latest{0, SIMTIME_MS};
                    for (auto sensor: tracking.sensors()) {
                        latest = std::max(latest, sensor.second.last());
                    }
                    omnetpp::SimTime aoi = simTime() - latest;
                    emit(aoiSignal, aoi);
                    emit(cpmReceivedCountSignal, tracking.getSize100());
                    // std::cout << tracking.getSize100() << "\n";

                    int riskClass = 0;
                    double collisionT = 0.0;
                    auto f = [&](double t) -> double {
                        double targetX  = obj->getVehicleData().position().x.value() + obj->getVehicleData().speed().value() * sin(obj->getVehicleData().heading().value()) * (omnetpp::simTime().dbl() + t - obj->getVehicleData().updated().dbl());
                        double targetY =  obj->getVehicleData().position().y.value() - obj->getVehicleData().speed().value() * cos(obj->getVehicleData().heading().value()) * (omnetpp::simTime().dbl() + t - obj->getVehicleData().updated().dbl());
                        double x = mVehicleDataProvider->position().x.value() + mVehicleDataProvider->speed().value() * sin(mVehicleDataProvider->heading().value()) * (omnetpp::simTime().dbl() + t - mVehicleDataProvider->updated().dbl());
                        double y = mVehicleDataProvider->position().y.value() - mVehicleDataProvider->speed().value() * cos(mVehicleDataProvider->heading().value()) * (omnetpp::simTime().dbl() + t - mVehicleDataProvider->updated().dbl());
                        double dist = std::sqrt(std::pow(targetX - x, 2) + std::pow(targetY - y, 2));
                        // if (mTraciId == "17.0" && targetId == "83.0") std::cout << "(x, y)=" << x << ", " << y << " (tX, tY)=" << targetX << ", " << targetY << " dist=" << dist << "\n";
                        // else if (mTraciId == "17.0") std::cout << targetId << "\n";
                        return dist; 
                    };
                    while (collisionT < 20 && f(collisionT) > thretholdD) {
                        collisionT += 0.1;
                    }
                    // if ()
                    if (collisionT < offset + obj->getVehicleData().speed().value() / min_a) riskClass = 0;
                    else riskClass = 1;
                    emit(riskClassSignal, riskClass);
                    emit(collisionTimeSignal, collisionT);
                    emit(perceptedVelocitySignal, obj->getVehicleData().speed().value());
                    emit(perceptedAccelerationSignal, obj->getVehicleData().acceleration().value());
                    emit(perceptedYawrateSignal, obj->getVehicleData().yaw_rate().value());
                    // if (mTraciId == "189.0") std::cout << targetId << ": " << obj->getVehicleData().speed().value() << "m/s, " << obj->getVehicleData().acceleration().value() << "m/s^2, " << obj->getVehicleData().yaw_rate().value() <<  " radian/s\n";   
                    // if (mTraciId == "95.0") {
                    //     std::cout << tracking.traci() << ": " << delta_vx << ", " << delta_vy << " = " << reletiveVelocity << "m/s \n";
                    // }
                    // std::cout << tracking.traci() << ": " << tracking.getPosX() << ", " << tracking.getPosY() << ", " << tracking.getSpeed() << ", " << tracking.getHeading() << "\n";
                    // double posErr = std::sqrt(std::pow(tracking.getPosX() -  obj->getVehicleData().position().x.value(), 2) + std::pow(tracking.getPosY() -  obj->getVehicleData().position().y.value(), 2));
                    // double speedErr = abs(tracking.getSpeed() - obj->getVehicleData().speed().value());
                    // double headingErr = abs(tracking.getHeading() - obj->getVehicleData().heading().value());
                    // double estimatedPosX = tracking.getPosX() + tracking.getSpeed() * sin(tracking.getHeading()) * (obj->getVehicleData().updated().dbl() - tracking.getLastTime().dbl());
                    // double estimatedPosY = tracking.getPosY() - tracking.getSpeed() * cos(tracking.getHeading()) * (obj->getVehicleData().updated().dbl() - tracking.getLastTime().dbl()) ;
                    // double estimatedPosErr = std::sqrt(std::pow(estimatedPosX -  obj->getVehicleData().position().x.value(), 2) + std::pow(estimatedPosY -  obj->getVehicleData().position().y.value(), 2));
                    
                    // emit(posErrorSignal, posErr);
                    // emit(speedErrorSignal, speedErr);
                    // emit(headingErrorSignal, headingErr);
                    // emit(estimatedPosErrorSignal, estimatedPosErr);

                    // double risk = tracking.getRisk();
                    // emit(receivedRiskSignal, risk);
                    // if (mTraciId == "95.0" && tracking.traci() == "89.0") {
                    //     std::cout << tracking.traci() << ": updated: " << obj->getVehicleData().updated().dbl() << "s, last time: " << tracking.getLastTime().dbl() << "\n";
                    //     std::cout << "True: " << obj->getVehicleData().position().x.value() << "m, " << obj->getVehicleData().position().y.value() << "m, " << obj->getVehicleData().speed().value() << "m/s, " << obj->getVehicleData().heading().value() << "radian\n";
                    //     std::cout << "have: " << tracking.getPosX() << "m, " << tracking.getPosY() << "m, " << tracking.getSpeed() << "m/s, " << tracking.getHeading() << "radian\n";
                    //     std::cout << "estimate: " << estimatedPosX << "m, " << estimatedPosY << "m, " << estimatedPosErr << "m\n"; 
                    //     // std::cout << tracking.traci() << ": " << posErr << ", " << speedErr << ", " << headingErr << ", " << estimatedPosX << ", " << estimatedPosY << ", " << estimatedPosErr << "\n";
                    //     // std::cout << "pos : " << tracking.getPosX() << ", " << tracking.getPosY() << "\n";
                    //     // std::cout << "time delta: " << obj->getVehicleData().updated().dbl() << ", " << tracking.getLastTime().dbl() << "\n";
                    //     // std::cout << "ture pos: " << obj->getVehicleData().position().x.value() << ", " << obj->getVehicleData().position().y.value() << "\n";
                    // }
                }
            }
        }
    }
    
    // 各対象車両の危険度クラスを計算
    // using TrackedObject = LocalEnvironmentModel::TrackedObject;
    // auto sensingIds = mEnvironmentModel->getSensingIds();
    // for (const TrackedObject& object : mEnvironmentModel->allObjects()) {
    //     const LocalEnvironmentModel::Tracking& tracking = object.second;
    //     std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
    //     if (obj) {
    //         std::string targetId = obj->getExternalId();
    //         auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(targetId);
    //         if (identity) {
    //             // トラッキング情報から、各センサのトラッキング情報を見る
    //             for (const auto& sensor : tracking.sensors()) {
    //                 // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
    //                 if (mSensors.find(sensor.first) != mSensors.end()) {
    //                     // センサーの有効期限内にその物体を認識しているかチェック
    //                     if (sensor.second.last() + sensor.first->getValidityPeriod() >= omnetpp::simTime()) {
    //                         // 対象車両の、各受信車両との危険度を計算
    //                         for (auto rcvObject : mEnvironmentModel->allObjects()) {
    //                             auto rcvTracking = rcvObject.second;
    //                             std::shared_ptr<EnvironmentModelObject> rcvObj = rcvObject.first.lock();
    //                             if (rcvObj) {
    //                                 std::string rcvId = rcvObj->getExternalId();
    //                                 auto rcvIdentity = mIdentityRegistry->lookup<IdentityRegistry::traci>(rcvId);
    //                                 // 受信車両と対象車両が同じならスキップ
    //                                 if (rcvId == targetId) continue;
    //                                 if (rcvIdentity) {
    //                                     // 受信車両が対象車両をセンシングしていなければ, 危険度クラスを計算
    //                                     if (sensingIds.find(rcvId) != sensingIds.end() && sensingIds[rcvId].find(targetId) == sensingIds[rcvId].end()) {
    //                                         auto f = [&](double t) -> double {
    //                                             double targetX  = tracking.getPosX() + tracking.getSpeed() * sin(tracking.getHeading()) * (t - tracking.getLastTime().dbl());
    //                                             double targetY = tracking.getPosY() - tracking.getSpeed() * cos(tracking.getHeading()) * (t - tracking.getLastTime().dbl());
    //                                             double rcvX = rcvTracking.getPosX() + rcvTracking.getSpeed() * sin(rcvTracking.getHeading()) * (t - rcvTracking.getLastTime().dbl());
    //                                             double rcvY = rcvTracking.getPosY() - rcvTracking.getSpeed() * cos(rcvTracking.getHeading()) * (t - rcvTracking.getLastTime().dbl());
    //                                             double dist = std::sqrt(std::pow(targetX - rcvX, 2) + std::pow(targetY - rcvY, 2));
    //                                             return dist;
    //                                         };
    //                                         int riskClass;
    //                                         double collisionT = 0.0, offset = 0.8, thretholdD = 20.0, min_a = 4.5;
    //                                         while (collisionT < 10 and f(collisionT) > thretholdD) {
    //                                             collisionT += 0.1;
    //                                         }
    //                                         if (collisionT > offset + tracking.getSpeed() / min_a) riskClass = 0;
    //                                         else targetInterval = std::min(mIntervalC1, targetInterval);
    //                                         // double dist = round(distance(obj->getVehicleData().position(), rcvObj->getVehicleData().position()), vanetza::units::si::meter);
    //                                         // double delta_vx = obj->getVehicleData().speed().value() * sin(obj->getVehicleData().heading().value()) - receiveObj->getVehicleData().speed().value() * sin(receiveObj->getVehicleData().heading().value());
    //                                         // double delta_vy = obj->getVehicleData().speed().value() * -cos(obj->getVehicleData().heading().value()) - receiveObj->getVehicleData().speed().value() * -cos(receiveObj->getVehicleData().heading().value());
    //                                         // auto reletiveVelocity = std::sqrt(delta_vx * delta_vx + delta_vy * delta_vy);



    //                                         // if (mTraciId == "24.0" && targetId == "32.0" && receiveId == "0.0") {
    //                                         //     std::cout << mTraciId <<" perceive " << receiveId << "not sensing " << targetId << ": dist=" << dist << ", vx=" << delta_vx << ", vy=" << delta_vy << ", reVel=" << reletiveVelocity << "\n";
    //                                         // }
    //                                     }
    //                                 }
    //                             }
    //                         }
    //                     }
    //                     break;                
    //                 }
    //             }
    //         }
    //     }
    // }

    // 提案手法の実装：mChangeInterval[s]ごとに、各対象車両の送信間隔を決定
    // if (mIntervalFlag && mLastChanged + mChangeInterval <= omnetpp::simTime()) {
    //     using TrackedObject = LocalEnvironmentModel::TrackedObject;
    //     auto allObjects = mEnvironmentModel->allObjects();
    //     auto sensingIds = mEnvironmentModel->getSensingIds();
    //     for (const TrackedObject& object : allObjects) {
    //         const LocalEnvironmentModel::Tracking& tracking = object.second;
    //         std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
    //         if (obj) {
    //             std::string targetId = obj->getExternalId();
    //             auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(targetId);
    //             if (identity) {
    //                 for (const auto& sensor : tracking.sensors()) {
    //                     // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
    //                     if (mSensors.find(sensor.first) != mSensors.end()) {
    //                         // センサーの有効期限内にその物体を認識していなければ、スキップ
    //                         if (sensor.second.last() + sensor.first->getValidityPeriod() < omnetpp::simTime()) continue; 
                            
    //                         omnetpp::SimTime targetInterval = mIntervalC1;
    //                         // 各対象車両の危険度クラスを計算// 衝突時間がオフセット時間＋対処時間を超えていたら、危険度クラスは0
    //                         for (auto rcvObject : mEnvironmentModel->allObjects()) {
    //                             auto rcvTracking = rcvObject.second;
    //                             std::shared_ptr<EnvironmentModelObject> rcvObj = rcvObject.first.lock();
    //                             if (rcvObj) {
    //                                 std::string rcvId = rcvObj->getExternalId();
    //                                 // 受信車両と対象車両が同じならスキップ
    //                                 auto rcvIdentity = mIdentityRegistry->lookup<IdentityRegistry::traci>(rcvId);
    //                                 if (rcvId == targetId) continue;
    //                                 if (rcvIdentity) {
    //                                     // 受信車両が対象車両をセンシングしていなければ, 危険度クラスを計算
    //                                     if (sensingIds.find(rcvId) != sensingIds.end()) {
    //                                         if (sensingIds[rcvId].find(targetId) == sensingIds[rcvId].end()) {
    //                                             // 2分探索で衝突時間を求める
    //                                             // double collisionT, minT;
    //                                             // int low = 0, high = 1000;
    //                                             // double thretholdD = 20.0;
    //                                             // double offset = 0.8, min_a = 4.5;
    //                                             // auto f = [&](int c) -> double {
    //                                             //     double t = (double) c / 10.0;
    //                                             //     double targetX  = tracking.getPosX() + tracking.getSpeed() * sin(tracking.getHeading()) * (t - tracking.getLastTime().dbl());
    //                                             //     double targetY = tracking.getPosY() - tracking.getSpeed() * cos(tracking.getHeading()) * (t - tracking.getLastTime().dbl());
    //                                             //     double rcvX = rcvTracking.getPosX() + rcvTracking.getSpeed() * sin(rcvTracking.getHeading()) * (t - rcvTracking.getLastTime().dbl());
    //                                             //     double rcvY = rcvTracking.getPosY() - rcvTracking.getSpeed() * cos(rcvTracking.getHeading()) * (t - rcvTracking.getLastTime().dbl());
    //                                             //     double dist = std::sqrt(std::pow(targetX - rcvX, 2) + std::pow(targetY - rcvY, 2));
    //                                             //     return dist;
    //                                             // };
                                               
    //                                             // while(high - low > 2) {
    //                                             //     int c1 = (low * 2 + high) / 3, c2 = (low + 2 * high) / 3;
    //                                             //     if (f(c1) < f(c2)) high = c2;
    //                                             //     else low = c1;
    //                                             // }
    //                                             // minT = (double) std::min({f(low), f(low+1), f(low+2), f(high)}) / 10.0;
    //                                             // low = 0, high = minT * 10;
    //                                             // while(high - low > 1) {
    //                                             //     int mid = (low + high) / 2;
    //                                             //     if (f(mid) < thretholdD) high = mid;
    //                                             //     else low = mid; 
    //                                             // }
                                                
    //                                             // collisionT = (double) high / 10.0;
    //                                             auto f = [&](double t) -> double {
    //                                                 double targetX  = tracking.getPosX() + tracking.getSpeed() * sin(tracking.getHeading()) * (omnetpp::simTime().dbl() + t - tracking.getLastTime().dbl());
    //                                                 double targetY = tracking.getPosY() - tracking.getSpeed() * cos(tracking.getHeading()) * (omnetpp::simTime().dbl() + t - tracking.getLastTime().dbl());
    //                                                 double rcvX = rcvTracking.getPosX() + rcvTracking.getSpeed() * sin(rcvTracking.getHeading()) * (omnetpp::simTime().dbl() + t - rcvTracking.getLastTime().dbl());
    //                                                 double rcvY = rcvTracking.getPosY() - rcvTracking.getSpeed() * cos(rcvTracking.getHeading()) * (omnetpp::simTime().dbl() + t - rcvTracking.getLastTime().dbl());
    //                                                 double dist = std::sqrt(std::pow(targetX - rcvX, 2) + std::pow(targetY - rcvY, 2));
    //                                                 return dist;
    //                                             };
    //                                             double collisionT = 0.0;
    //                                             while (collisionT < 10 && f(collisionT) > thretholdD) {
    //                                                 collisionT += 0.1;
    //                                             }
    //                                             // 衝突時間がオフセット時間＋対処時間を未満なら、危険度クラスは0
    //                                             if (collisionT < offset + tracking.getSpeed() / min_a) targetInterval = std::min(mIntervalC0, targetInterval);
    //                                             else targetInterval = std::min(mIntervalC1, targetInterval);
    //                                             // if (mTraciId == "60.0" && targetId == "228.0") std::cout << rcvId << ": " << collisionT << ", " << offset + tracking.getSpeed() / min_a << "\n";
    //                                         }
    //                                     }
    //                                 }
    //                             }
    //                         }


    //                         // 対象車両と、その車両をセンシングしている車両との間の距離順が優先度を割り当て、allowedSentNum台以降の送信間隔を無限に変更
    //                         std::vector<std::pair<double, std::string>> sensedDist;
    //                         auto sensedIds = tracking.getSensedIds();
    //                         for (auto sensedId: sensedIds) {
    //                             auto sensedObject = mGlobalEnvironmentModel->getObject(sensedId.first);
    //                             auto foundObject = allObjects.find(sensedObject);
    //                             if (foundObject != allObjects.end()) {
    //                                 const LocalEnvironmentModel::Tracking& sensedTracking = foundObject->second;
    //                                 double estimatedPosX = sensedTracking.getPosX() + sensedTracking.getSpeed() * sin(sensedTracking.getHeading()) * (obj->getVehicleData().updated().dbl() - sensedTracking.getLastTime().dbl());
    //                                 double estimatedPosY = sensedTracking.getPosY() - sensedTracking.getSpeed() * cos(sensedTracking.getHeading()) * (obj->getVehicleData().updated().dbl() - sensedTracking.getLastTime().dbl()) ;
    //                                 double dist = std::sqrt(std::pow(estimatedPosX -  obj->getVehicleData().position().x.value(), 2) + std::pow(estimatedPosY -  obj->getVehicleData().position().y.value(), 2));
    //                                 // if (mTraciId == "36.0" && targetId == "66.0") std::cout << "  " << targetId << " <-> " << sensedId.first << ": dist = " << dist << "m \n";
    //                                 sensedDist.emplace_back(dist, sensedId.first);
    //                             }
    //                         }
    //                         // 対象車両と自車両間の距離を計算
    //                         auto dist = std::sqrt(std::pow(mVehicleDataProvider->position().x.value() -  obj->getVehicleData().position().x.value(), 2) + std::pow(mVehicleDataProvider->position().y.value() -  obj->getVehicleData().position().y.value(), 2));
    //                         sensedDist.emplace_back(dist, mTraciId);
    //                         // 距離に応じてセンシング車両をソート
    //                         std::sort(sensedDist.begin(), sensedDist.end());
    //                         int myPriority = 0;
    //                         for (auto it = sensedDist.begin(); it != sensedDist.end(); it++) {
    //                             if (it->second == mTraciId) break;
    //                             else myPriority++;
    //                         }
    //                         if (myPriority >= mAllowedSentNum) mIntervals[targetId] = omnetpp::SimTime { 50000, SIMTIME_MS };
    //                         else mIntervals[targetId] = targetInterval;
    //                         // if (targetId == "66.0") std::cout << " " << mTraciId << ", priority: " << myPriority << "\n";
    //                         // if (targetId == "228.0") std::cout << mTraciId << " send: interval = " << mIntervals[targetId] << " s \n";
    //                     }
    //                 }
    //             }
    //         }
    //     }
    //     mLastChanged = omnetpp::simTime();
    // } 
    // 各車両の危険度を計算
    // if (mTraciId == "24.0") std::cout << mTraciId << "\n";
    // using TrackedObject = LocalEnvironmentModel::TrackedObject;
    // auto sensingIds = mEnvironmentModel->getSensingIds();
    // for (const TrackedObject& object : mEnvironmentModel->allObjects()) {
    //     const LocalEnvironmentModel::Tracking& tracking = object.second;
    //     std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
    //     if (obj) {
    //         std::string tgtId = obj->getExternalId();
    //         auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(tgtId);
    //         if (identity) {
    //             // トラッキング情報から、各センサのトラッキング情報を見る
    //             for (const auto& sensor : tracking.sensors()) {
    //                 // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
    //                 if (mSensors.find(sensor.first) != mSensors.end()) {
    //                     // センサーの有効期限内にその物体を認識していなければ、スキップ
    //                     if (sensor.second.last() + sensor.first->getValidityPeriod() < omnetpp::simTime()) continue; 

    //                     // 対象車両の危険度を計算
    //                     // if (mTraciId == "24.0"  && tgtId == "32.0") std::cout << "tgtId: " << tgtId << "\n";
    //                     double sum_w = 0, sum_wx = 0, sum_wy = 0;
    //                     for (auto rcvObject : mEnvironmentModel->allObjects()) {
    //                         auto rcvTracking = rcvObject.second;
    //                         std::shared_ptr<EnvironmentModelObject> rcvObj = rcvObject.first.lock();
    //                         if (rcvObj) {
    //                             std::string rcvId = rcvObj->getExternalId();
    //                             // 受信車両と対象車両が同じならスキップ
    //                             auto rcvIdentity = mIdentityRegistry->lookup<IdentityRegistry::traci>(rcvId);
    //                             if (rcvId == tgtId) continue;
    //                             if (rcvIdentity) {
    //                                 // 受信車両が対象車両をセンシングしていなければ, 危険度の計算に組み込む
                                    
    //                                 if (sensingIds.find(rcvId) != sensingIds.end()) {
    //                                     if (sensingIds[rcvId].find(tgtId) == sensingIds[rcvId].end()) {
    //                                         double w = 300 - std::sqrt(std::pow(tracking.getPosX() - rcvTracking.getPosX(), 2.0) + std::pow(tracking.getPosY() - rcvTracking.getPosY(), 2.0));
    //                                         if (w >= 0) {
    //                                             double delta_vx = abs((double) tracking.getSpeed() * sin(tracking.getHeading()) - (double) rcvTracking.getSpeed() * sin(rcvTracking.getHeading()));
    //                                             double delta_vy = abs((double) tracking.getSpeed() * cos(tracking.getHeading()) - (double) rcvTracking.getSpeed() * cos(rcvTracking.getHeading()));
    //                                             sum_wx += w * delta_vx;
    //                                             sum_wy += w * delta_vy;
    //                                             sum_w += w;
    //                                             // if (mTraciId == "24.0" && tgtId == "32.0") {
    //                                             //     std::cout <<  "tgtId<->rcvId: " << rcvId << " w: " << w << "m, " << delta_vx << "m/s, " << delta_vy << "\n"; 
    //                                             // }
    //                                         }
    //                                     }
    //                                     // else {
    //                                     //     if (mTraciId == "24.0" && tgtId == "32.0" && rcvId == "0.0") {
    //                                     //     std::cout << mTraciId <<" perceive " << rcvId << "sensing " << tgtId << "\n";
    //                                     //     }
    //                                     // }
    //                                 }
    //                             }
    //                         }
    //                     }
    //                     double delta_vx = 0, delta_vy = 0;
    //                     if (sum_w != 0) {
    //                         delta_vx = sum_wx / sum_w;
    //                         delta_vy = sum_wy / sum_w;
    //                     }
    //                     double delta_v = sqrt(delta_vx * delta_vx + delta_vy * delta_vy);
    //                     double risk = delta_v / 2 / 16.67;
    //                     mRiskMap[tgtId] = risk;

    //                     emit(riskSignal, risk);
    //                     emit(riskPosXSignal, obj->getVehicleData().position().x.value());
    //                     emit(riskPosYSignal, obj->getVehicleData().position().y.value());
    //                     emit(riskSpeedSignal, obj->getVehicleData().speed().value());
    //                     emit(riskHeadingSignal, obj->getVehicleData().heading().value());
    //                     emit(riskAccelerationSignal, obj->getVehicleData().acceleration().value());
    //                     emit(riskYawrateSignal, obj->getVehicleData().yaw_rate().value());
    //                     // if (mTraciId == "30.0" && tgtId == "55.0") 
    //                     //     std::cout << tgtId << ": delta_vx: " << delta_vx << ", delta_vy: " << delta_vy << ": row:" << row << "\n";
    //                 }
    //             }
    //         }
    //     }
    // }    
}

// CPM受信時に呼び出されるメソッド
void CollectivePerceptionMockService::indicate(const vanetza::btp::DataIndication&, omnetpp::cPacket* packet)
{
    auto cpm = omnetpp::check_and_cast<CollectivePerceptionMockMessage*>(packet);
    // if (cpm) {
    //     std::cout << omnetpp::simTime() << ": " << mTraciId << " received from " << cpm->getTraciId() << "\n";
    // }
    emit(cpmReceivedSignal, cpm);
    delete packet;
}

// CPMを生成するメソッド
void CollectivePerceptionMockService::generatePacket()
{
    // AoIと物体認識確率をシグナルで送信
    //  for (auto object: mEnvironmentModel->allObjects()) {
    //     // そのオブジェクトがまだシミュレーション上に存在するかチェック
    //     std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
    //     if (obj) {
    //         auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
    //         if (identity) {
    //             // オブジェクトとの距離をシグナルで送信
    //             auto dist = round(distance(mVehicleDataProvider->position(), obj->getVehicleData().position()), vanetza::units::si::meter);
    //             emit(perceptedObjectDistanceSignal, dist);

    //             // 各センサについて、最も最近に物体を認識したセンサをもとに、AoIを計算
    //             auto tracking = object.second;
    //             omnetpp::SimTime latest{0, SIMTIME_MS};
    //             for (auto sensor: tracking.sensors()) {
    //                 latest = std::max(latest, sensor.second.last());
    //             }
    //             omnetpp::SimTime aoi = simTime() - latest;
    //             emit(aoiSignal, aoi);
    //         }
    //     }
    // }

    // BTP層へ送るリクエストを生成
    using namespace vanetza;
    btp::DataRequestB req;
    req.destination_port = host_cast<PortNumber>(getPortNumber());
    req.gn.transport_type = geonet::TransportType::SHB;
    req.gn.traffic_class.tc_id(mDccProfile);
    req.gn.communication_profile = geonet::CommunicationProfile::ITS_G5;

    // CPMを生成し、サイズをヘッダサイズ分だけ設定
    auto packet = new CollectivePerceptionMockMessage();
    packet->setByteLength(mLengthHeader);

    uint16_t genDeltaTimeMod = countTaiMilliseconds(mTimer->getTimeFor(mVehicleDataProvider->updated()));
    packet->setGenerationDeltaTime(genDeltaTimeMod);

    // SUMOのIDをcpmに追加 
    packet->setTraciId(mTraciId);
    packet->setPosX(mVehicleDataProvider->position().x.value());
    packet->setPosY(mVehicleDataProvider->position().y.value());
    packet->setSpeed(mVehicleDataProvider->speed().value());
    packet->setHeading(mVehicleDataProvider->heading().value());
    
    // std::cout << packet->getExistFov() << std::endl;
    // 一定インターバルごとに、cpmにFOVコンテナを追加
    if (mFovLast + mFovInterval <= omnetpp::simTime()) {
        // std::cout << omnetpp::simTime() << "set fov\n";
        packet->setFovContainers(mFovContainers);
        packet->addByteLength(mLengthFovContainer * mFovContainers.size());
        mFovLast = omnetpp::simTime();
    }

    // SICコンテナを追加
    std::vector<CollectivePerceptionMockMessage::SensingIdContainer> sensingIdContainers;
    using TrackedObject = LocalEnvironmentModel::TrackedObject;
    // if (mTraciId == "0.0") std::cout << mTraciId << " send sensingIdContainers\n";
    for (const TrackedObject& object : mEnvironmentModel->allObjects()) {
        const LocalEnvironmentModel::Tracking& tracking = object.second;
        std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
        if (obj) {
            auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
            if (identity) {
                    // トラッキング情報から、各センサのトラッキング情報を見る
                for (const auto& sensor : tracking.sensors()) {
                    // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
                    if (mSensors.find(sensor.first) != mSensors.end()) {
                        // センサーの有効期限内にその物体を認識していなければ、スキップ
                        if (sensor.second.last() + sensor.first->getValidityPeriod() < omnetpp::simTime()) continue; 
                        CollectivePerceptionMockMessage::SensingIdContainer sensingIdContainer;
                        sensingIdContainer.objectId = tracking.traci();
                        sensingIdContainer.object = object.first;
                        // if (mTraciId == "0.0") std::cout << "  " << sensingIdContainer.objectId << ", ";
                        sensingIdContainers.emplace_back(std::move(sensingIdContainer));
                    }
                }
            }
        }
    }
    // if (mTraciId == "0.0") std::cout << "\n";
    packet->setSensingIdContainers(sensingIdContainers);

    // 以下でCPMに含める物体の候補を選ぶ
    // 物体コンテナを追加
    std::vector<CollectivePerceptionMockMessage::ObjectContainer> objectContainers;
    //　ローカル環境に含まれる全オブジェクトを見る
    using TrackedObject = LocalEnvironmentModel::TrackedObject;
    // ETSIの動的生成ルールに該当したオブジェクトの配列と、実際に送信するオブジェクトの配列
    std::vector<std::string> sentAllowedObjects = {};
    std::set<std::string> sentObjects = {};
    // 提案手法：車両の衝突予想時間の最小値と、CPMの送信台数と、車両id, 
    std::vector<std::tuple<double, int, std::string>> proposedSentAllowedObjects = {};
    double maxT = 20.0, thretholdD = 20.0;

    int cpmContainedAllCnt = 0;
    auto allObjects = mEnvironmentModel->allObjects();
    for (const TrackedObject& object : allObjects) {
        // 各オブジェクトのトラッキング情報を見る　object.first = 物体へのポインタ、object.second = トラッキング情報
        const LocalEnvironmentModel::Tracking& tracking = object.second;
        // 物体がシミュレーション上に存在するかチェック
        std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
        std::string targetId = tracking.traci();
        if (obj) {
            // std::cout << obj->getExternalId() << "\n";
            // round(obj->getVehicleData().position().x, vanetza::units::si::meter) << "m, " << 
            // round(obj->getVehicleData().speed(), centimeter_per_second) * SpeedValue_oneCentimeterPerSec << "cm/s, " <<
            // round(obj->getVehicleData().heading(), decidegree) << "deci°" << "\n";
            // 物体のアイデンディティが存在するかチェック
            auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
            if (!identity) continue;
        } else continue;
                    // if (!mIntervalFlag) { 
                    // ETSIの標準に基づき、動的なルールでチェック
                    // if (!checkNewSentCpm(object.first) && 
                    // !checkTimeDelta(obj) && 
                    // !checkPositionDelta(obj) && 
                    // !checkSpeedDelta(obj) && 
                    // !checkHeadingDelta(obj)) continue;
                // }
        //     } else continue;
        // } else {
        //     // std::cout << "object expired\n";
        //     continue;
        // }

        // トラッキング情報から、各センサのトラッキング情報を見る
        for (const auto& sensor : tracking.sensors()) {
            // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
            if (mSensors.find(sensor.first) != mSensors.end()) {
                // センサーの有効期限内にその物体を認識していなければ、スキップ
                if (sensor.second.last() + sensor.first->getValidityPeriod() < omnetpp::simTime()) continue; 
                cpmContainedAllCnt++;
                // 周期的に送信する場合
                // if (mIntervalFlag) {
                //     if (mIntervals.find(targetId) == mIntervals.end()) {
                //         // mIntervals[targetId] = rand() % 2 == 0 ? mIntervalC0 : mIntervalC1;
                //         mIntervals[targetId] = mIntervalC0;
                //         mLastSent[targetId] = omnetpp::simTime();
                //     } else {
                //         if (mIntervals[targetId] + mLastSent[targetId] > omnetpp::simTime()) continue;
                //     }
                // } else { 

                // ここに提案手法を実装: 各対象車両の衝突時間の最小値を計算して、ソート
                if (mProposedFlag || mOnlyCollisionTimeFlag) {
                    double minCollisionTime = maxT;
                    // 各対象車両の衝突時間を計算
                    auto sensingIds = mEnvironmentModel->getSensingIds(); // 各車両がセンシングしている車両のid
                    for (auto rcvObject : mEnvironmentModel->allObjects()) {
                        auto rcvTracking = rcvObject.second;
                        std::shared_ptr<EnvironmentModelObject> rcvObj = rcvObject.first.lock();
                        if (rcvObj) {
                            std::string rcvId = rcvObj->getExternalId();
                            // 受信車両と対象車両が同じならスキップ
                            auto rcvIdentity = mIdentityRegistry->lookup<IdentityRegistry::traci>(rcvId);
                            if (rcvId == targetId) continue;
                            if (rcvIdentity) {
                                // 受信車両が対象車両をセンシングしていなければ, 危険度クラスを計算
                                if (sensingIds.find(rcvId) != sensingIds.end() && sensingIds[rcvId].find(targetId) == sensingIds[rcvId].end()) {
                                    auto f = [&](double t) -> double {
                                        double targetX  = tracking.getPosX() + tracking.getSpeed() * sin(tracking.getHeading()) * (omnetpp::simTime().dbl() + t - tracking.getLastTime().dbl());
                                        double targetY = tracking.getPosY() - tracking.getSpeed() * cos(tracking.getHeading()) * (omnetpp::simTime().dbl() + t - tracking.getLastTime().dbl());
                                        double rcvX = rcvTracking.getPosX() + rcvTracking.getSpeed() * sin(rcvTracking.getHeading()) * (omnetpp::simTime().dbl() + t - rcvTracking.getLastTime().dbl());
                                        double rcvY = rcvTracking.getPosY() - rcvTracking.getSpeed() * cos(rcvTracking.getHeading()) * (omnetpp::simTime().dbl() + t - rcvTracking.getLastTime().dbl());
                                        double dist = std::sqrt(std::pow(targetX - rcvX, 2) + std::pow(targetY - rcvY, 2));
                                        return dist;
                                    };
                                    double collisionT = 0.0;
                                    while (collisionT < maxT && f(collisionT) > thretholdD) {
                                        collisionT += 0.1;
                                    }
                                    minCollisionTime = std::min(collisionT, minCollisionTime);
                                }
                            }
                        }
                    } 
                    // 最小の衝突予想時刻、CPM送信数、車両idを配列に入れる
                    proposedSentAllowedObjects.emplace_back(minCollisionTime, tracking.getSize(), targetId);
                    // if (mTraciId == "243.0") std::cout << targetId << ": " << minCollisionTime << " s\n";
                } else if (mRandomFlag || mAllFlag) {
                    sentAllowedObjects.push_back(targetId);
                    // if (mTraciId == "243.0") std::cout << targetId << "\n";
                } else { // ETSIの標準に基づき、CPMに含める物体を選択
                    if (!checkNewSentCpm(object.first) && 
                    !checkTimeDelta(obj) && 
                    !checkPositionDelta(obj) && 
                    !checkSpeedDelta(obj) && 
                    !checkHeadingDelta(obj)) continue;
                    else {
                        sentAllowedObjects.push_back(targetId);
                        // if (mTraciId == "136.0")  {
                        //     std::cout << targetId << ": " << obj->getVehicleData().position().x.value() << "m, " << obj->getVehicleData().position().y.value() << "m, " <<  
                        //     obj->getVehicleData().speed().value() << "cm/s, " << obj->getVehicleData().heading().value() << "deci°" << "\n";
                        // }
                    }
                }
                // }

                // if (mTraciId == "32.0" && targetId == "0.0") {
                //     std::cout << omnetpp::simTime() << "s :" << obj->getVehicleData().position().x.value() << "m, " << obj->getVehicleData().position().y.value() << "m, " <<  
                //     obj->getVehicleData().speed().value() << "cm/s, " << obj->getVehicleData().heading().value() << "deci°" << "\n";
                // }

                // CollectivePerceptionMockMessage::ObjectContainer objectContainer;
                // objectContainer.object = object.first;
                // objectContainer.objectId = tracking.traci();
                // objectContainer.sensorId = sensor.first->getId();
                // objectContainer.timeOfMeasurement = sensor.second.last();
                // objectContainer.posX = obj->getVehicleData().position().x.value();
                // objectContainer.posY = obj->getVehicleData().position().y.value();
                // objectContainer.speed = obj->getVehicleData().speed().value();
                // objectContainer.heading = obj->getVehicleData().heading().value();
                // // if (mRiskMap.find(tracking.traci()) != mRiskMap.end()) objectContainer.risk = mRiskMap[tracking.traci()];
                // // else objectContainer.risk = 0.0;
                // // std::cout << objectContainer.risk << "\n";
                // objectContainers.emplace_back(std::move(objectContainer));

                // // if (tracking.traci() == "66.0") {
                // //     std::cout << mTraciId << "send cpm\n";
                // // }
                // // 最後に送信したCPMの情報を更新
                // if (mIntervalFlag) mLastSent[targetId] = omnetpp::simTime();
                // else mLastCpm.update(obj);

                break; // 同じオブジェクトを含めないようにブレーク
            }
        }
        // if (objectContainers.size() >= 30) {
        //     // std::cout << "Number of objects included in CPM >= 35\n";
        //     break;
        // }
    }

    // 以下で候補から、実際にCPMに含める物体を選択
    // 提案手法の実装
    if (mProposedFlag) {
        sort(proposedSentAllowedObjects.begin(), proposedSentAllowedObjects.end());
        // 昇順に見て、cpmの送信車両数が0ならCPMに載せる
        for (int i = 0; i < proposedSentAllowedObjects.size(); i++) {
            if (sentObjects.size() >= mCpmContainedCnt) break;
            int cpmSourceCnt = std::get<1>(proposedSentAllowedObjects.at(i));
            std::string id = std::get<2>(proposedSentAllowedObjects.at(i));
            if (cpmSourceCnt == 0) sentObjects.insert(id);

            // if (mTraciId == "90.0") std::cout << id << ": time = " << std::get<0>(proposedSentAllowedObjects.at(i)) << ", cnt = " << cpmSourceCnt << "\n"; 
        }
        // 昇順に見て、cpmの送信車両数がK未満ならCPMに載せる
        for (int i = 0; i < proposedSentAllowedObjects.size(); i++) {
            if (sentObjects.size() >= mCpmContainedCnt) break;
            int cpmSourceCnt = std::get<1>(proposedSentAllowedObjects.at(i));
            std::string id = std::get<2>(proposedSentAllowedObjects.at(i));
            if (cpmSourceCnt < mK) sentObjects.insert(id);
            // if (mTraciId == "0.0") std::cout << id << ": time = " << std::get<0>(proposedSentAllowedObjects.at(i)) << ", cnt = " << cpmSourceCnt << "\n"; 
        }
        // まだCPMに入れられるなら、昇順に見て、格納していない物体を追加
        for (int i = 0; i < proposedSentAllowedObjects.size(); i++) {
            if (sentObjects.size() >= mCpmContainedCnt) break;
            int cpmSourceCnt = std::get<1>(proposedSentAllowedObjects.at(i));
            std::string id = std::get<2>(proposedSentAllowedObjects.at(i));
            if (sentObjects.find(id) == sentObjects.end()) sentObjects.insert(id);
            // if (mTraciId == "0.0") std::cout << id << ": time = " << std::get<0>(proposedSentAllowedObjects.at(i)) << ", cnt = " << cpmSourceCnt << "\n"; 
        }
    } else if (mOnlyCollisionTimeFlag) { // 衝突予想時刻の小さい順にCPMに含める
        sort(proposedSentAllowedObjects.begin(), proposedSentAllowedObjects.end());
        for (int i = 0; i < std::min((int) proposedSentAllowedObjects.size(), mCpmContainedCnt); i++) {
            std::string id = std::get<2>(proposedSentAllowedObjects.at(i));
            sentObjects.insert(id);
        }
    } else if (mAllFlag) { // 候補の物体をすべてCPMに含める
        for (int i = 0; i < sentAllowedObjects.size(); i++) {
            sentObjects.insert(sentAllowedObjects.at(i));
        }
    } else {
        // 条件に該当した物体数が、mCpmContainedCnt台を超える場合、ランダムに選択
        std::srand(time(NULL));
        std::mt19937_64 get_rand_mt(std::rand());
        std::shuffle(sentAllowedObjects.begin(), sentAllowedObjects.end(), get_rand_mt);
        for (int i = 0; i < std::min(mCpmContainedCnt, (int) sentAllowedObjects.size()); i++) {
            sentObjects.insert(sentAllowedObjects.at(i));
        }
    }

    // 配列sentObjectsに含まれる物体をCPMに格納
    for (const TrackedObject& object : allObjects) {
        // 各オブジェクトのトラッキング情報を見る　object.first = 物体へのポインタ、object.second = トラッキング情報
        const LocalEnvironmentModel::Tracking& tracking = object.second;
        std::shared_ptr<EnvironmentModelObject> obj = object.first.lock();
        std::string targetId = tracking.traci();
        if (obj) {
            for (const auto& sensor : tracking.sensors()) {
                // RadarSensorによる情報かどうかをチェック(CamSensorの情報は送らないようにする)
                if (mSensors.find(sensor.first) != mSensors.end()) {
                    // センサーの有効期限内にその物体を認識していなければ、スキップ
                    if (sensor.second.last() + sensor.first->getValidityPeriod() < omnetpp::simTime()) continue; 
                    // ランダムで選ばれた場合、CPMに追加
                    if (sentObjects.find(targetId) != sentObjects.end()) {
                        CollectivePerceptionMockMessage::ObjectContainer objectContainer;
                        objectContainer.object = object.first;
                        objectContainer.objectId = tracking.traci();
                        objectContainer.sensorId = sensor.first->getId();
                        objectContainer.timeOfMeasurement = sensor.second.last();
                        objectContainer.posX = obj->getVehicleData().position().x.value();
                        objectContainer.posY = obj->getVehicleData().position().y.value();
                        objectContainer.speed = obj->getVehicleData().speed().value();
                        objectContainer.heading = obj->getVehicleData().heading().value();
                        objectContainers.emplace_back(std::move(objectContainer));
                        // 最後に送信したCPMの情報を更新
                        mLastCpm.update(obj);
                        break;
                    }
                }
            }
        }
    }

    packet->addByteLength(mLengthObjectContainer * objectContainers.size());
    packet->setObjectContainers(std::move(objectContainers));
    packet->setSourceStation(mHostId);

    // if (mTraciId == "136.0") std::cout << sentObjects.size() << ", " << cpmContainedAllCnt << ", " <<sentAllowedObjects.size() << "\n";
    emit(cpmContainedCntSignal, sentObjects.size());
    emit(cpmContainedAllCntSignal, cpmContainedAllCnt);
    emit(cpmContainedEtsiCntSignal, sentAllowedObjects.size());

    // LEMの中身をプリント
    // std::cout << omnetpp::simTime() <<": " << mTraciId << "\n";
    // for (const TrackedObject& object : mEnvironmentModel->allObjects()) {
    //     const LocalEnvironmentModel::Tracking& tracking = object.second;
    //     if (tracking.expired()) {
    //         // skip objects with lost tracking
    //         continue;
    //     }
    //     // Objectのsumo idをプリント
    //     std::shared_ptr<EnvironmentModelObject> obj = object.first.lock(); 
    //     if (obj) {
    //         std::cout << "  " << obj->getExternalId() << ": ";
    //     } else {
    //         printf("expired!\n");
    //     }


    //     for (const auto& sensor : tracking.sensors()) {
    //         std::cout << sensor.first->getSensorCategory() << ":" << sensor.second.last() << "  ";    
    //     }
    // }
    // printf("\n");

    // std::cout << mTraciId << ": " << omnetpp::simTime() << ": send cpm\n";
    
    // std::cout << "Time: " << omnetpp::simTime() << ", ";
    // printf("CPM [src: %d, Byte: %d]\n", packet->getSourceStation(), packet->getBitLength());

    // std::cout << omnetpp::simTime() << "CPM " << mTraciId << "\n";
    // パケットに含まれる車両IDをチェック
    // if (mTraciId == "243.0") {
    //     std::cout << omnetpp::simTime() << " CPM [src: " << mTraciId << "]\n";
    //     for (auto objectContainer: packet->getObjectContainers()) {
    //         std::shared_ptr<EnvironmentModelObject> obj = objectContainer.object.lock(); 
    //         if (obj) {
    //             std::cout << obj->getExternalId() << " ";
    //             // round(obj->getVehicleData().position().x, vanetza::units::si::meter) << "m, " << 
    //             // round(obj->getVehicleData().speed(), centimeter_per_second) * SpeedValue_oneCentimeterPerSec << "cm/s, " <<
    //             // round(obj->getVehicleData().heading(), decidegree) << "deci°" << "\n";
    //         } else {
    //             printf("expired!\n");
    //         }
    //     }
    //     printf("\n");
    // }
    

    // cpmのフローID, 参照時刻、含まれているフローIDを確認
    // std::cout << "cpm " << mTraciId << ": "  << mVehicleDataProvider->updated() << "  ";
    //     for (auto objectContainer: packet->getObjectContainers()) {
    //     std::shared_ptr<EnvironmentModelObject> obj = objectContainer.object.lock(); 
    //     if (obj) {
    //         std::cout << obj->getExternalId() << " ";
    //     } else {
    //         printf("expired!\n");
    //     }
    // }
    // printf("\n");

    // if (mTraciId == "flow0.0") std::cout << omnetpp::simTime() << ": CPM\n";

    emit(cpmSentSignal, packet);
    emit(cpmGenerationTimeSignal, mVehicleDataProvider->updated());
    // emit(cpmSourceIdSignal, std::hash<std::string>()(mTraciId));
    emit(cpmSourceIdSignal, std::stol(mTraciId));
    for (auto objectContainer: packet->getObjectContainers()) {
        std::shared_ptr<EnvironmentModelObject> obj = objectContainer.object.lock();
        if (obj) {
            auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
            if (identity) {
                // emit(cpmContainedIdSignal, std::hash<std::string>()(identity->traci));
                emit(cpmContainedIdSignal, std::stol(identity->traci));
                // if(mTraciId == "136.0") std::cout << identity->traci << ", ";
            }
        }
       
    }
    //  if (mTraciId == "136.0") std::cout << "\n";
    request(req, packet);
}

// 各物体が、CPMで初めて送信されるかチェック
bool CollectivePerceptionMockService::checkNewSentCpm(std::weak_ptr<EnvironmentModelObject> obj) {
    return (mLastCpm.mData.find(obj) == mLastCpm.mData.end());
}

bool CollectivePerceptionMockService::checkTimeDelta(std::shared_ptr<EnvironmentModelObject> obj) {
    return (mLastCpm.mData[obj].getTime() + mTimeDelta <= omnetpp::simTime());
}

bool CollectivePerceptionMockService::checkPositionDelta(std::shared_ptr<EnvironmentModelObject> obj) {
    return (distance(mLastCpm.mData[obj].getPosition(), obj->getVehicleData().position()) > mPositionDelta);
}

bool CollectivePerceptionMockService::checkSpeedDelta(std::shared_ptr<EnvironmentModelObject> obj) {
    return abs(mLastCpm.mData[obj].getSpeed() - obj->getVehicleData().speed()) > mSpeedDelta;
}

bool CollectivePerceptionMockService::checkHeadingDelta(std::shared_ptr<EnvironmentModelObject> obj) {
    return !vanetza::facilities::similar_heading(mLastCpm.mData[obj].getHeading(), obj->getVehicleData().heading(), mHeadingDelta);
}

// ある物体について、最後にCPMに載せたデータを更新または追加する
void CollectivePerceptionMockService::LastCpm::update(std::shared_ptr<EnvironmentModelObject> obj) {
    if (obj) {
        auto it = mData.find(obj);
        if (it != mData.end()) {
            it->second.update(obj);
        } else { 
            mData.emplace(obj, Data{obj});
        }
    }
}

// 各物体について、最後にCPMに載せるデータのコンストラクタ
CollectivePerceptionMockService::Data::Data() : 
    mTime(omnetpp::simTime())
{
}

CollectivePerceptionMockService::Data::Data(std::shared_ptr<EnvironmentModelObject> obj) :
    mTime(omnetpp::simTime()), mPosition(obj->getVehicleData().position()), mSpeed(obj->getVehicleData().speed()), mHeading(obj->getVehicleData().heading())
{
}

// 各物体について、最後にCPMに載せるデータを更新
void CollectivePerceptionMockService::Data::update(std::shared_ptr<EnvironmentModelObject> obj) {
    if (obj) {
        mTime = omnetpp::simTime();
        mPosition = obj->getVehicleData().position();
        mSpeed = obj->getVehicleData().speed();
        mHeading = obj->getVehicleData().heading();
    }
}

} // namespace artery

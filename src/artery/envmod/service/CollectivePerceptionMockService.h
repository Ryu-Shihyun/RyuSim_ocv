/*
* Artery V2X Simulation Framework
* Copyright 2019 Raphael Riebl et al.
* Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
*/

#ifndef ARTERY_COLLECTIVEPERCEPTIONMOCKSERVICE_H_V08YXH9S
#define ARTERY_COLLECTIVEPERCEPTIONMOCKSERVICE_H_V08YXH9S

#include "artery/envmod/service/CollectivePerceptionMockMessage.h"
#include "artery/application/ItsG5Service.h"
#include "artery/networking/PositionProvider.h"
// #include "artery/networking/VehiclePositionProvider.h"
#include "artery/utility/IdentityRegistry.h"
#include <inet/common/ModuleAccess.h>
#include <unordered_set>
#include <vector>
#include <string> 
// 追加
#include <omnetpp/simtime.h>
#include <vanetza/units/angle.hpp>
#include <vanetza/units/velocity.hpp>

namespace artery
{
class EnvironmentModelObject; //追加
class Timer;
class VehicleDataProvider;
class IdentityRegistry; 
class GlobalEnvironmentModel;

class CollectivePerceptionMockService : public ItsG5Service
{
    public:
        // 追加
        using Object = std::weak_ptr<EnvironmentModelObject>;
        
        // 最後にcpmに載せた情報
        class Data {
            public:
                Data();
                Data(std::shared_ptr<EnvironmentModelObject> obj); // 物体を与えると、最後にcpmに載せた情報を買
                void update(std::shared_ptr<EnvironmentModelObject> obj); // 物体を与えると、最後にCPMに載せた情報を更新

                omnetpp::SimTime getTime() {return mTime;}
                Position getPosition() {return mPosition;}
                vanetza::units::Velocity getSpeed() {return mSpeed;}
                vanetza::units::Angle getHeading() {return mHeading;}

            private:
                omnetpp::SimTime mTime;
                Position mPosition;
                vanetza::units::Velocity mSpeed;
                vanetza::units::Angle mHeading;
        };

        // 各物体と最後にCPMに載せた情報のマップを保持
        class LastCpm {
            public:
                void update(std::shared_ptr<EnvironmentModelObject> obj); //物体を与えると、その物体の最後にCPMに載せた情報を追加または更新
                std::map<Object, Data, std::owner_less<Object>> mData;
        };

        virtual ~CollectivePerceptionMockService();

    protected:
        int numInitStages() const override;
        void initialize(int stage) override;
        void trigger() override;
        void handleMessage(omnetpp::cMessage*) override;
        void receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t, omnetpp::cObject*, omnetpp::cObject*) override;
        void generatePacket();
        void indicate(const vanetza::btp::DataIndication&, omnetpp::cPacket*) override;

        // 物体をCPMに含めるかどうかをチェックする条件
        bool checkNewSentCpm(Object obj);
        bool checkTimeDelta(std::shared_ptr<EnvironmentModelObject> obj);
        bool checkPositionDelta(std::shared_ptr<EnvironmentModelObject> obj);
        bool checkSpeedDelta(std::shared_ptr<EnvironmentModelObject> obj);
        bool checkHeadingDelta(std::shared_ptr<EnvironmentModelObject> obj);

    private:
        int mHostId = 0; // Omnet++のモジュールid
        std::string mTraciId; // 追加　sumoの車両id
        const PositionProvider* mPositionProvider = nullptr;
        const Timer* mTimer = nullptr;
        const VehicleDataProvider* mVehicleDataProvider = nullptr;
        // const VehiclePositionProvider* mVehiclePositionProvider = nullptr;
        const LocalEnvironmentModel* mEnvironmentModel = nullptr;
        IdentityRegistry* mIdentityRegistry;
        GlobalEnvironmentModel* mGlobalEnvironmentModel;

        omnetpp::cMessage* mTrigger = nullptr;
        bool mGenerateAfterCam;
        omnetpp::SimTime mCpmOffset;
        omnetpp::SimTime mCpmInterval;
        omnetpp::SimTime mFovInterval = omnetpp::SimTime::ZERO;
        omnetpp::SimTime mFovLast = omnetpp::SimTime::ZERO;
        std::vector<CollectivePerceptionMockMessage::FovContainer> mFovContainers;
        std::unordered_set<const Sensor*> mSensors; //車両に搭載しているセンサの集合
        unsigned mDccProfile = 0;
        unsigned mLengthHeader = 0;
        unsigned mLengthFovContainer = 0;
        unsigned mLengthObjectContainer = 0;
        bool mDccRestriction;
        
        // 物体ごとに、最後にCPMに載せた時間、位置、速度、進行方向を保存する
        LastCpm mLastCpm; 
        
        omnetpp::SimTime mTimeDelta;
        vanetza::units::Angle mHeadingDelta;
		vanetza::units::Length mPositionDelta;
		vanetza::units::Velocity mSpeedDelta;

        // シミュレーション結果のログを取る範囲
        double mLowerPosX;
        double mUpperPosX;
        double mLowerPosY;
        double mUpperPosY;

        // 各クラスの送信間隔
        // bool mIntervalFlag;
        // omnetpp::SimTime mIntervalC0;
        // omnetpp::SimTime mIntervalC1;
        // omnetpp::SimTime mChangeInterval;
        // omnetpp::SimTime mLastChanged;
        // int mAllowedSentNum;
        // omnetpp::SimTime mFirstSent;
        
        int mCpmContainedCnt;
        bool mProposedFlag;
        bool mRandomFlag;
        bool mOnlyCollisionTimeFlag;
        bool mAllFlag;
        int mK;
        
        // 各車両の送信間隔
        std::map<std::string, omnetpp::SimTime> mIntervals;
        // 各車両の最後に送信した時刻
        std::map<std::string, omnetpp::SimTime> mLastSent;
        // 各車両の危険度を保存
        // std::map<std::string, double> mRiskMap;
        
        // シグナル変数を宣言
        omnetpp::simsignal_t cpmGenerationTimeSignal;
        omnetpp::simsignal_t cpmSourceIdSignal;
        omnetpp::simsignal_t cpmContainedIdSignal;
        
        omnetpp::simsignal_t cpmContainedCntSignal;
        omnetpp::simsignal_t cpmContainedAllCntSignal;
        omnetpp::simsignal_t cpmContainedEtsiCntSignal;

        // omnetpp::simsignal_t objectPerceptionSignal; // 各物体について認識の有無を送信するシグナル
        // omnetpp::simsignal_t objectDistanceSignal; // 全物体との距離を送るシグナル
        omnetpp::simsignal_t aoiSignal; // 認識している物体についてAoIを送信するシグナル
        omnetpp::simsignal_t perceptedObjectDistanceSignal; // 認識している物体との距離を送信するシグナル
        omnetpp::simsignal_t cpmReceivedCountSignal;
        omnetpp::simsignal_t perceptedObjectReletiveVelocitySignal; // 認識している物体との相対速度を送信するシグナル
        omnetpp::simsignal_t riskClassSignal; // 認識している物体との危険度クラス
        omnetpp::simsignal_t collisionTimeSignal;
        omnetpp::simsignal_t perceptedVelocitySignal;
        omnetpp::simsignal_t perceptedAccelerationSignal;
        omnetpp::simsignal_t perceptedYawrateSignal;
        
        omnetpp::simsignal_t posErrorSignal;
        omnetpp::simsignal_t speedErrorSignal;
        omnetpp::simsignal_t headingErrorSignal;
        omnetpp::simsignal_t estimatedPosErrorSignal;
        omnetpp::simsignal_t receivedRiskSignal;
        
        // 危険度クラスに関するシグナル
        omnetpp::simsignal_t riskClass;
        omnetpp::simsignal_t riskDistance;
        omnetpp::simsignal_t riskReletiveVelocity;

        // 危険度に関するシグナル
        // omnetpp::simsignal_t riskSignal;
        // omnetpp::simsignal_t riskPosXSignal;
        // omnetpp::simsignal_t riskPosYSignal;
        // omnetpp::simsignal_t riskSpeedSignal;
        // omnetpp::simsignal_t riskHeadingSignal;
        // omnetpp::simsignal_t riskAccelerationSignal;
        // omnetpp::simsignal_t riskYawrateSignal;

};

} // namespace artery

#endif /* ARTERY_COLLECTIVEPERCEPTIONMOCKSERVICE_H_V08YXH9S */

/*
 * Artery V2X Simulation Framework
 * Copyright 2014-2017 Hendrik-Joern Guenther, Raphael Riebl, Oliver Trauer
 * Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
 */

#include "artery/envmod/sensor/CpmSensor.h"
#include "artery/envmod/GlobalEnvironmentModel.h"
#include "artery/envmod/LocalEnvironmentModel.h"
#include "artery/envmod/service/CollectivePerceptionMockMessage.h"
#include "artery/application/Middleware.h"
#include "artery/utility/IdentityRegistry.h"
#include <inet/common/ModuleAccess.h>
#include <string>

using namespace omnetpp;

namespace artery
{

static const simsignal_t CpmReceivedSignal = cComponent::registerSignal("CpmReceived");

Define_Module(CpmSensor);

void CpmSensor::initialize()
{
    BaseSensor::initialize();
    mIdentityRegistry = inet::getModuleFromPar<IdentityRegistry>(par("identityRegistryModule"), this);
    getMiddleware().subscribe(CpmReceivedSignal, this);

    // 追加 sumoのIDを取得
	mTraciId = getFacilities().get_const<Identity>().traci; 
    mTimer = &getFacilities().get_const<Timer>();
    mReceiveCount = 0;

    cpmReceivedGenerationTimeSignal = registerSignal("cpmReceivedGenerationTime");
    cpmReceivedSourceIdSignal = registerSignal("cpmReceivedSourceId");
    cpmReceivedContainedIdSignal = registerSignal("cpmReceivedContainedId");
}

void CpmSensor::finish()
{
    // std::cout << mTraciId << ": " << mReceiveCount << "\n";
    getMiddleware().unsubscribe(CpmReceivedSignal, this);
    BaseSensor::finish();
}

void CpmSensor::measurement()
{
    Enter_Method("measurement");
}

void CpmSensor::receiveSignal(cComponent*, simsignal_t signal, cObject *obj, cObject*)
{   
    if (signal == CpmReceivedSignal) {
        auto* cpm = dynamic_cast<CollectivePerceptionMockMessage*>(obj);
        if (cpm) {
            SensorDetection detection;
            std::string traciId = cpm->getTraciId();
            auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(traciId);
            if (identity) {
                // 受信したCPMの送信元とメッセージIDをプリント
                // std::cout << "cpm " << mTraciId << " received from " << identity->traci << "\n";        
                // sumoのIDを使用して、グローバル環境モデルからCPMの送信元のオブジェクトを獲得
                auto object = mGlobalEnvironmentModel->getObject(identity->traci);
                auto measurement = mTimer->getTimeFor(mTimer->reconstructMilliseconds(cpm->getGenerationDeltaTime()));
                detection.objects.push_back(object);
                detection.measurements.push_back(measurement);
                detection.posXs.push_back(cpm->getPosX());
                detection.posYs.push_back(cpm->getPosY());
                detection.speeds.push_back(cpm->getSpeed());
                detection.headings.push_back(cpm->getHeading());
                // detection.risks.push_back(-1);
                // std::cout << "  cpm " << mTraciId << " received from " << identity->traci << ", " << measurement << "\n";    
                // std::cout << mTraciId << ": " << omnetpp::simTime() << " receive cpm\n";

                emit(cpmReceivedGenerationTimeSignal, measurement);
                // emit(cpmReceivedSourceIdSignal, std::hash<std::string>()(identity->traci));
                emit(cpmReceivedSourceIdSignal, std::stol(identity->traci));
            } else {
                EV_WARN << "Unknown identity for station ID " << traciId;
            }

            // CPMに含まれるオブジェクトをdetectionに追加
            for (auto objectContainer: cpm->getObjectContainers()) {
                auto object = objectContainer.object;
                std::shared_ptr<EnvironmentModelObject> obj = object.lock(); 
                if (obj) {
                    auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
                    if (identity) {
                         // オブジェクトが自車両ならスキップ
                        if (identity->traci == mTraciId) continue;
                        omnetpp::SimTime measurement = objectContainer.timeOfMeasurement;
                        detection.objects.push_back(obj);
                        detection.measurements.push_back(measurement);
                        detection.posXs.push_back(objectContainer.posX);
                        detection.posYs.push_back(objectContainer.posY);
                        detection.speeds.push_back(objectContainer.speed);
                        detection.headings.push_back(objectContainer.heading);
                        // detection.risks.push_back(objectContainer.risk);
                        // std::cout << obj->getExternalId() << " " << detection.risks.back() << "\n";
                        // emit(cpmReceivedContainedIdSignal, std::hash<std::string>()(identity->traci));
                        emit(cpmReceivedContainedIdSignal, std::stol(identity->traci));
                    }
                }
            }

            // sensingIdContainerコンテナが含まれている場合
            // if (mTraciId == "32.0" && traciId == "0.0") std::cout << mTraciId << " received sensingIdContainers from " << traciId << "\n";
            
            // if (mTraciId == "32.0" && traciId == "0.0") std::cout << "\n";

            // std::cout << "\n";
            mLocalEnvironmentModel->complementObjects(detection, *this, traciId);
            mReceiveCount++;

            // CPMに含まれるセンシング情報を取得
            // if (mTraciId =="32.0" && traciId == "0.0") std::cout << mTraciId << ": rcv Sensing Information from " << traciId << "\n";
            if (identity) {
                auto sourceObject = mGlobalEnvironmentModel->getObject(identity->traci);
                std::vector<std::string> sensingIds;
                std::vector<std::shared_ptr<EnvironmentModelObject>> objects;
                for (auto sensingIdContainer: cpm->getSensingIdContainers()) {
                    std::string traci = sensingIdContainer.objectId;
                    std::shared_ptr<EnvironmentModelObject> obj = sensingIdContainer.object.lock(); 
                    if (obj) {
                        auto identity = mIdentityRegistry->lookup<IdentityRegistry::traci>(obj->getExternalId());
                        if (identity) {
                            sensingIds.emplace_back(traci);
                            objects.push_back(obj);
                            // if (mTraciId == "32.0" && traciId == "0.0") std::cout <<  " " << traci << ", ";
                        }
                    }     
                    // if (mTraciId == "32.0" && traciId == "0.0") std::cout << "  " << traci << ", ";
                }
                // if (mTraciId == "32.0" && traciId == "0.0") std::cout << "\n";
                mLocalEnvironmentModel->complementSensingIds(traciId, sourceObject, sensingIds, objects);
            }
        }  
    } else {
        EV_ERROR << "received signal has no CollectivePerceptionMockMessage";
    }
    
}

omnetpp::SimTime CpmSensor::getValidityPeriod() const
{
    return omnetpp::SimTime { 1100, SIMTIME_MS };
    // return mValidityPeriod; // 追加
}

const std::string& CpmSensor::getSensorCategory() const
{
    static const std::string category = "CP";
    return category;
}
} // namespace artery

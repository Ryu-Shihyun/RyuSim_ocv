/*
 * Artery V2X Simulation Framework
 * Copyright 2014-2017 Hendrik-Joern Guenther, Raphael Riebl, Oliver Trauer
 * Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
 */

#ifndef ENVMOD_CAMSENSOR_H_
#define ENVMOD_CAMSENSOR_H_

#include "artery/envmod/sensor/BaseSensor.h"
#include <omnetpp/clistener.h>
#include <string>

namespace artery
{

class IdentityRegistry;
class Timer;

class CpmSensor : public BaseSensor, public omnetpp::cListener
{
public:
    void measurement() override;
    void receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t, omnetpp::cObject*, omnetpp::cObject* = nullptr) override;
    void setVisualization(const SensorVisualizationConfig&) override {}
    const FieldOfView* getFieldOfView() const override { return nullptr; }
    omnetpp::SimTime getValidityPeriod() const override;
    SensorPosition position() const override { return SensorPosition::VIRTUAL; }
    const std::string& getSensorCategory() const override;

    std::string mTraciId; // 追加 sumoのID
    int mReceiveCount; //追加 受信したcpm数

protected:
    void initialize() override;
    void finish() override;

private:
    IdentityRegistry* mIdentityRegistry;
    const Timer* mTimer;

    // シグナル変数を宣言
    omnetpp::simsignal_t cpmReceivedGenerationTimeSignal;
    omnetpp::simsignal_t cpmReceivedSourceIdSignal;
    omnetpp::simsignal_t cpmReceivedContainedIdSignal;
};

} // namespace artery

#endif /* ENVMOD_CAMSENSOR_H_ */

#ifndef ARTERY_VEHICLEPOSITIONPROVIDER_H_NNR8FIJ5
#define ARTERY_VEHICLEPOSITIONPROVIDER_H_NNR8FIJ5

#include "artery/networking/PositionFixObject.h"
#include <omnetpp/clistener.h>
#include <omnetpp/csimplemodule.h>
#include <vanetza/common/position_provider.hpp>
// #include "artery/networking/PositionProvider.h" //added by ryu
namespace traci { class VehicleController; }

namespace artery
{

class Runtime;

class VehiclePositionProvider :
    public omnetpp::cSimpleModule, public omnetpp::cListener,
    public vanetza::PositionProvider
{
    public:
        // cSimpleModule
        void initialize(int stage) override;
        int numInitStages() const override;

        // cListener
        void receiveSignal(omnetpp::cComponent*, omnetpp::simsignal_t, omnetpp::cObject*, omnetpp::cObject*) override;
         // 追加
        // PositionProvider
        // Position getCartesianPosition() const override;
        // GeoPosition getGeodeticPosition() const override;

        // PositionProvider
        const vanetza::PositionFix& position_fix() override { return mPositionFix; }

    private:
        void updatePosition();

        PositionFixObject mPositionFix;
        Runtime* mRuntime = nullptr;
        traci::VehicleController* mVehicleController = nullptr;
};

} // namespace artery

#endif /* ARTERY_VEHICLEPOSITIONPROVIDER_H_NNR8FIJ5 */


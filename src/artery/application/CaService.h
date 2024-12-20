/*
* Artery V2X Simulation Framework
* Copyright 2014-2019 Raphael Riebl et al.
* Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
*/

#ifndef ARTERY_CASERVICE_H_
#define ARTERY_CASERVICE_H_

#include "artery/application/ItsG5BaseService.h"
#include "artery/utility/Channel.h"
#include "artery/utility/Geometry.h"
#include <vanetza/asn1/cam.hpp>
#include <vanetza/btp/data_interface.hpp>
#include <vanetza/units/angle.hpp>
#include <vanetza/units/velocity.hpp>
#include <omnetpp/simtime.h>

namespace artery
{

class NetworkInterfaceTable;
class Timer;
class VehicleDataProvider;

class CaService : public ItsG5BaseService
{
	public:
		CaService();
		void initialize() override;
		void indicate(const vanetza::btp::DataIndication&, std::unique_ptr<vanetza::UpPacket>) override;
		void trigger() override;

	private:
		void checkTriggeringConditions(const omnetpp::SimTime&);
		bool checkHeadingDelta(const omnetpp::SimTime&) ;
		bool checkPositionDelta(const omnetpp::SimTime&) ;
		bool checkSpeedDelta(const omnetpp::SimTime&);
		void sendCam(const omnetpp::SimTime&);
		omnetpp::SimTime genCamDcc();

		ChannelNumber mPrimaryChannel = channel::CCH;
		const NetworkInterfaceTable* mNetworkInterfaceTable = nullptr;
		const VehicleDataProvider* mVehicleDataProvider = nullptr;
		const Timer* mTimer = nullptr;
		LocalDynamicMap* mLocalDynamicMap = nullptr;

		omnetpp::SimTime mGenCamMin;
		omnetpp::SimTime mGenCamMax;
		omnetpp::SimTime mGenCam;
		omnetpp::SimTime mExponentialMean;
		omnetpp::SimTime mGenCamNonPeriodic;
		unsigned mGenCamLowDynamicsCounter;
		unsigned mGenCamLowDynamicsLimit;
		Position mLastCamPosition;
		vanetza::units::Velocity mLastCamSpeed;
		vanetza::units::Angle mLastCamHeading;
		omnetpp::SimTime mLastCamTimestamp;
		omnetpp::SimTime mLastLowCamTimestamp;
		vanetza::units::Angle mHeadingDelta;
		vanetza::units::Length mPositionDelta;
		vanetza::units::Velocity mSpeedDelta;
		bool mDccRestriction;
		bool mFixedRate;
		bool mExponentialNonPeriodic;
        omnetpp::SimTime startUpTime;
		//ryu test
		void updateCSVWithIndex(std::string& ,  uint32_t id, bool isChange);
		bool calculateTChange();
	private:
		//ryu test
		omnetpp::simsignal_t scSignalCamReceived;
		omnetpp::simsignal_t scSignalCamReceivedID;
		omnetpp::simsignal_t scSignalCamSent;
		omnetpp::simsignal_t camSentHead;
        omnetpp::simsignal_t camSentPositionX;
        omnetpp::simsignal_t camSentPositionY;
        omnetpp::simsignal_t camSentSpeed;
        omnetpp::simsignal_t camTriggerHead;
        omnetpp::simsignal_t camTriggerPosition;
        omnetpp::simsignal_t camTriggerSpeed;
		omnetpp::simsignal_t camVehicleId;

		double camTriggerHead_;

};

vanetza::asn1::Cam createCooperativeAwarenessMessage(const VehicleDataProvider&, uint16_t genDeltaTime);
void addLowFrequencyContainer(vanetza::asn1::Cam&);

} // namespace artery

#endif /* ARTERY_CASERVICE_H_ */

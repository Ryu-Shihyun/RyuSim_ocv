/*
* Artery V2X Simulation Framework
* Copyright 2014-2019 Raphael Riebl et al.
* Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
*/

#include "artery/application/CaObject.h"
#include "artery/application/CaService.h"
#include "artery/application/Asn1PacketVisitor.h"
#include "artery/application/MultiChannelPolicy.h"
#include "artery/application/VehicleDataProvider.h"
#include "artery/utility/simtime_cast.h"
#include "veins/base/utils/Coord.h"
#include <boost/units/cmath.hpp>
#include <boost/units/systems/si/prefixes.hpp>
#include <omnetpp/cexception.h>
#include <vanetza/btp/ports.hpp>
#include <vanetza/dcc/transmission.hpp>
#include <vanetza/dcc/transmit_rate_control.hpp>
#include <vanetza/facilities/cam_functions.hpp>
#include <chrono>
//added by ryu
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <unordered_map>


namespace artery
{

using namespace omnetpp;

auto microdegree = vanetza::units::degree * boost::units::si::micro;
auto decidegree = vanetza::units::degree * boost::units::si::deci;
auto degree_per_second = vanetza::units::degree / vanetza::units::si::second;
auto centimeter_per_second = vanetza::units::si::meter_per_second * boost::units::si::centi;

// static const simsignal_t scSignalCamReceived = cComponent::registerSignal("CamReceived");
// static const simsignal_t scSignalCamSent = cComponent::registerSignal("CamSent");
static const auto scLowFrequencyContainerInterval = std::chrono::milliseconds(500);


template<typename T, typename U>
long round(const boost::units::quantity<T>& q, const U& u)
{
	boost::units::quantity<U> v { q };
	return std::round(v.value());
}


Define_Module(CaService)

CaService::CaService() :
		mGenCamMin { 100, SIMTIME_MS },
		mExponentialMean { 50, SIMTIME_MS },
		mGenCamMax { 1000, SIMTIME_MS },
		mGenCam(mGenCamMax),
		mGenCamLowDynamicsCounter(0),
		mGenCamLowDynamicsLimit(3)
{
}

void CaService::initialize()
{
	ItsG5BaseService::initialize();
	mNetworkInterfaceTable = &getFacilities().get_const<NetworkInterfaceTable>();
	mVehicleDataProvider = &getFacilities().get_const<VehicleDataProvider>();
	mTimer = &getFacilities().get_const<Timer>();
	mLocalDynamicMap = &getFacilities().get_mutable<artery::LocalDynamicMap>();

	// avoid unreasonable high elapsed time values for newly inserted vehicles
	mLastCamTimestamp = simTime();

    double delay = 0.001 * intuniform(0, 1000, 0);
    startUpTime = simTime() + delay;

	// first generated CAM shall include the low frequency container
	mLastLowCamTimestamp = mLastCamTimestamp - artery::simtime_cast(scLowFrequencyContainerInterval);

	// generation rate boundaries
	mGenCamMin = par("minInterval");
	mGenCamMax = par("maxInterval");

	// vehicle dynamics thresholds
	mHeadingDelta = vanetza::units::Angle { par("headingDelta").doubleValue() * vanetza::units::degree };
	mPositionDelta = par("positionDelta").doubleValue() * vanetza::units::si::meter;
	mSpeedDelta = par("speedDelta").doubleValue() * vanetza::units::si::meter_per_second;

	mDccRestriction = par("withDccRestriction");
	mFixedRate = par("fixedRate");
    mExponentialNonPeriodic = par( "exponentialNonPeriodic");
    mExponentialMean = par("exponentialMean");
    mGenCamNonPeriodic = mGenCamMin + exponential(mExponentialMean);

	// look up primary channel for CA
	ChannelNumber mPrimaryChannel = getFacilities().get_const<MultiChannelPolicy>().primaryChannel(vanetza::aid::CA);
	
	//ryu test
	scSignalCamReceived = cComponent::registerSignal("CamReceived");
	scSignalCamReceivedID = cComponent::registerSignal("CamReceivedID");
	scSignalCamSent = cComponent::registerSignal("CamSent");
	camSentHead = cComponent::registerSignal("camSentHead");
	camSentPositionX = cComponent::registerSignal("camSentPositionX");
	camSentPositionY = cComponent::registerSignal("camSentPositionY");
	camSentSpeed = cComponent::registerSignal("camSentSpeed");
	camTriggerHead = cComponent::registerSignal("camTriggerHead");
	camTriggerPosition = cComponent::registerSignal("camTriggerPosition");
	camTriggerSpeed = cComponent::registerSignal("camSentHead");
	camVehicleId = cComponent::registerSignal("camVehicleId");

	camTriggerHead_ = 0;
	
}

void CaService::trigger()
{
	Enter_Method("trigger");
	checkTriggeringConditions(simTime());
}

void CaService::indicate(const vanetza::btp::DataIndication& ind, std::unique_ptr<vanetza::UpPacket> packet)
{
	Enter_Method("indicate");

	Asn1PacketVisitor<vanetza::asn1::Cam> visitor;
	const vanetza::asn1::Cam* cam = boost::apply_visitor(visitor, *packet);
	if (cam && cam->validate()) {
		CaObject obj = visitor.shared_wrapper;
		omnetpp::SimTime t = mLocalDynamicMap->getTime(obj);
		double diff = omnetpp::simTime().dbl() - t.dbl();
		emit(scSignalCamReceived, diff);
		ItsPduHeader_t& header = cam->m_struct->header;
		emit(scSignalCamReceivedID, header.stationID);
		// std::cout << header.stationID << std::endl;
		mLocalDynamicMap->updateAwareness(obj);
	}
}

void CaService::checkTriggeringConditions(const SimTime& T_now)
{
	// provide variables named like in EN 302 637-2 V1.3.2 (section 6.1.3)
	SimTime& T_GenCam = mGenCam;
	const SimTime& T_GenCamMin = mGenCamMin;
	const SimTime& T_GenCamMax = mGenCamMax;
	const SimTime& T_GenCamNonPeriodic = mGenCamNonPeriodic;
    const SimTime& T_GenCamDcc = genCamDcc();

    SimTime T_GenCamFinal = T_GenCamMin;
	if (mDccRestriction) {
        T_GenCamFinal = T_GenCamDcc;
    } else if (mExponentialNonPeriodic) {
        T_GenCamFinal = T_GenCamNonPeriodic;
        // Need to update the time for next sending
        mGenCamNonPeriodic = mGenCamMin + exponential(mExponentialMean, 0);
	}

	const SimTime T_elapsed = T_now - mLastCamTimestamp;

	// 外部ファイルを作成
	std::string parameter_str = "parameter.data";
	
	if (T_elapsed >= T_GenCamFinal & T_now > startUpTime) {
		if (mFixedRate || mExponentialNonPeriodic) {
			sendCam(T_now);
			updateCSVWithIndex(parameter_str,mVehicleDataProvider->station_id(),calculateTChange());
			
		}  else if (checkHeadingDelta(T_now) || checkPositionDelta(T_now) || checkSpeedDelta(T_now)) {
			sendCam(T_now);
			T_GenCam = std::min(T_elapsed, T_GenCamMax); /*< if middleware update interval is too long */
			mGenCamLowDynamicsCounter = 0;
			updateCSVWithIndex(parameter_str,mVehicleDataProvider->station_id(),calculateTChange());
			
		} else if (T_elapsed >= T_GenCam) {
			sendCam(T_now);
			updateCSVWithIndex(parameter_str,mVehicleDataProvider->station_id(),calculateTChange());

			if (++mGenCamLowDynamicsCounter >= mGenCamLowDynamicsLimit) {
				T_GenCam = T_GenCamMax;
			}
		}
	}
}

bool CaService::checkHeadingDelta(const SimTime& T_now) 
{
	//start::ryu
	// std::cout << "check heading delta\n";
	if(!vanetza::facilities::similar_heading(mLastCamHeading, mVehicleDataProvider->heading(), mHeadingDelta)){
		// std::string csv_file_path = "data/headingDelta.csv";
		// std::ofstream ofs;
		// ofs.open(csv_file_path,std::ios::app);
		// ofs << T_now.format(-9)<< "," << mVehicleDataProvider->station_id() << "," <<mLastCamHeading.value() << "," << mVehicleDataProvider->heading().value() <<","<< mHeadingDelta.value() << std::endl;
		// ofs.close();	
		camTriggerHead_ = mVehicleDataProvider->heading().value();
		emit(camTriggerHead,camTriggerHead_,nullptr);
	}
	//end::ryu
	return !vanetza::facilities::similar_heading(mLastCamHeading, mVehicleDataProvider->heading(), mHeadingDelta);
}

bool CaService::checkPositionDelta(const SimTime& T_now) 
{
	// std::cout << "check heading delta\n";
	if(distance(mLastCamPosition, mVehicleDataProvider->position()) > mPositionDelta){
		// std::string csv_file_path = "data/positionDelta.csv";
		// std::ofstream ofs;
		// ofs.open(csv_file_path,std::ios::app);
		// ofs << T_now.format(-9)<< "," << mVehicleDataProvider->station_id() << "," <<mLastCamPosition.x.value() << "," <<mLastCamPosition.y.value()  << ","<< mVehicleDataProvider->position().x.value() <<","<< mVehicleDataProvider->position().y.value()<< "," << mPositionDelta.value() << std::endl;
		// ofs.close();
		emit(camTriggerPosition,distance(mLastCamPosition, mVehicleDataProvider->position()).value(),nullptr);
	}
	//end::ryu
	return (distance(mLastCamPosition, mVehicleDataProvider->position()) > mPositionDelta);
}

bool CaService::checkSpeedDelta(const SimTime& T_now) 
{
	//start::ryu
	// std::cout << "check heading delta\n";
	if(abs(mLastCamSpeed - mVehicleDataProvider->speed()) > mSpeedDelta){
		// std::string csv_file_path = "data/speedDelta.csv";
		// std::ofstream ofs;
		// ofs.open(csv_file_path,std::ios::app);
		// ofs << T_now.format(-9)<< "," << mVehicleDataProvider->station_id() << "," <<mLastCamSpeed.value() << "," << mVehicleDataProvider->speed().value() <<","<< mSpeedDelta.value() << std::endl;
		// ofs.close();
		emit(camTriggerSpeed,abs(mLastCamSpeed - mVehicleDataProvider->speed()).value(),nullptr);

	}
	//end::ryu
	return abs(mLastCamSpeed - mVehicleDataProvider->speed()) > mSpeedDelta;
}

void CaService::sendCam(const SimTime& T_now)
{
	uint16_t genDeltaTimeMod = countTaiMilliseconds(mTimer->getTimeFor(mVehicleDataProvider->updated()));
	auto cam = createCooperativeAwarenessMessage(*mVehicleDataProvider, genDeltaTimeMod);
	//start ryu
	// std::string csv_file_path = "data/camTimeStamp.csv";
	// std::ofstream ofs;
	// ofs.open(csv_file_path,std::ios::app);
	
	emit(camVehicleId,mVehicleDataProvider->station_id(),	nullptr);
	//end ryu
	mLastCamPosition = mVehicleDataProvider->position();
	mLastCamSpeed = mVehicleDataProvider->speed();
	mLastCamHeading = mVehicleDataProvider->heading();
	mLastCamTimestamp = T_now;
	if (T_now - mLastLowCamTimestamp >= artery::simtime_cast(scLowFrequencyContainerInterval)) {
		addLowFrequencyContainer(cam);
		mLastLowCamTimestamp = T_now;
	}

	using namespace vanetza;
	btp::DataRequestB request;
	request.destination_port = btp::ports::CAM;
	request.gn.its_aid = aid::CA;
	request.gn.transport_type = geonet::TransportType::SHB;
	request.gn.maximum_lifetime = geonet::Lifetime { geonet::Lifetime::Base::One_Second, 1 };
	request.gn.traffic_class.tc_id(static_cast<unsigned>(dcc::Profile::DP2));
	request.gn.communication_profile = geonet::CommunicationProfile::ITS_G5;

	CaObject obj(std::move(cam));
	// emit(scSignalCamSent, &obj);

	using CamByteBuffer = convertible::byte_buffer_impl<asn1::Cam>;
	std::unique_ptr<geonet::DownPacket> payload { new geonet::DownPacket() };
	std::unique_ptr<convertible::byte_buffer> buffer { new CamByteBuffer(obj.shared_ptr()) };
	payload->layer(OsiLayer::Application) = std::move(buffer);
	// ofs << T_now.format(-9)<< "," << mVehicleDataProvider->station_id() << "," << payload->size() << ","<< mVehicleDataProvider->position().x.value() <<","<< mVehicleDataProvider->position().y.value() << "," << mVehicleDataProvider->heading().value()<< "," << mVehicleDataProvider->speed().value() << std::endl;
	// ofs.close();
	//start ryu
	emit(camSentHead,mVehicleDataProvider->heading().value(),nullptr);
	emit(camSentPositionX,mVehicleDataProvider->position().x.value(),nullptr);
	emit(camSentPositionY,mVehicleDataProvider->position().y.value(),nullptr);
	emit(camSentSpeed,mVehicleDataProvider->speed().value(),nullptr);
	
	
	//T_changeを出力する関数を呼び出す
	// parameter.dataに書き込み
	//end ryu
	this->request(request, std::move(payload), mNetworkInterfaceTable->select(0).get());
}

SimTime CaService::genCamDcc()
{
	// network interface may not be ready yet during initialization, so look it up at this later point
	auto netifc = mNetworkInterfaceTable->select(mPrimaryChannel);
	vanetza::dcc::TransmitRateThrottle* trc = netifc ? netifc->getDccEntity().getTransmitRateThrottle() : nullptr;
	if (!trc) {
		throw cRuntimeError("No DCC TRC found for CA's primary channel %i", mPrimaryChannel);
	}

	static const vanetza::dcc::TransmissionLite ca_tx(vanetza::dcc::Profile::DP2, 0);
	vanetza::Clock::duration delay = trc->delay(ca_tx);
	SimTime dcc { std::chrono::duration_cast<std::chrono::milliseconds>(delay).count(), SIMTIME_MS };
	return std::min(mGenCamMax, std::max(mGenCamMin, dcc));
}

vanetza::asn1::Cam createCooperativeAwarenessMessage(const VehicleDataProvider& vdp, uint16_t genDeltaTime)
{
	vanetza::asn1::Cam message;

	ItsPduHeader_t& header = (*message).header;
	header.protocolVersion = 1;
	header.messageID = ItsPduHeader__messageID_cam;
	header.stationID = vdp.station_id();

	CoopAwareness_t& cam = (*message).cam;
	cam.generationDeltaTime = genDeltaTime * GenerationDeltaTime_oneMilliSec;
	BasicContainer_t& basic = cam.camParameters.basicContainer;
	HighFrequencyContainer_t& hfc = cam.camParameters.highFrequencyContainer;

	basic.stationType = StationType_passengerCar;
	basic.referencePosition.altitude.altitudeValue = AltitudeValue_unavailable;
	basic.referencePosition.altitude.altitudeConfidence = AltitudeConfidence_unavailable;
	basic.referencePosition.longitude = round(vdp.longitude(), microdegree) * Longitude_oneMicrodegreeEast;
	basic.referencePosition.latitude = round(vdp.latitude(), microdegree) * Latitude_oneMicrodegreeNorth;
	basic.referencePosition.positionConfidenceEllipse.semiMajorOrientation = HeadingValue_unavailable;
	basic.referencePosition.positionConfidenceEllipse.semiMajorConfidence =
			SemiAxisLength_unavailable;
	basic.referencePosition.positionConfidenceEllipse.semiMinorConfidence =
			SemiAxisLength_unavailable;

	hfc.present = HighFrequencyContainer_PR_basicVehicleContainerHighFrequency;
	BasicVehicleContainerHighFrequency& bvc = hfc.choice.basicVehicleContainerHighFrequency;
	bvc.heading.headingValue = round(vdp.heading(), decidegree);
	bvc.heading.headingConfidence = HeadingConfidence_equalOrWithinOneDegree;
	bvc.speed.speedValue = round(vdp.speed(), centimeter_per_second) * SpeedValue_oneCentimeterPerSec;
	bvc.speed.speedConfidence = SpeedConfidence_equalOrWithinOneCentimeterPerSec * 3;
	bvc.driveDirection = vdp.speed().value() >= 0.0 ?
			DriveDirection_forward : DriveDirection_backward;
	const double lonAccelValue = vdp.acceleration() / vanetza::units::si::meter_per_second_squared;
	// extreme speed changes can occur when SUMO swaps vehicles between lanes (speed is swapped as well)
	if (lonAccelValue >= -160.0 && lonAccelValue <= 161.0) {
		bvc.longitudinalAcceleration.longitudinalAccelerationValue = lonAccelValue * LongitudinalAccelerationValue_pointOneMeterPerSecSquaredForward;
	} else {
		bvc.longitudinalAcceleration.longitudinalAccelerationValue = LongitudinalAccelerationValue_unavailable;
	}
	bvc.longitudinalAcceleration.longitudinalAccelerationConfidence = AccelerationConfidence_unavailable;
	bvc.curvature.curvatureValue = abs(vdp.curvature() / vanetza::units::reciprocal_metre) * 10000.0;
	if (bvc.curvature.curvatureValue >= 1023) {
		bvc.curvature.curvatureValue = 1023;
	}
	bvc.curvature.curvatureConfidence = CurvatureConfidence_unavailable;
	bvc.curvatureCalculationMode = CurvatureCalculationMode_yawRateUsed;
	bvc.yawRate.yawRateValue = round(vdp.yaw_rate(), degree_per_second) * YawRateValue_degSec_000_01ToLeft * 100.0;
	if (abs(bvc.yawRate.yawRateValue) >= YawRateValue_unavailable) {
		bvc.yawRate.yawRateValue = YawRateValue_unavailable;
	}
	bvc.vehicleLength.vehicleLengthValue = VehicleLengthValue_unavailable;
	bvc.vehicleLength.vehicleLengthConfidenceIndication =
			VehicleLengthConfidenceIndication_noTrailerPresent;
	bvc.vehicleWidth = VehicleWidth_unavailable;

	std::string error;
	if (!message.validate(error)) {
		throw cRuntimeError("Invalid High Frequency CAM: %s", error.c_str());
	}

	return message;
}

void addLowFrequencyContainer(vanetza::asn1::Cam& message)
{
	LowFrequencyContainer_t*& lfc = message->cam.camParameters.lowFrequencyContainer;
	lfc = vanetza::asn1::allocate<LowFrequencyContainer_t>();
	lfc->present = LowFrequencyContainer_PR_basicVehicleContainerLowFrequency;
	BasicVehicleContainerLowFrequency& bvc = lfc->choice.basicVehicleContainerLowFrequency;
	bvc.vehicleRole = VehicleRole_default;
	bvc.exteriorLights.buf = static_cast<uint8_t*>(vanetza::asn1::allocate(1));
	assert(nullptr != bvc.exteriorLights.buf);
	bvc.exteriorLights.size = 1;
	bvc.exteriorLights.buf[0] |= 1 << (7 - ExteriorLights_daytimeRunningLightsOn);
	// TODO: add pathHistory

	std::string error;
	if (!message.validate(error)) {
		throw cRuntimeError("Invalid Low Frequency CAM: %s", error.c_str());
	}
}

//start by ryu
void CaService::updateCSVWithIndex(std::string& filename,  uint32_t id,  bool isChange)
{
	std::string id_str = std::to_string(id);
	// std::cout << "updateCSVWithIndex" << std::endl;

	std::ifstream inFile(filename);
    if (!inFile.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }

    // インデックス作成（ID -> ファイル位置）
    std::unordered_map<std::string, std::streampos> index;
    std::string line;
    std::streampos pos = inFile.tellg();

    while (std::getline(inFile, line)) {
        std::stringstream ss(line);
        std::string rowId;
        std::getline(ss, rowId, ',');
        index[rowId] = pos;
        pos = inFile.tellg();
    }

    inFile.close();
	
	//Trueなら1、Falseなら0
	int int_ischange=0;
	isChange ? int_ischange=1 : int_ischange=0;
    // IDが存在する場合、更新
    if (index.find(id_str) != index.end()) {
        std::fstream file(filename, std::ios::in | std::ios::out);
        if (!file.is_open()) {
            std::cerr << "Failed to open file for update." << std::endl;
            return;
        }

        file.seekp(index[id_str]);
        std::getline(file, line); // 更新対象の行を読み飛ばす
        file.seekp(index[id_str]);    // 再度位置を調整
        file << id_str << ","<< int_ischange << "\n"; //

        file.close();
    } else {
        // IDが存在しない場合、新しい行を追加
        std::ofstream outFile(filename, std::ios::app);
        if (!outFile.is_open()) {
            std::cerr << "Failed to open file for appending." << std::endl;
            return;
        }
        outFile << id_str << "," << int_ischange << "\n";
        outFile.close();
    }
}

bool CaService::calculateTChange()
{
	float time_e = mGenCam.dbl();

	// 等加速運動として計算
	float vectorA_e=(mVehicleDataProvider->speed().value()-mLastCamSpeed.value())/time_e;
	float vectorV_e=mVehicleDataProvider->speed().value() + vectorA_e * time_e ;
	// float vectorP_e=mVehicleDataProvider->position() + vectorV_e * time_e + vectorA_e * 0.5 * time_e * time_e;
	float time_change_p = (sqrt(vectorV_e*vectorV_e+2*vectorA_e*mPositionDelta.value())-vectorV_e)/vectorA_e;
	float time_change_v = mSpeedDelta.value()/vectorA_e;
	
	float degreeV_e=(mVehicleDataProvider->heading().value()-mLastCamHeading.value())/time_e;
	float degree_e=mVehicleDataProvider->heading().value()+degreeV_e * time_e;
	float time_change_a = mHeadingDelta.value()/degreeV_e;

	if(mGenCamLowDynamicsCounter >=  mGenCamLowDynamicsLimit){
		return (mGenCamMax.dbl() >time_change_a ||mGenCamMax.dbl() > time_change_v || mGenCamMax.dbl() > time_change_p);
	}else{
		return (time_e >time_change_a ||time_e > time_change_v || time_e > time_change_p);
	}


}
//end by ryu

} // namespace artery

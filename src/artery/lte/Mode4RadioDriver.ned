package artery.lte;

import artery.nic.IRadioDriver;

simple RadioDriver like IRadioDriver
{
	parameters:
		@class(Mode4RadioDriver);
		@signal[ChannelLoad](type=double);
		double channelLoadReportInterval = default(0.1s) @unit(s);
		bool addStartUpDelay = default(false);

	gates:
		inout upperLayer;
		input lowerLayerIn;
		output lowerLayerOut;
		output properties;
}

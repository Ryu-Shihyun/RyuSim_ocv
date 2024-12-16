//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package artery.application;

simple CaService like ItsG5Service
{
    parameters:
        @signal[CamReceived];
        @signal[CamReceivedID];
        @signal[CamSent];

        // @statistic[reception](source=CamReceived;record=vector(camStationId)?,vector(camGenerationDeltaTime)?);
        // @statistic[transmission](source=CamSent;record=vector(camStationId)?,vector(camGenerationDeltaTime)?);
        @statistic[CamReceived](title="cam received";source="CamReceived";record=sum,vector);
        @statistic[CamReceivedID](title="source id of cam received";source="CamReceivedID";record=sum,vector);
        @statistic[CamSent](title="cam sent";source="CamSent";record=sum,vector);

        //ryu added
        @signal[camSentHead](type="double");
        @signal[camSentPositionX](type="double");
        @signal[camSentPositionY](type="double");
        @signal[camSentSpeed](type="double");
        @signal[camTriggerHead](type="double");
        @signal[camTriggerPosition](type="double");
        @signal[camTriggerSpeed](type="double");
        @signal[camVehicleId](type="double");
        @statistic[camSentHead](titile="Heading angles when cam is sent";source="camSentHead";record=sum,vector);
        @statistic[camSentPositionX](titile="Position x when cam is sent";source="camSentPositionX";record=sum,vector);
        @statistic[camSentPositionY](titile="Position y when cam is sent";source="camSentPositionY";record=sum,vector);
        @statistic[camSentSpeed](titile="Speed when cam is sent";source="camSentSpeed";record=sum,vector);
        @statistic[camTriggerHead](titile="head trigger";source="camTriggerHead";record=sum,vector);
        @statistic[camTriggerPosition](titile="position trigger";source="camTriggerPosition";record=sum,vector);
        @statistic[camTriggerSpeed](titile="speed trigger";source="camTriggerSpeed";record=sum,vector);
        @statistic[camVehicleId](titile="vehicle ID";source="camVehicleId";record=vector);
        
        // evaluate DCC transmission interval restrictions
        bool withDccRestriction = default(true);

        // generation interval boundaries
        double minInterval @unit(s) = default(0.1s);
        double maxInterval @unit(s) = default(1.0s);

        bool exponentialNonPeriodic = default(false);
        double exponentialMean @unit(s) = default(0.05s);

        // generate at fixed rate (using minInterval, optionally restricted by DCC)
        bool fixedRate = default(false);

        // change in orientation triggering CAM generation (in degree)
        double headingDelta = default(4.0);

        // change in position triggering CAM generation
        double positionDelta @unit(m) = default(4.0m);

        // change in speed triggering CAM generation (in meter/second)
        double speedDelta @unit(mps) = default(0.5mps);
}

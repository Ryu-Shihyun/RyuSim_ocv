//
// Artery V2X Simulation Framework
// Copyright 2014-2017 Hendrik-Joern Guenther, Raphael Riebl, Oliver Trauer
// Licensed under GPLv2, see COPYING file for detailed license and warranty terms.
//

package artery.envmod.sensor;

simple CpmSensor
{
    parameters:
        // cpmの送信時の生成時間を集めるシグナル
        @signal[cpmReceivedGenerationTime](type="omnetpp::SimTime");
        @statistic[cpmReceivedGenerationTime](title="cpmReceivedGenerationTime"; source="cpmReceivedGenerationTime"; record=vector);
        // cpmの送信元のSUMOのIDを集めるシグナル
        @signal[cpmReceivedSourceId](type="long");
        @statistic[cpmReceivedSourceId](title="cpmReceivedSourceId"; source="cpmReceivedSourceId"; record=vector);
        // cpmに含める車両のSUMOのIDを集めるシグナル
        @signal[cpmReceivedContainedId](type="long");
        @statistic[cpmReceivedContainedId](title="cpmReceivedContainedId"; source="cpmReceivedContainedId"; record=vector);

        string identityRegistryModule;
}

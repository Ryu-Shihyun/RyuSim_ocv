package artery.lte;

import artery.application.VehicleMiddleware;
import artery.networking.Vanetza;
import artery.nic.IRadioDriver;

import inet.node.inet.INetworkNode;

import lte.stack.phy.ILteNic;

module Mode4Car extends artery.inet.PlainVehicle like INetworkNode
{
    parameters:
        // LTE NIC
        string nicType = default("LteNicVUeMode4");
        int macNodeId = default(0);
        int masterId = default(0); // Not yet removed from SimuLTE for Mode 4 simulations

        @networkNode;
        @labels(node,ethernet-node,wireless-node);

        int numRadios = default(1);

    gates:
        input lteRadioIn @directIn;
        input radioIn[numRadios] @directIn;
        inout pppg[] @labels(PPPFrame-conn);
        inout ethg[] @labels(EtherFrame-conn);

    submodules:
        lteNic: <nicType> like ILteNic {
            @display("p=150,400");
            nodeType = "UE";
        }

        radioDriver: RadioDriver {
            parameters:
                @display("p=250,300");
        }

        vanetza: Vanetza {
            parameters:
                @display("p=250,200");
                *.middlewareModule = absPath("^.middleware");
                *.mobilityModule = absPath("^.mobility");
                *.radioDriverModule = absPath("^.radioDriver");
                runtime.datetime = middleware.datetime;
        }

        middleware: VehicleMiddleware {
            parameters:
                @display("p=250,100");
                mobilityModule = ".mobility";
        }

    connections allowunconnected:
        lteNic.radioIn <-- lteRadioIn;

        radioDriver.upperLayer <--> vanetza.radioDriverData;
        radioDriver.properties --> vanetza.radioDriverProperties;

        radioDriver.lowerLayerOut --> lteNic.upperLayerIn;
        radioDriver.lowerLayerIn <-- lteNic.upperLayerOut;
}

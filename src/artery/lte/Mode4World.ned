package artery.lte;

import inet.networklayer.ipv4.RoutingTableRecorder;
import inet.node.ethernet.Eth10G;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import lte.corenetwork.binder.LteBinder;
import lte.corenetwork.deployer.LteDeployer;
import lte.world.radio.LteChannelControl;

network Mode4World extends artery.inet.World
{
    parameters:
        double playgroundSizeX @unit(m); // x size of the area the nodes are in (in meters)
        double playgroundSizeY @unit(m); // y size of the area the nodes are in (in meters)
        double playgroundSizeZ @unit(m); // z size of the area the nodes are in (in meters)
        @display("bgb=750,500");
        traci.mapper.vehicleType = default("artery.lte.Mode4Car");

    submodules:
        routingRecorder: RoutingTableRecorder {
            @display("p=700,75;is=s");
        }

        //# LTE modules
        channelControl: LteChannelControl {
            @display("p=700,25;is=s");
        }

        binder: LteBinder {
            @display("p=700,175;is=s");
        }

        deployer: LteDeployer {
            @display("p=700,225;is=s");
        }
}

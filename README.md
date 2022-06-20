# body-nodes-specs
In this folder you can find all the Bodynodes specification documents for Development Environments.

In all the documents we refer to:
- Node as a generic device capable of sending data
- Host as a generic machine capable of accepting data and use it for an Application

The first step for a Node to interact with a Host is to "Establish a Connection"

The Node sends information through "Messages".
The Host can give commands to Nodes by sending "Actions"

The is a third actor called SNode that can act as intermediate between Nodes and a Host.
Typically it is used to help in case when there are limitations on the communications.
SNodes can still have their own sensors and add data to the stream they collect from other Nodes to the Host.

Messages and Actions will refer to specific "Bodyparts" with codes and names depending on the communication.

In order for every application to work properly the "Sensors on the Node" have to send data with the same axis.
So we specify with pictures what are the expected values coming from the Node with each position/movement.
For now we specify on the "AbsoluteOrientation".

Communication supported are:
- Wifi -> Wifi

Naming conventions follow the following format:
- Bodynode: A Node made officially by Bodynodes
- BodynodesHost: A Host made officially by Bodynodes

Naming depending on the protocol in use:
- <protocol> Bodynode -> <protocol> Node, examples:
  - Wifi Bodynode -> Wifi Node
- <protocol> BodynodesHost -> <protocol> Host, examples:
  - Wifi BodynodesHost   -> Wifi Host


The Nodes we currently consider in the specifications are:
- WifiNodes

Hosts can be easily implementated by knowing the messages and actions exchanged. Anyone is encourage to create his own Host and Application. 

If you want to create an Application using our Production Environment get in touch with usby sending us an email at bodynodes.dev@gmail.com

// Black Box Board Software //////////////////////////////////////////////////////////////////////////////////////////////////////////
// MRDT 2023                //////////////////////////////////////////////////////////////////////////////////////////////////////////
// Grant Brinker            //////////////////////////////////////////////////////////////////////////////////////////////////////////
// #RoveSoHard              //////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "BlackboxSoftware.h"


void setup()
{
    Serial.begin(9600);
    RoveComm.begin(RC_BLACKBOXBOARD_FOURTHOCTET, &TCPServer, RC_ROVECOMM_BLACKBOXBOARD_MAC);

    telemetry.begin(Telemetry, 1500000);
    Serial.println("Started: ");

    struct Board BMS, PowerBoard, Nav, ArmBoard, SciMoco, SciHeater, SciSensors;

    BMS.boardIP =                   "192.168.1.133";
    PowerBoard.boardIP =            "192.168.1.132";
    Nav.boardIP =                   "192.168.1.136";
    ArmBoard.boardIP =              "192.168.1.131";
    SciMoco.boardIP =               "192.168.1.137";
    SciHeater.boardIP =             "192.168.1.144";
    SciSensors.boardIP =            "192.168.1.138";

    BMS.boardFourthOctet =          133;
    PowerBoard.boardFourthOctet =   132;
    Nav.boardFourthOctet =          136;
    ArmBoard.boardFourthOctet =     131;
    SciMoco.boardFourthOctet =      137;
    SciHeater.boardFourthOctet =    144;
    SciSensors.boardFourthOctet =   138;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void loop()
{
    packet = RoveComm.read();

    switch(packet.data_id)
    {
        case RC_BLACKBOXBOARD_BLACKBOXLISTENING_DATA_ID:
            
    }
}
#pragma once

#include <iostream>
#include <fstream>
#include "RoveComm.h"

RoveCommEthernet RoveComm;
rovecomm_packet packet;

EthernetServer TCPServer(RC_ROVECOMM_SIGNALSTACKBOARD_PORT);

IntervalTimer telemetry;




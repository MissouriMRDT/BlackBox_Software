'''
conda activate test
cd C:\\Users\Andrew\Documents\GitHub\BlackBox_Software
python BlackBox_Software.py
'''

from RoveComm_Python import *
import os
import datetime
import threading
import atexit

ROVECOMM_ADDRESS_BASE = "192.168.1."

#Add addresses to sniff here
board_addresses = {
		"OPEN" :"130",
		"ARM" :"131",
		"POWER" :"132",
		"BMS" :"133",
		"DRIVE" :"134",
		"LIGHTINGSHIMBLE" :"135",
		"NAVCAMERA" :"136",
		"SRAACTUATION" :"137",
		"SRASENSORS" :"138",
		"AUTONOMY" :"139",
		"SHIMBLENAV" :"140"
}

startup_time = datetime.datetime.now()
try:
	os.mkdir("0-DataLog")
except:
	pass
	
folder_path = "0-DataLog/" + str(startup_time).replace(':', '_')
os.mkdir(folder_path)
os.chdir(folder_path)

RoveComm = RoveCommEthernetUdp()
do_thread = True
boards = []


	
def subscribeAll():
	print("Subscribing")
	for board in boards:
		board.subscribe()
	if(do_thread):
		subscribe_thread = threading.Timer(1, subscribeAll)
		subscribe_thread.daemon = True
		subscribe_thread.start()
	
class BoardFile():
	def __init__(self, board_name, ip_octet_4, port=ROVECOMM_PORT):
		self.board_name = board_name
		self.ip_address = (ROVECOMM_ADDRESS_BASE + ip_octet_4, port)
		self.file_name = str(self.ip_address) + "_" + self.board_name + ".txt"
		self.file = open(self.file_name, "w+")
		self.file.write("Number, Timestamp, Delta, ID, Count, Type, Data\n")
		self.file.close()
		
		self.start_time = datetime.datetime.now()
		self.count = 0
			
	def subscribe(self):
		packet = RoveCommPacket(ROVECOMM_SUBSCRIBE_REQUEST)
		packet.SetIp(self.ip_address)
		RoveComm.write(packet)
		
	def parsePacket(self, packet):
		if (packet.ip_address == self.ip_address):
			now = datetime.datetime.now()
			delta = now-self.start_time
			self.file = open(file_name, 'a')
			self.file.write(count, str(now), str(delta), packet.data_id, packet.data_count, packet.data_type, packet.data, +"\n")
			self.file.close()
			
			self.count = count+1
	
for x in board_addresses:
	boards.append(BoardFile(x, board_addresses[x]))
	
subscribeAll()

while(1):
	packet = RoveComm.read()
	if(packet.data_id != 0):
		for board in boards:
			board.parsePacket(packet)
		
	





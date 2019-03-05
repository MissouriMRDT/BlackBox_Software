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

#Add addresses to sniff here
board_addresses = {
		"OPEN"            :"192.168.1.130",
		"ARM"             :"192.168.1.131",
		"POWER"           :"192.168.1.132",
		"BMS"             :"192.168.1.133",
		"DRIVE"           :"192.168.1.134",
		"LIGHTINGSHIMBLE" :"192.168.1.135",
		"NAVCAMERA"       :"192.168.1.136",
		"SRAACTUATION"    :"192.168.1.137",
		"SRASENSORS"      :"192.168.1.138",
		"AUTONOMY"        :"192.168.1.139",
		"SHIMBLENAV"      :"192.168.1.140",
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
	def __init__(self, board_name, ip_address, port=ROVECOMM_PORT):
		self.board_name = board_name
		self.ip_address = (ip_address, port)
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
			self.file = open(self.file_name, 'a')
			self.file.write(str(self.count) + "," + 
							str(now) + "," + 
							str(delta) + "," + 
							str(packet.data_id) + "," + 
							str(packet.data_count) + "," + 
							str(packet.data_type) + "," + 
							str(packet.data) + "\n")
			self.file.close()
			
			self.count = self.count+1
	
for x in board_addresses:
	boards.append(BoardFile(x, board_addresses[x]))
	
subscribeAll()

while(1):
	packet = RoveComm.read()
	if(packet.data_id != 0):
		packet.print()
		for board in boards:
			board.parsePacket(packet)
		
	





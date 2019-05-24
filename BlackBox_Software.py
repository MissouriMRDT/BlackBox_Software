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

#Add addresses to define and subscribe to here
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
		#"SHIMBLENAV"      :"192.168.1.140",
}

startup_time = datetime.datetime.now()
try:
	os.mkdir("0-DataLog")
except:
	pass
	

try:
	sequence_store = open("sequence.txt", "r")
	sequence_num = int(sequence_store.read())
	sequence_store.close()
	sequence_store = open("sequence.txt", "w")
	sequence_store.write(str(sequence_num+1))
	sequence_store.close()
except:
	sequence_store = open("sequence.txt", "w+")
	sequence_num = 0
	sequence_store.write(str(sequence_num+1))
	sequence_store.close()
	
instance_folder_path = "0-DataLog/" + str(sequence_num) + "-" + str(startup_time).replace(':', '_')
os.mkdir(instance_folder_path)
os.chdir(instance_folder_path)

RoveComm = RoveCommEthernetUdp()
do_thread = True
boards = []


	
def subscribeAll():
	print("Subscribing")
	for board in boards:
		board.subscribe()
	if(do_thread):
		subscribe_thread = threading.Timer(5, subscribeAll)
		subscribe_thread.daemon = True
		subscribe_thread.start()
	
class IdFile():
	def __init__(self, data_id, board_address):
		self.data_id = data_id
		self.file_name = board_address +"/"+ str(data_id) + ".txt"
		
		self.file = open(self.file_name, 'w+')
		self.file.write("Count,Time,Delta,Data ID, Data Count,Data Type, Data\n")
		self.count = 0
		self.file.close()
		
	def writeFile(self, packet):
		if(packet.data_id == self.data_id):
			now = datetime.datetime.now()
			delta = now-startup_time
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
		
	
class BoardFolder():
	def __init__(self, board_name, ip_address, port=ROVECOMM_PORT):
		self.board_name = board_name
		self.ip_address = ip_address
		
		self.board_dir = str(self.ip_address) + "_" + self.board_name
		
		os.mkdir(self.board_dir)
		
		self.id_files = []
		
		self.count = 0
			
	def subscribe(self):
		packet = RoveCommPacket(ROVECOMM_SUBSCRIBE_REQUEST)
		packet.data_id = 3
		packet.SetIp(self.ip_address)
		RoveComm.write(packet)
		
	def parsePacket(self, packet):
		if (packet.ip_address == self.ip_address):
			if(packet.data_id not in [a.data_id for a in self.id_files]):
				self.id_files.append(IdFile(packet.data_id, self.board_dir))
			for id in self.id_files:
				id.writeFile(packet)
			
	
for x in board_addresses:
	boards.append(BoardFolder(x, board_addresses[x]))
	
subscribeAll()

new_boards = 0;

while(1):
	packet = RoveComm.read()
	if (packet.data_id != 0):
		if(packet.ip_address not in [a.ip_address for a in boards]):
			new_boards = new_boards + 1
			boards.append(BoardFolder("Board-" + str(new_boards), packet.ip_address[0]))
		packet.print()
		for board in boards:
			board.parsePacket(packet)






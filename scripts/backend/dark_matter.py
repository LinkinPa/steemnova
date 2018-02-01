# ==================================================================================\\
# ~TheRavikin |  theravikin.pl | mail at: scripts@theravikin.pl  					 ||
#	TO DO:																			 ||
#		- change SQL																 ||
#		- change limit hisotry or change it completly								 ||
#		- change black matter multiplayer											 ||
#		- depending on currency SBD or STEEM need to adjust multiplier				 ||
# ==================================================================================//
from steem import Steem
from datetime import datetime
import json
import os.file

# Some global vars
_json = ""
_time = datetime.now().isoformat(timespec='seconds')
_date = datetime.now().strftime("%d%m%y")

# Some funcions

## opening steem object
def init():
    global _json

    s = Steem()																	# steeming it up!
   try:
    	data = s.get_account_history('steemnova', -1, limit=100)				# getting account history
    except :
    	raise NameError("init() faild at downloading history. \tData response:\n\t "+data)	
    

## just log into file
def log(__line):
	logfile = os.getcwd()+"/"+_date+".log" 
	if logfile.exists(): 														# checking for logfile existance
	    with open(logfile, 'a') as f:											# if exists then just append new line
	        f.write(__line)
	else:																		# if not then create new one with CSV header
		with open(logfile, 'w') as f:
			f.write("timestamp;player;recived;darkmatter"+'\n')

## some magic
def get_transfers():
    for __item in _json:															# for top json item
        if __item[1]['op'][0] == "transfer":										# search for transfers
            if __item[1]['op'][1]['memo'] == "hokus pokus":							# and for steemnova darkmatter top-ups
                __transaction_timestamp = __item[1]['timestamp']			
                __player = __item[1]['op'][1]['from']			
                __amount_recived = float(__item[1]['op'][1]['amount'].partition(' ')[0])	
                __dark_matter_to_send = float(amount_recived * 3)													# HOW much darkmatter player will get
                log("GT;{0};{1};{2};{3}".format(__transaction_timestamp, __player, __amount_recived, __dark_matter_to_send)+'\n')	# loginng for future

## here comes less magic
def pay_users(__user, __amount, __timestamp): 
	INSERT INTO table (user_col, mater_col) VALUES (__user, __amount);			# add dark matter to the users while guessing the columns xd
	log("PU;{0};{1};{2}".format(_time, __user, __amount)+'\n')					# and inform about it ;D
	with open("lastpaid.txt", 'w') as f:										#  \  
		f.write(__timestamp)													#	update last paid timestamp
	
## aaand here comes the truth!
def rotate():
	with open("lastpaid.txt", 'r') as lastpaid:
		with open("logfile.log", 'rb') as csvfile:
			line = csv.reader(csvfile, delimiter=';')
				for row in line:
					if line['timestamp'] > lastpaid:						   # if player wasn't paid yet he is getting paid (english.... -.-)
						pay_users(line['player', 'darkmatter', 'timestamp'])



# MAIN
## initiating program...
init()
## sniffing transactions
get_transfers()
## making some good stuff for tribe ppl
rotate()
# goin' sleep
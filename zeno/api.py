import argparse
import json
from flask import Flask
from app import zeno, thread_pcap, classify
from utils import utils, netutils, globalvar
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/last-second-bytes")
def hello():
	data = {}
	data['upload'] = 0	
	data['download'] = globalvar.last_second_bytes
	return json.dumps(data)


@app.route("/results")
def results():
	data = {}
	data['scalogram'] = globalvar.last_scalogram
	data['scales'] = globalvar.last_scales
	data['service'] = globalvar.last_service
	return json.dumps(data)


if __name__ == "__main__":

	print("Reading arguments...")
	k = 0
	parser=argparse.ArgumentParser()
	parser.add_argument('-i', '--interface', nargs='?',required=True, help='capture interface')
	parser.add_argument('-c', '--cnet', nargs='+',required=True, help='client network(s)')
	parser.add_argument('-s', '--snet', nargs='+',required=True, help='service network(s)')
	parser.add_argument('-t', '--tcpport', nargs='?',help='service TCP port (or range)')
	parser.add_argument('-u', '--udpport', nargs='?',help='service UDP port (or range)')
	args=parser.parse_args()

	globalvar.init()
	zeno.start(args)
	
	app.run(host=str(netutils.get_lan_ip()))

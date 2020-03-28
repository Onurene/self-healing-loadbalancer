import os
import subprocess
import requests
from flask import Flask
from flask_cors import CORS, cross_origin
import datetime
import json
import digitalocean

app = Flask(__name__)

stopCommand = "service haproxy stop"
startCommand = "service haproxy start"

master_sh = "/etc/keepalived/master.sh"





API_KEY = '50bb20782a2205c5cac0a42cefcc267a96b73908c936a841ace210bbbe5bbf07'
DROPLET_ID = '184416072'
SNAPSHOT_NAME = 'snap2_' + str(datetime.datetime.now())
KEEP_SNAPSHOTS = 1

API_LIST_SHAPSHOTS = 'https://api.digitalocean.com/v2/droplets/' + str(DROPLET_ID) + '/snapshots'

API_CREATE_SNAPSHOT = 'https://api.digitalocean.com/v2/droplets/' + str(DROPLET_ID) + '/actions'


headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer ' + API_KEY
}

payload = {}


d = {
    'type': 'snapshot',
    'name': SNAPSHOT_NAME
}

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/start')
@cross_origin()
def server_request():
    subprocess.call(startCommand, shell=True)
    return "Started"


@app.route('/stop')
@cross_origin()
def haproxy_stop():
    #print("requesting snapshot")
    #r = requests.post(API_CREATE_SNAPSHOT, data=json.dumps(d), headers=headers)
    #print("snapshot response ",r)
    subprocess.call(stopCommand, shell=True)
    print("HAPROXY STOPPED")
    res = requests.get("http://134.209.159.251:5000/run_sh")
    print(res)
    #droplet_create = requests.post(url, data=json.dumps(data), headers=h)
    #print("droplet created ",droplet_create)
    return "HAPROXY STOPPED"


@app.route('/run_sh')
def run_sh():
    print("running .sh file")
    subprocess.call(master_sh, shell=True)
    print("floating ip reassigned")
    return "IP reassigned"


@app.route('/list_snap')
@cross_origin()
def list_snapshot():
    r = requests.get(API_LIST_SHAPSHOTS, data=json.dumps(payload), headers=headers)
    data = r.json()
    snapshots = data['snapshots']
    print(snapshots)
    return "listed"



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')



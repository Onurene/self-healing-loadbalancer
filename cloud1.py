import os
import subprocess
import requests
from flask import Flask
from flask_cors import CORS, cross_origin
import datetime
import json
import digitalocean
import shlex


app = Flask(__name__)

stopCommand = "service haproxy stop"
startCommand = "service haproxy start"
master_sh = "/etc/keepalived/master.sh"


#url = "https://api.digitalocean.com/v2/droplets"
#h = {"Content-Type":"application/json", "Authorization": "Bearer 614703c9aef96dd673cbe68ddddb7bf91804bc6f6501ea7024cd7dbebda562bc"}
#data = {"name":"snapshotDroplet","region":"BLR1","size":"s-1vcpu-2gb","ssh_keys":"null","backups":"false","ipv6":"false","user_data":"Peer1","private_networking":"null", "image":"60410489"}

API_KEY = '50bb20782a2205c5cac0a42cefcc267a96b73908c936a841ace210bbbe5bbf07'
DROPLET_ID = '184414244'
SNAPSHOT_NAME = 'snap_' + str(datetime.datetime.now())
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


def droplet_create(snapshot_id):
    subprocess.call('python try.py', shell=True)
    print("droplet created ",droplet_create)
    return

def starthaproxy():
    subprocess.call(startCommand, shell=True)
    print("HAproxy started")
    return

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
    r = requests.post(API_CREATE_SNAPSHOT, data=json.dumps(d), headers=headers)
    print("snapshot response ",r)
    print()
    subprocess.call(stopCommand, shell=True)
    print("HAPROXY STOPPED")
    requests.get("http://134.209.144.190:5000/start")
    requests.get("http://134.209.144.190:5000/run_sh")
    print("ran sh file")
    r = requests.get(API_LIST_SHAPSHOTS, data=json.dumps(payload), headers=headers)
    data = r.json()
    snapshots = data['snapshots']
    op = snapshots[0][u'id']
    print(op)
    #op = op.encode()
    droplet_create(op)
    #droplet_create = requests.post(url, data=json.dumps(data), headers=h)
    #print("droplet created ",droplet_create)
    return "Stopped"


@app.route('/run_sh')
def run_sh():
    print("running .sh file")
    subprocess.call(master_sh, shell=True)
    print("floating ip reassigned")
    starthaproxy()
    return "IP reassigned"


@app.route('/list_snap')
@cross_origin()
def list_snapshot():
    r = requests.get(API_LIST_SHAPSHOTS, data=json.dumps(payload), headers=headers)
    data = r.json()
    snapshots = data['snapshots']
    print(snapshots)
    snap_li = []
    #for i in range(len(snapshots)):
    #    snap_li.append(snapshots[i][u'name'])
    return snapshots[0][u'name']


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

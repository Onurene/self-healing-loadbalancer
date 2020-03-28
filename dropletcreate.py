import shlex
import subprocess
cmd = '''curl -X POST -d  '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP", "actions": "ALLOW", "priority": "10"}' http://localhost:8080/firewall/rules/0000000000000001'''




c = '''curl -X POST -H 'Content-Type: application/json'  -H 'Authorization: Bearer  50bb20782a2205c5cac0a42cefcc267a96b73908c936a841ace210bbbe5bbf07' -d '{"name":"newdroplet","region":"BLR1","size":"s-1vcpu-2gb","ssh_keys":null,"backups":false,"ipv6":false,"user_data":"Peer1","private_networking":null, "image":"60510549"}' "https://api.digitalocean.com/v2/droplets"
'''
args = shlex.split(c)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

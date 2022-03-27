import yaml
import subprocess
import itertools

with open('config.yaml') as f:
    config = yaml.safe_load(f)

network = config['network']
rules = config['rules']
external_ip = network['external_ip']
external_interface = network['external_interface']
internal_network = network['internal_network']

prerouting_template = 'iptables -t nat -A PREROUTING -p {4} -d {0} --dport {1} -j DNAT --to-destination {2}:{3}'
postrouting_template = 'iptables -t nat -A POSTROUTING -p {4} -d {2} --sport {3} -j SNAT --to-source {0}:{1}'
port_template = 'iptables -A INPUT -p {1} --dport {0} -j ACCEPT'

nat_rules = [f'iptables -t nat -A POSTROUTING -s {internal_network} -o {external_interface} -j MASQUERADE']
prerouting_rules = []
postrouting_rules = []
port_rules = []

for internal_ip, protocols in rules.items():
    for protocol, ports in protocols.items():
        for external_port, internal_port in ports.items():
            prerouting_rules.append(prerouting_template.format(external_ip, external_port, internal_ip, internal_port, protocol))
            postrouting_rules.append(postrouting_template.format(external_ip, external_port, internal_ip, internal_port, protocol))
            port_rules.append(port_template.format(external_port, protocol))

for rule in itertools.chain(nat_rules, prerouting_rules, postrouting_rules, port_rules):
    print('Applying:', rule)
    process = subprocess.run(rule.split())
    if process.returncode:
        print('Error while applying this rule')


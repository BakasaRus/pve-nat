import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

network = config['network']
rules = config['rules']
external_ip = network['external_ip']

prerouting_template = 'iptables -t nat -A PREROUTING -p tcp -d {0} --dport {1} -j DNAT --to-destination {2}:{3}'
postrouting_template = 'iptables -t nat -A POSTROUTING -p tcp -d {2} --sport {3} -j SNAT --to-source {0}:{1}'
port_template = 'iptables -A INPUT -p tcp --dport {0} -j ACCEPT'

prerouting_rules = []
postrouting_rules = []
port_rules = []

for internal_ip, ports in rules.items():
    for external_port, internal_port in ports.items():
        prerouting_rules.append(prerouting_template.format(external_ip, external_port, internal_ip, internal_port))
        postrouting_rules.append(postrouting_template.format(external_ip, external_port, internal_ip, internal_port))
        port_rules.append(port_template.format(external_port))

print(*prerouting_rules, sep='\n')
print(*postrouting_rules, sep='\n')
print(*port_rules, sep='\n')
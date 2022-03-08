#!/usr/bin/env bash

iptables -F PREROUTING
iptables -F POSTROUTING
iptables -F INPUT

source venv/bin/activate
python main.py
deactivate

iptables-save > /etc/iptables/rules.v4
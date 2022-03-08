#!/usr/bin/env bash

iptables -t nat -F
iptables -F INPUT

source venv/bin/activate
python main.py
deactivate

iptables-save > /etc/iptables/rules.v4
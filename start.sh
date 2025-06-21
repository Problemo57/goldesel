#!/bin/bash

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -P FORWARD ACCEPT
sudo iptables -P INPUT ACCEPT

docker compose up --build -d

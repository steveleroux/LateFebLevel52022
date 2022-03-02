#!/usr/bin/python3

import yaml

file = open('underlay.yml', 'r')

underlay = yaml.safe_load(file)

for switch in underlay:
  print("The config for", switch, "is bellow:")
  print("----------------------------------")
  for interface in underlay[switch]['interfaces']:
      print("interface", interface)
      print("  ip address", underlay[switch]['interfaces'][interface])
  print("router bgp", underlay[switch]['BGP']['ASN'])
  loopback0 = underlay[switch]['interfaces']['loopback0']
  router_id = loopback0.split("/")
  print("  router-id", router_id[0])
  print("----------------------------------")    
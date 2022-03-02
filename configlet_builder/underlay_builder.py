#!/usr/bin/python3
from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml
from cvplibrary import RestClient
import ssl

prefix_list = """
 ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
    seq 50 permit 192.168.253.0/24 eq 32
"""
route_map = """
route-map LOOPBACK permit 10
   match ip address prefix-list LOOPBACK
"""
peer_filter = """ 
peer-filter LEAF-AS-RANGE
 10 match as-range 65000-65535 result accept
"""


def get_yaml(configlet):
  ssl._create_default_https_context = ssl._create_unverified_context
  cvp_url = 'https://192.168.0.5/cvpservice/'
  client = RestClient(cvp_url+'configlet/getConfigletByName.do?name='+configlet,'GET')
  if client.connect():
    raw = yaml.load(client.getResponse())
    yaml_raw = raw['config']
    yaml_dict = yaml.safe_load(yaml_raw)
    return yaml_dict

def get_hostname():
  stuff = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
  for item in stuff:
    if 'hostname' in item:
      key, value = item.split(':')
      hostname = value
  return hostname
  
hostname = get_hostname()  
underlay = get_yaml('underlay_yaml')

def gen_interfaces(hostname):
  for interface in underlay[hostname]['interfaces']:
    print("interface %s") % interface
    ip = underlay[hostname]['interfaces'][interface]['ipv4']
    mask = underlay[hostname]['interfaces'][interface]['mask']
    print("  ip address %s/%s") % (ip, mask)
    if 'Ethernet' in interface:
      print("  no switchport")
      mtu = underlay['global']['MTU']
      print("  mtu %s") % mtu
  
def gen_spine_bgp(hostname):
  print(prefix_list)
  print(route_map)
  print(peer_filter)
  
  print("router bgp %s") % underlay[hostname]['BGP']['ASN']
  router_id = underlay[hostname]['interfaces']['loopback0']['ipv4']
  print("  router-id %s") % router_id
  print("""
  no bgp default ipv4-unicast
  maximum-paths 3
  distance bgp 20 200 200
""")

  DC_number_list = hostname.split("-")
  DC_number = DC_number_list[1]
  listen_range = underlay['global'][DC_number]['p2p']
  print("  bgp listen range %s peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE") % listen_range

  print("""      
  neighbor LEAF_Underlay peer group
  neighbor LEAF_Underlay send-community
  neighbor LEAF_Underlay maximum-routes 12000
  """)
  

  print("  neighbor EVPN peer group")
  evpn_listen_range = underlay['global'][DC_number]['lo0']
  print("  bgp listen range %s peer-group EVPN peer-filter LEAF-AS-RANGE") % evpn_listen_range
      
  print("""
  neighbor EVPN update-source Loopback0
  neighbor EVPN ebgp-multihop 3
  neighbor EVPN send-community extended
  neighbor EVPN maximum-routes 0

  redistribute connected route-map LOOPBACK
   
  address-family evpn
    neighbor EVPN activate
  address-family ipv4
    neighbor LEAF_Underlay activate
    redistribute connected route-map LOOPBACK
""")

def gen_leaf_bgp(hostname):
  DC_number_list = hostname.split("-")
  DC_number = DC_number_list[1]
  print(prefix_list)
  print(route_map)
  print(peer_filter)
  
  print("router bgp %s") % underlay[hostname]['BGP']['ASN']
  router_id = underlay[hostname]['interfaces']['loopback0']['ipv4']
  print("  router-id %s") % router_id
  print("""
  no bgp default ipv4-unicast
  maximum-paths 3
  distance bgp 20 200 200
""")
  spine_ASN = underlay['global'][DC_number]['spine_ASN']
  print("  neighbor Underlay peer group")
  print("  neighbor Underlay remote-as %s") % spine_ASN
  print("  neighbor Underlay send-community")
  print("  neighbor Underlay maximum-routes 12000")
  ASN = underlay[hostname]['BGP']['ASN']
  print("  neighbor LEAF_Peer peer group")
  print("  neighbor LEAF_Peer remote-as %s") % ASN
  print("  neighbor LEAF_Peer next-hop-self")
  print("  neighbor LEAF_Peer maximum-routes 12000") 

  for spine_peer in underlay[hostname]['BGP']['spine-peers']:
    print("  neighbor %s peer group Underlay") % spine_peer

  if underlay[hostname]['MLAG'] == 'Odd':
    print("  neighbor 192.168.255.2 peer group LEAF_Peer")
  if underlay[hostname]['MLAG'] == 'Even':
    print("  neighbor 192.168.255.1 peer group LEAF_Peer")
 
  print("  neighbor EVPN peer group")
    
  print("  neighbor EVPN remote-as %s") % spine_ASN
  print("""
  neighbor EVPN update-source Loopback0
  neighbor EVPN allowas-in 1
  neighbor EVPN ebgp-multihop 3
  neighbor EVPN send-community extended
  neighbor EVPN maximum-routes 12000
  """)
  
  EVPN_spine_list = underlay['global'][DC_number]['spine_peers']
  
  for EVPN_peer in EVPN_spine_list:
    print("  neighbor %s peer group EVPN") % EVPN_peer

   
    
  print("""
  address-family evpn
    neighbor EVPN activate
   
  address-family ipv4
    neighbor Underlay activate
    neighbor LEAF_Peer activate
    redistribute connected route-map LOOPBACK
  """)
  print("")

if 'spine' in hostname:
  gen_spine_bgp(hostname)
  
if 'leaf' in hostname:
  gen_leaf_bgp(hostname)

if 'spine' in hostname or 'leaf' in hostname:  
  gen_interfaces(hostname)



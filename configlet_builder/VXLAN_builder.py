from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml
from cvplibrary import RestClient
import ssl

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
VXLAN = get_yaml('VXLAN_yaml')

print("ip virtual-router mac-address 001c.7300.0099")

def gen_vrf():
  for Tenant in VXLAN['Tenants']:
    print("vrf instance %s") % Tenant
    print("ip routing vrf %s") % Tenant
  print("")

def gen_VLANS():
  for Tenant in VXLAN['Tenants']:
    for net_name in VXLAN['Tenants'][Tenant]['L2VNI']:
      print("vlan %s") % VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VLANID']
  print("")
def gen_SVI():
  for Tenant in VXLAN['Tenants']:
    for net_name in VXLAN['Tenants'][Tenant]['L2VNI']:
      print("interface vlan %s") % VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VLANID']
      print("  vrf %s") % Tenant
      print("  ip address virtual %s") % VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['SVI']
      
  print("")    

def gen_vxlan1():
  print("interface vxlan1")
  print("  vxlan source-interface Loopback1")
  print("  vxlan udp-port 4789")
  for Tenant in VXLAN['Tenants']:
    print("  vxlan vrf %s vni %s") % (Tenant, VXLAN['Tenants'][Tenant]['L3VNI'])
    for net_name in VXLAN['Tenants'][Tenant]['L2VNI']:
      print("  vxlan vlan %s vni %s") % (VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VLANID'], VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VNID'])
    
def gen_BGP():
  ASN = underlay[hostname]['BGP']['ASN']
  loopback0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
  print("router bgp %s ") % ASN
  for Tenant in VXLAN['Tenants']:
    print("  vrf %s") % Tenant
    print("    rd %s:%s") % (loopback0,VXLAN['Tenants'][Tenant]['L3VNI'])
    print("    route-target import evpn %s:%s") % (VXLAN['Tenants'][Tenant]['L3VNI'],VXLAN['Tenants'][Tenant]['L3VNI'])
    print("    route-target export evpn %s:%s") % (VXLAN['Tenants'][Tenant]['L3VNI'],VXLAN['Tenants'][Tenant]['L3VNI'])
    for net_name in VXLAN['Tenants'][Tenant]['L2VNI']:
      print("  vlan %s") % VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VLANID']
      print("     rd auto")
      VNID = VXLAN['Tenants'][Tenant]['L2VNI'][net_name]['VNID']
      print("     route-target both %s:%s") % (VNID,VNID)
      
gen_vrf()
gen_VLANS()
gen_SVI()
gen_vxlan1()
gen_BGP()


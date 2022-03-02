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
  
  
underlay = get_yaml('underlay_yaml')




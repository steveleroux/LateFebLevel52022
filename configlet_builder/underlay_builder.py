from cvplibrary import CVPGlobalVariables, GlobalVariableNames


def get_hostname():
  stuff = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
  for item in stuff:
    if 'hostname' in item:
      key, value = item.split(':')
      hostname = value
  return hostname
  
hostname = get_hostname()

print(hostname)
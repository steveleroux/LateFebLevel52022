# Configlet Builder to Configure Interfaces from YAML



One of the common use cases for network automation is to take an abstracted data model and turn it into native syntax for a given platform. This is a common use case for CloudVision Portal Configlet Builders. 

In this lab you will create a configlet builder that will take information from a data model (written in YAML) and generate configuration syntax that will configure physical interfaces on your topology. 

For EVPN networks, especially with eBGP as an underlay (which typically uses IPv4 addresses in a point-to-point fashion) this can be particularly useful. 


## Converting YAML to a Dictionary

Normally in a configlet builder, a data model will be external: It could be a file on a git repository, on a web server, or even YAML stored in another configlet. 

However, to make this lab more self-contained, the data model will be stored as a string in Python. With Python, multi-line strings (often called "docstrings") can be declared between triple quotes. 

(Note: Storing a data model in a script is not best practice, but will suffice for this lab)

Create a configlet builder called "Interface-Builder" .

Add the following to it:

<pre>
import yaml
config = """
leaf1-DC1:
  interfaces:
    loopback0:
      ipv4: 192.168.101.11
      mask: 32
    loopback1:
      ipv4: 192.168.102.11
      mask: 32
    Ethernet3:
      ipv4: 192.168.103.0
      mask: 31
    Ethernet4:
      ipv4: 192.168.103.2
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.4
      mask: 31
"""
switches = yaml.safe_load(config)
print(switches['leaf1']['interfaces']['loopback0']['ipv4'])

</pre>


Then click "Generate".

![](media/media/generate_static.png)

You should see the IP address displayed of loopback0 on the right.

Everything between the """ is the YAML data model, which describes the interface configuration for leaf1. YAML needs to be converted into a native data structure in Python called a dictionary, and that's done with the yaml.safe_load(config) line. 

"switches" is now a native Python dictionary containing the data model, and can be called using the brackets ([]) with the path of information required. 

## Looping Through a Dictionary

Replace the entire contents of the configlet with the following: 

<pre>
import yaml
config = """
leaf1-DC1:
  interfaces:
    loopback0:
      ipv4: 192.168.101.11
      mask: 32
    loopback1:
      ipv4: 192.168.102.11
      mask: 32
    Ethernet3:
      ipv4: 192.168.103.0
      mask: 31
    Ethernet4:
      ipv4: 192.168.103.2
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.4
      mask: 31
"""
switches = yaml.safe_load(config)

for iface in switches['leaf1-DC1']['interfaces']:
    print("interface %s") % iface
    ip = switches['leaf1-DC1']['interfaces'][iface]['ipv4']
    mask = switches['leaf1-DC1']['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
    if "Ethernet" in iface:
        print " no switchport"
</pre>


Click generate.

![](media/media/generate.png)

This should display an EOS friendly syntax that would configure the interfaces on the EOS switch leaf1. 



The for loop iterates through the elements under ['leaf1-DC1']['interfaces'], obtains the requsite information (ip, mask) and also checks to see if "Ethernet" is in the hostname. If Ethernet is in the hostname, the script issues the "no switchport" command. 

*(Don't worry about the order of interfaces, CloudVision will put them in the correct order when applied to the switch.)*

## Determine Which Switch

With minimal Python code, it's possible to retrief information from a YAML data model and generate an appropriate configuration. However, the script will need to work with mulitple devices in order to be useful, and for that to happen the script will need to know which switch it's being run against. 

CVP passes several variables to the scrip when run against a device. You will need to pull these variable out. 

Replace the entire script with the following: 

<pre>
from cvplibrary import CVPGlobalVariables, GlobalVariableNames

labels = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)


for item in labels:
  key, value = item.split(':')
  if key == 'hostname':
    hostname = value
    
print(hostname)

</pre>

In the "Form Design" dropdown, select a switch (any switch), then click "Generate". 

The name of the switch you selected in the Form Design drop down should be in the "Built Configlet" window on the right. 

Now we can put all these elements together and generate a configuraiton for multiple devices. 

### Interface Configlet Builder

Replace the entire configlet with the following: 

<pre>
from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml

labels = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)


for item in labels:
  key, value = item.split(':')
  if key == 'hostname':
    hostname = value
    

config = """
spine1-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.101
      mask: 32
    Ethernet2: 
      ipv4: 192.168.103.1
      mask: 31
    Ethernet3: 
      ipv4: 192.168.103.7
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.13
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.19
      mask: 31
    Ethernet6: 
      ipv4: 192.168.103.25
      mask: 31
    Ethernet7: 
      ipv4: 192.168.103.31
      mask: 31
spine2-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.102
      mask: 32
    Ethernet2: 
      ipv4: 192.168.103.3
      mask: 31
    Ethernet3: 
      ipv4: 192.168.103.9
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.15
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.21
      mask: 31
    Ethernet6: 
      ipv4: 192.168.103.27
      mask: 31
    Ethernet7: 
      ipv4: 192.168.103.33
      mask: 31
spine3-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.103
      mask: 32
    Ethernet2: 
      ipv4: 192.168.103.5
      mask: 31
    Ethernet3: 
      ipv4: 192.168.103.11
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.17
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.23
      mask: 31
    Ethernet6: 
      ipv4: 192.168.103.29
      mask: 31
    Ethernet7: 
      ipv4: 192.168.103.35
      mask: 31
leaf1-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.11
      mask: 32
    loopback1: 
      ipv4: 192.168.102.11
      mask: 32
    Ethernet3:
      ipv4: 192.168.103.0
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.2
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.4
      mask: 31
leaf2-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.12
      mask: 32
    loopback1: 
      ipv4: 192.168.102.11
      mask: 32
    Ethernet3:
      ipv4: 192.168.103.6
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.8
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.10
      mask: 31
leaf3-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.13
      mask: 32
    loopback1: 
      ipv4: 192.168.102.13
      mask: 32
    Ethernet3: 
      ipv4: 192.168.103.12
      mask: 31
    Ethernet4:
      ipv4: 192.168.103.14
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.16
      mask: 31
leaf4-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.14
      mask: 32
    loopback1: 
      ipv4: 192.168.102.13
      mask: 32
    Ethernet3: 
      ipv4: 192.168.103.18
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.20
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.22
      mask: 31
borderleaf1-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.21
      mask: 32
    loopback1: 
      ipv4: 192.168.102.21
      mask: 32
    Ethernet3: 
      ipv4: 192.168.103.24
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.26
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.28
      mask: 31
borderleaf2-DC1:
  interfaces:
    loopback0: 
      ipv4: 192.168.101.21
      mask: 32
    loopback1: 
      ipv4: 192.168.102.21
      mask: 32
    Ethernet3: 
      ipv4: 192.168.103.30
      mask: 31
    Ethernet4: 
      ipv4: 192.168.103.32
      mask: 31
    Ethernet5: 
      ipv4: 192.168.103.34
      mask: 31
"""

switches = yaml.safe_load(config)

for iface in switches[hostname]['interfaces']:
    print("interface %s") % iface
    #Pull variables into easier to use variables
    ip = switches[hostname]['interfaces'][iface]['ipv4']
    mask = switches[hostname]['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
    if "Ethernet" in iface:
        print " no switchport"

</pre>

Select a leaf or spine in the Form section, and click generate. You should see the EOS syntax with the specific IPs for that particular switch. 

## Apply the Configlet Builder 

Take this configlet builder and apply it to the Leaf and the Spine containers. 

Select the Leaf container, right click, and select configets. 

Select the Interface-Builder configlet on the left and click "Generate" in the middle. This will run this script against several of the switches, generating configurations. 

Click "Update" at the bottom. 

Repeat this process for the "Spines" container. 

When that is complete, click on "Save" on the bottom of the topology. This will generate several tasks. Create a change control for these tasks and execute it. 

Verify the interfaces are configured by going into the "Devices" tab at the top, selecting a leaf or spine, and looking at the running-config section. 

## Clean Up for the Next Labs

Once verification is complete, on the Spine and Leaf containers, remove the Interface-Builder configlet builder. This will remove all created configlets from this builder. Be sure to click "Update" and "Save", and run the tasks as a change control. 





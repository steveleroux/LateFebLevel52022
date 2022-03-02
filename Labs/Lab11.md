## Advanced Configlet Builder lab (Lab 11)


In this lab we will create an underlay in our topology via configlet builders. It will use both YAML and Python and while an understanding of both of these is ideal it isn't nessecary to complete the lab.

## Create Configlet Builder

In this lab yo will create a configlet builder that is capable of generating EOS configurations for the eBGP underly point-to-point ipv4 interfaces. 

This will be done in 3 steps: 

* Obtain the "hostname" variable from CVP
* Load a YAML file (data model) into a Python dictionary
* Loop through the interfaces section of the data model for a given switch an create EOS syntax for interface configuration



Create a configlet builder called "eBGP-Underlay-Builder".

Add the following to it:

<pre>
import yaml
config = """
leaf1:
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
switches = yaml.load(config)
print(switches['leaf1']['interfaces']['loopback0']['ipv4'])

</pre>

Select leaf1 then click "Generate".

You should see the IP address displayed of loopback0 on the right.

Replace the print statement with the following:

<pre>
for iface in switches['leaf1']['interfaces']:
#Iterate through all interfaces using iface variable as the incrementing index
    print("interface %s") % iface
#Pull variables into easier to use variables
    ip = switches['leaf1']['interfaces'][iface]['ipv4']
    mask = switches['leaf1']['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
</pre>


Click generate to show the config. This will loop through all interfaces and add the IP/mask.

*(Don't worry about the order, CloudVision will put them in the correct order when applied to the switch.)*

That's great, but the physical interfaces are default Layer 2. If you use this configuration by itself, it will not make IP addresses on the interfaces. You will need "no switchport". However, that command will error on the loopbacks.

Add an "if" statement in the for loop.

<pre>
#Iterate through all interfaces using iface variable as the incrementing index
for iface in switches['leaf1']['interfaces']:
    print("interface %s") % iface
    #Pull variables into easier to use variables
    ip = switches['leaf1-DC1']['interfaces'][iface]['ipv4']
    mask = switches['leaf1-DC1']['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
    #Check if the interface name contains "Ethernet", as it will need "no switchport"
    if "Ethernet" in iface:
        print " no switchport"
</pre>

#Generate the configuration.

<pre>
    interface Ethernet3
        ip address 192.168.103.0/31
        no switchport
    interface loopback0
        ip address 192.168.101.11/32
    interface loopback1
        ip address 192.168.102.11/32
    interface Ethernet4
        ip address 192.168.103.2/31
        no switchport
    interface Ethernet5
        ip address 192.168.103.4/31
        no switchport
</pre>

That looks better. You should be able to apply that to a particular switch. But we want to be able to apply this to multiple switches.

Add leaf2 to the YAML declaration:

<pre>

config = """
leaf1:
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
leaf2:
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
"""
</pre>

You can loop through the first element of this YAML file as well.

<pre>
#Iterate through all switches in the switches dictionary
for switch in switches:
    for iface in switches[switch]['interfaces']:
    #Iterate through all interfaces using iface variable as the incrementing index
    print("interface %s") % iface
    #Pull variables into easier to use variables
    ip = switches[switch]['interfaces'][iface]['ipv4']
    mask = switches[switch]['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
    if "Ethernet" in iface:
        print " no switchport"
</pre>

Now generate the configlet:

Iterating through all the switches isn't useful for this purpose however, so we need the configlet to generate just a single switch's configuration from the YAML file.

We will need to transfer the variable here (in the red box):

With this value you can specify the first key and obtain all the key value pairs underneath it.

We can get this from some variables provided by CloudVision:

Replace your configlet code with the following:
<pre>
from cvplibrary import CVPGlobalVariables, GlobalVariableNames
hostname = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SERIAL)
import yaml
from cvplibrary import CVPGlobalVariables, GlobalVariableNames
hostname = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SERIAL)
config = """
leaf1:
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
leaf2:
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
"""

switches = yaml.load(config)
for iface in switches[hostname]['interfaces']:
    #Iterate through all interfaces using iface variable as the incrementing index
    print("interface %s") % iface
    #Pull variables into easier to use variables
    ip = switches[hostname]['interfaces'][iface]['ipv4']
    mask = switches[hostname]['interfaces'][iface]['mask']
    print(" ip address %s/%s") % (ip, mask)
    if "Ethernet" in iface:
        print " no switchport"
</pre>

In the "Form Design" field on the left, select leaf1 and run the configlet generator. Then do the same for leaf2. It should generate individual configlets for each with the proper IP addresses.

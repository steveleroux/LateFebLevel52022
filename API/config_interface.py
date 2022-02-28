#!/usr/bin/python3

import pyeapi

switches = ['leaf1-DC1', 'leaf2-DC1', 'leaf3-DC1', 'leaf4-DC1']

for switch in switches:
    connect = pyeapi.connect_to(switch)
    
    interfaces = connect.api("interfaces").getall()
    for interface in interfaces:
        if interfaces[interface]['shutdown'] is False:
            print("The interface", interface, "on", switch, "is in 'no shut' state")
        else:
            print("The interface", interface, "on", switch, "is shutdown")

    # # Basically this is "no swithport" on Ethernet7
    # for vlan in range(10,100):
    #     result = connect.api("vlans").create(vlan)
    #     if result is True:
    #         print("VLAN", vlan," create for", switch)
    #     if result is False:
    #         print("Something went wrong with switch", switch)
    #     vlan_instance = connect.api("vlans").get(vlan)
    #     if vlan_instance['state'] == 'active':
    #         print("VLAN", vlan, "validated for", switch)

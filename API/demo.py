#!/usr/bin/python3

import yaml

# Variables

## Simple and Complex

### Simple variables

#### Integers

i = 1
j = 2

h = i + j


#### Strings

x = "This is Steve's"
y = ' world!'
m = x + y

#### Booleans

z = True


# Complex variables (lists, dictionaries)

planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# for planet in planets:
#     print(planet)

## Dictionaries

captains = {'1701': 'Kirk', '1701-D': 'Picard', '1864': 'Khan'}


### Dictionaries and YAML

config_yaml = open('config.yaml', 'r')

config = yaml.safe_load(config_yaml)

for switch in config:
  print('Interface configuration in EOS syntax for', switch, ':')
  for interface in config[switch]['interfaces']:
    print("interface", interface)
    print("  ip address", config[switch]['interfaces'][interface])


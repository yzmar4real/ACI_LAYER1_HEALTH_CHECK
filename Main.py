# import libraries and functions required for the code run

import acitoolkit.acitoolkit as aci
import sys
import acitoolkit
from acitoolkit import Session, Credentials, Node, ExternalSwitch
from Credential import apic_dc_ip1, apic_dc_ip2, apic_dc_ip3,apic_username, apic_password
from Legend import *
from datetime import datetime

# Creating the output files and including timestamps for the code run

file_list = ['L1_Output.txt', 'L1_Health.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("\nHealth Check Execution time is" + "  " + "[" + str(now) + "]\n")

# Create the storage containers for the outputs of the health computation

exceptions = []
percentage = []

# Define the connection parameters for the APIC

apic_url_dc = 'https://' + apic_dc_ip1

session = aci.Session(apic_url_dc, apic_username, apic_password)

# Connect to the APIC and retrieve the interfaces state using aci.Interface function

resp = session.login()

if not resp.ok:
    print("ERROR: Could not login into APIC: %s" % apic_url_dc)
    sys.exit(0)
else:
    print("SUCCESS: Logged into APIC: %s" % apic_url_dc)

interfaces = aci.Interface.get(session)

# Iterate through the interfaces captured, identify its characteristics (dn,operSt,if_name) and store in the list Output if its not up

for interface in interfaces:
    try:
        dn = interface.attributes['dn']
        operSt = interface.attributes['operSt']
        if_name = interface.attributes['if_name']
    except:
        print(str(dn) + "" + "Is not a main interface")
    
    else:
        if operSt != 'up':
           output.append(if_name)

# For each of the zones captured in the legend, compare the interface set with the output from the fabric, compute the percentage health and store the final value in the percentage and exceptions list

for zone in Zone_Agg:
    compare = set(zone).intersection(output)
    percentile = (100 - (len(compare)/len(zone))*100)
    percent = round(percentile,2)
    percentage.append(percent)
    exceptions.append(compare)

# Create a dictionary that captures all of the final output in JSON capable format and store all of the values

Final_Dict = {}

j = 0
while j < len(Zone_DC_Names):
   Final_Dict[Zone_DC_Names[j]] = {"Health_Status": percentage[j], "Exception List": exceptions[j]}
   j += 1

# Create a dictionary that captures all of the final output in JSON capable format and store all of the values

avg_SF_HC = sum(percentage)/len(percentage)
ServerFarm_HealthCheck = round(avg_SF_HC,2)
Exceptions_SF = exceptions

# Compute the final results and store in a text file L1_Health and L1_Output

with open('L1_Health.txt', 'a') as f:
    f.write("******************************* L1 HEALTH CHECK REPORT **********************************************\n\n")
    f.write("******************************* EXECUTIVE SUMMARY DASHBOARD******************************************\n\n")
    f.write("Health Check Report for SERVER FARM AGG is :" + str(ServerFarm_HealthCheck) + "%" + "\n\n")
    f.write("******************************* SERVER FARM DETAIL REPORT  **********************************************\n\n")

for name in Final_Dict.keys():
    with open('L1_Health.txt', 'a') as f:
       f.write("Health Check Report for" + "  " + str(name) + " " + "is :" + " " + " at  Health Percentage" + "  "  + "  " + str(Final_Dict[name]['Health_Status']) + "%" + "   " + "\n\n")
    

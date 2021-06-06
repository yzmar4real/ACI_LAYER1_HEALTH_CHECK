
### APIC FABRIC VARIABLES #######

## THE INTERFACES SHOULD BE REPLACED WITH ACTUAL INTERFACES OF INTEREST IN YOUR TOPOLOGY

zone_A = ['eth 1/203/1/1', 'eth 1/203/1/2', 'eth 1/203/1/3', 'eth 1/203/1/4', 'eth 1/203/1/5']
zone_B = ['eth 1/203/1/6', 'eth 1/203/1/7', 'eth 1/203/1/8', 'eth 1/203/1/9', 'eth 1/203/1/10']

#### Dictionary to capture all of the health criteria  #######

### These should reflect the variables under the section above

Zone_DC_Names = ['zone_A','zone_B']
Zone_Agg = [zone_A,zone_B]

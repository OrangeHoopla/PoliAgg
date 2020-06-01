##loading screen
import time, sys
import xml.etree.ElementTree as ET
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loading():



    print(bcolors.WARNING + "Installing virus..." + bcolors.ENDC)
    for i in range(0, 100):
        time.sleep(0.1)
        sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
        sys.stdout.flush()
    print('')
    
tree = ET.parse('../../Music/committee_memberships_SSAP.xml')
root = tree.getroot()
Name = root[0][1].text
members = root[0][3].text
test = root[0][3][0][0][0].text
print(test)
loading()

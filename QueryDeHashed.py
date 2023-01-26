import requests
import json
import sys
from termcolor import colored
from requests.auth import HTTPBasicAuth

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

email = ''
api_key = ''
domain = ''
enable_debugging = False

banner = """
██████╗ ███████╗██╗  ██╗ █████╗ ███████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
██║  ██║█████╗  ███████║███████║███████╗███████║█████╗  ██║  ██║
██║  ██║██╔══╝  ██╔══██║██╔══██║╚════██║██╔══██║██╔══╝  ██║  ██║
██████╔╝███████╗██║  ██║██║  ██║███████║██║  ██║███████╗██████╔╝
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ 
                                                                
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗                     
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║                     
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║                     
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║                     
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║                     
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝                                                                                                                                                        
"""

def query_dehashed(key, debug):
    
    url = 'https://api.dehashed.com/search?query=' + domain
    
    headers = {
        'Accept': 'application/json',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.3538.77 Safari/537.36',
    }

    response = requests.request(method='GET', url=url, auth=HTTPBasicAuth(email,key), headers=headers, verify=False)
    decodedResponse = json.loads(response.text)

    if debug == True:
        print(decodedResponse['entries'])
    elif debug == False:
        for entry in decodedResponse['entries']:
            print(colored("Email: ", 'green') + entry['email'])
            print(colored("Username: ", 'green') + entry['username'])
            print(colored("Password: ", 'green') + entry['password'])
            print(colored("Password Hash: ", 'green') + entry['hashed_password'])
            print(colored("Database: ", 'green') + entry['database_name'])
            print("")
    
    print("Total Identities found:\t" + str(decodedResponse['total']))
    print("API Query Balance:\t" + str(decodedResponse['balance']))

usage = """
QueryDeHashed.py will make an API request to dehashed.com to query if a given domain has been victim to any databreaches. 
This script is useful try and find leaked credentals or emails durinig the reconnaissance phase.

--domain\t domain to query
--debug\t\t enable debugging (prints out raw json)

C:\Tools\Scripts> python .\QueryDeHashed.py --domain example.com 
C:\Tools\Scripts> python .\QueryDeHashed.py --domain example.com --debug
"""

if len(sys.argv) == 3:
    if sys.argv[1] == '--domain':
        domain = sys.argv[2] 
        print(colored(banner, 'blue'))
        query_dehashed(api_key, enable_debugging)
    else:
        print(colored(banner, 'blue'))
        print(usage)
elif len(sys.argv) == 4:
    if sys.argv[1] == '--domain' and sys.argv[3] == '--debug':
        domain = sys.argv[2] 
        enable_debugging = True
        print(colored(banner, 'blue'))
        query_dehashed(api_key,enable_debugging)
    else:
        print(colored(banner, 'blue'))
        print(usage)
    
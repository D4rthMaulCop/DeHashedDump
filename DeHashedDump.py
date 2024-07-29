import requests
import json
import sys
import csv
from termcolor import colored
from requests.auth import HTTPBasicAuth

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

email = '' # chamge me
api_key = '' # change me

domain = '' # no need to change
debug = False # no need to change
output_csv = False # no need to change

banner = """
 _____     ______     __  __     ______     ______     __  __     ______     _____       
/\  __-.  /\  ___\   /\ \_\ \   /\  __ \   /\  ___\   /\ \_\ \   /\  ___\   /\  __-.     
\ \ \/\ \ \ \  __\   \ \  __ \  \ \  __ \  \ \___  \  \ \  __ \  \ \  __\   \ \ \/\ \    
 \ \____-  \ \_____\  \ \_\ \_\  \ \_\ \_\  \/\_____\  \ \_\ \_\  \ \_____\  \ \____-    
  \/____/   \/_____/   \/_/\/_/   \/_/\/_/   \/_____/   \/_/\/_/   \/_____/   \/____/    
                                                                                         
 _____     __  __     __    __     ______                                                
/\  __-.  /\ \/\ \   /\ "-./  \   /\  == \                                               
\ \ \/\ \ \ \ \_\ \  \ \ \-./\ \  \ \  _-/                                               
 \ \____-  \ \_____\  \ \_\ \ \_\  \ \_\                                                 
  \/____/   \/_____/   \/_/  \/_/   \/_/                                                                                                                                                      
"""

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Username', 'Password', 'Phone', 'Hashed Password', 'Database Name'])
        for entry in data:
            writer.writerow([entry['email'], entry['username'], entry['password'], entry['phone'], entry['hashed_password'], entry['database_name']])

def query_dehashed(key = "", debug = False, csv_export = False):

    url = 'https://api.dehashed.com/search?query=' + domain + '&size=10000'
    
    headers = {
        'Accept': 'application/json',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.3538.77 Safari/537.36',
    }

    response = requests.request(method='GET', url=url, auth=HTTPBasicAuth(email,key), headers=headers, verify=False)
    decodedResponse = json.loads(response.text)

    if debug == True:
        print(decodedResponse['entries'])
    elif csv_export == True:
        export_to_csv(decodedResponse['entries'], 'dehashed_results.csv')
    elif debug == False:
        for entry in decodedResponse['entries']:
            print(colored("Email: ", 'green') + entry['email'])
            print(colored("Username: ", 'green') + entry['username'])
            print(colored("Password: ", 'green') + entry['password'])
            print(colored("Phone: ", 'green') + entry['phone'])
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
--csv\t\t output results to csv file

C:\Tools\Scripts> python .\QueryDeHashed.py --domain example.com 
C:\Tools\Scripts> python .\QueryDeHashed.py --domain example.com --debug
"""

if len(sys.argv) == 3:
    if sys.argv[1] == '--domain':
        domain = sys.argv[2] 
        print(colored(banner, 'blue'))
        query_dehashed(api_key, debug)
    else:
        print(colored(banner, 'blue'))
        print(usage)
elif len(sys.argv) == 4:
    if sys.argv[1] == '--domain' and sys.argv[3] == '--debug':
        domain = sys.argv[2] 
        debug = True
        print(colored(banner, 'blue'))
        query_dehashed(api_key,debug)
    if sys.argv[1] == '--domain' and sys.argv[3] == '--csv':
        domain = sys.argv[2] 
        output_csv = True
        print(colored(banner, 'blue'))
        query_dehashed(api_key, debug, output_csv)
else:
    print(colored(banner, 'blue'))
    print(usage)    
    

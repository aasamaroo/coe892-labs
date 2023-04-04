import requests
import json
from dotenv import load_dotenv

#retrieve url from .env file
# load_dotenv()
# URL = os.getenv('URL')

baseurl = "http://localhost:8000"


def printJson(object):
    text = json.dumps(object, sort_keys=True, indent=4)
    print(text)



def run():
    i = -1
    while i != 0:
        i = input("Use one of the following commands:\n1: Map Options\n2: Mine Options\n3: Rover Options\n0: Exit Program\n")
        if i == "0":
            break;
        elif i == "1":
            mapOption = input("Which map option would you like?\n1: View Map\n2: Update Map\n3: Go Back\n0: Exit Program\n")
            if mapOption == "1":
                response = requests.get(baseurl+"/map")
                print("This is the current map:\n")
                printJson(response.json())
            elif mapOption == "2":
                cols, rows = input("Enter the new desired number of columns and rows: ").split()
                cols = int(cols)
                rows = int(rows)
                payload = {'cols': cols, 'rows': rows}
                headers = {"Content-Type": "application/json"}
                newMap = requests.put(baseurl+"/map", params=payload)
                print(newMap.text)
            elif mapOption == "0":
                break;
        elif i == "2":
            mineOption = input()



if __name__ == '__main__':
    run()

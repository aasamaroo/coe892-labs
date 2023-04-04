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
                newMap = requests.put(baseurl+"/map", params=payload)
                print(newMap.text)
            elif mapOption == "0":
                break;
        elif i == "2":
            mineOption = input("Which mine option would you like?\n1: View all Mines\n2: View a Specific Mine\n3: Delete a Mine\n4: Add a Mine\n5: Update a Mine\n6: Go Back\n0: Exit Program\n")
            if mineOption == "1":
                response = requests.get(baseurl+"/mines")
                print("These are all of the present Mines:\n")
                printJson(response.json())
            elif mineOption == "2":
                mineNo = input("Enter the ID of the Mine you wish to view: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.get(baseurl+"/mines/"+mineNo)
                print(mine.text)
            elif mineOption == "3":
                mineNo = input("Enter the ID of the Mine you wish to delete: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.delete(baseurl+"/mines/"+mineNo)
                print(mine.text)
            elif mineOption == "4":
                mineNo = input("Enter the ID of the Mine you wish to add: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.post(baseurl+"/mines", params=payload)
                print(mine.text)
            elif mineOption == "5":
                mineNo = input("Enter the ID of the Mine you wish to update: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.put(baseurl+"/mines/"+mineNo, params=payload)
                print(mine.text)



if __name__ == '__main__':
    run()

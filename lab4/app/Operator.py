import requests
import json
import os
from dotenv import load_dotenv

#retrieve url from .env file
load_dotenv()
URL = os.getenv('URL')

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

#All of the map functionalities

        elif i == "1":
            mapOption = input("Which map option would you like?\n1: View Map\n2: Update Map\n3: Go Back\n0: Exit Program\n")
            if mapOption == "1": #GET request for map
                response = requests.get(baseurl+"/map")
                print("This is the current map:\n")
                printJson(response.json())
            elif mapOption == "2": #PUT request to update the map
                cols, rows = input("Enter the new desired number of columns and rows: ").split()
                cols = int(cols)
                rows = int(rows)
                payload = {'cols': cols, 'rows': rows}
                newMap = requests.put(baseurl+"/map", params=payload)
                print(newMap.text)
            elif mapOption == "0":
                break;

#All of the Mine functionalities

        elif i == "2":
            mineOption = input("Which mine option would you like?\n1: View all Mines\n2: View a Specific Mine\n3: Delete a Mine\n4: Add a Mine\n5: Update a Mine\n6: Go Back\n0: Exit Program\n")
            if mineOption == "1": #GET request for list of all mines
                response = requests.get(baseurl+"/mines")
                print("These are all of the present Mines:\n")
                printJson(response.json())
            elif mineOption == "2": #GET request for specific mine
                mineNo = input("Enter the ID of the Mine you wish to view: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.get(baseurl+"/mines/"+mineNo)
                printJson(mine.json())
            elif mineOption == "3": #DELETE request to delete a mine
                mineNo = input("Enter the ID of the Mine you wish to delete: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.delete(baseurl+"/mines/"+mineNo)
                print(mine.text)
            elif mineOption == "4": #POST request to add a mine
                mineNo = input("Enter the ID of the Mine you wish to add: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.post(baseurl+"/mines", params=payload)
                print(mine.text)
            elif mineOption == "5": #PUT request to update a mine
                mineNo = input("Enter the ID of the Mine you wish to update: ")
                mineNum = int(mineNo)
                payload = {'mine_id': mineNum}
                mine = requests.put(baseurl+"/mines/"+mineNo, params=payload)
                print(mine.text)

#All of the Rover Functionalities

        elif i == "3":
            roverOption = input("Which rover option would you like?\n1: View all Rovers\n2: View a Specific Rover\n3: Create a New Rover\n4: Delete a Specified Rover\n5: Send a list of commands to a Rover\n6: Dispatch a Specified Rover\n7: View logs of a Specified Rover\n8: Go Back\n0: Exit Program\n")
            if roverOption == "1": #GET all rovers
                response = requests.get(baseurl+"/rovers")
                print("These are all of the present Rovers:\n")
                printJson(response.json())
            elif roverOption == "2": #GET rover of specified ID
                roverNo = input("Enter the ID of the Rover you wish to view: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.get(baseurl+"/rovers/"+roverNo)
                printJson(rover.json())
            elif roverOption == "3": #POST add new rover of specified ID
                roverNo = input("Enter the ID of the Rover you wish to add: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.post(baseurl+"/rovers", params=payload)
                print(rover.text)
            elif roverOption == "4": #DELETE rover of specified ID
                roverNo = input("Enter the ID of the Rover you wish to delete: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.delete(baseurl+"/rovers/"+roverNo)
                print(rover.text)
            elif roverOption == "5": #PUT update commands in rover
                roverNo = input("Enter the ID of the Rover you wish to update: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.put(baseurl+"/rovers/"+roverNo, params=payload)
                print(rover.text)
            elif roverOption == "6": #POST dispatch a rover
                roverNo = input("Enter the ID of the Rover you wish to dispatch: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.post(baseurl+"/rovers/"+roverNo+"/dispatch", params=payload)
                print(rover.text)
            elif roverOption == "7": #GET logs of a rover
                roverNo = input("Enter the ID of the Rover you wish to update: ")
                roverNum = int(roverNo)
                payload = {'rover_id': roverNum}
                rover = requests.get(baseurl+"/rovers/"+roverNo+"/logs", params=payload)
                print(rover.text)
            elif roverOption == "0":
                break;
    print("Try not to blow up!")


if __name__ == '__main__':
    run()

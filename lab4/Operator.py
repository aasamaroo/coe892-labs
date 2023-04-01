#----------------------------------------------------
#
#          COE892 Lab 4/5: FastAPI
#                 Main.py
#       Made by Anand Alexander Samaroo
#             Github: aasamaroo
#
#-----------------------------------------------------

import requests
import json
import hashlib
import sys
from fastapi import FastAPI, HTTPException
from typing import List, Tuple
from pydantic import BaseModel
from random import randint

app = FastAPI()


#------------------------------------------
#      Rover, and Mine Objects
#------------------------------------------

class Rover(BaseModel):
    id: int
    data: str
    status: str
    xpos: int
    ypos: int

#db to store all rovers
rovers_db = {}

class Mine(BaseModel):
    xpos: int
    ypos: int
    isDefused: bool = False
    serialNum: int
    id: int

#db to store all mines
mines_db = {}

#--------------------------------------------------
#
#                 Map functions
#
#--------------------------------------------------

#GET: Get the map from reading the map.txt file (similar to lab 2)
@app.get('/map')
def getMap():
    with open("map.txt", 'r') as f:
        q = open("map.txt", "r")
        map = []
        arr = []
        for line in q:
            stripedL = line.rstrip()
            row = stripedL.split(' ')
            map.append(row)
        w = 0
        for i in map:
            if w >= 1:
                arr.append(i)
            w = w + 1
    map = str(arr)
    rows = 4
    cols = 6
    return map


#PUT: Update height and width of field
@app.put('/map')
def updateField(cols: int, rows: int):
    map_data = [[0] * cols for _ in range(rows)]
    with open("map.txt", "w") as f:
        f.write(f"{rows} {cols}\n")
        for row in map_data:
            f.write(" ".join(str(x) for x in row) + "\n")
    return {"Message": "The map has been successfully updated."}

#--------------------------------------------------
#
#                 Mine functions
#
#--------------------------------------------------

#GET: Retrieve list of mines with their coordinates and serial numbers
@app.get('/mines')
def retrieveListMines():
    return list(mines_db.values())

#GET: Retrieve specified mine with serial number and coordinates
#Throws exception if Mine not found (404 error)
@app.get('/mines/{mine_id}')
def retrieveMine(mine_id: int):

#Check if the mine with the specified ID is in the database
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")
#Retrieve the mine
    return mines_db[mine_id]




#DELETE: Delete a mine specified by their ID
#Throws 404 error if Mine not found
@app.delete('/mines/{mine_id}')
def deleteMine(mine_id: int):

#Check if the mine with the specified ID is in the database
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")

#Delete the specified mine
    del mines_db[mine_id]
    return {"message": f"Mine {mine_id} has been successfully deleted"}




#POST: Create a new mine
@app.post('/mines')
def addMine(mine: Mine):

# Check if mine with same ID already exists
    if mine.id in mines_db:
        return {"error": "Rover with the same ID already exists"}

# Add mine to database
    mines_db[mine.id] = mine
    return {"message": f"Mine {mine.id} created successfully"}




#PUT: Update a mine
#404 error if Mine not found
@app.put('/mines/{mine_id}')
def updateMine(mine_id: int):

#Check if a mine with the specified ID exists
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")

#Check if the mine has already been defused
    elif mines_db[mine_id].isDefused == True:
        raise HTTPException(status_code=405, detail="Mine has been defused. CTs Win!")

#Put the mine in a random spot on the map (Must be within bounds of the map)
    map_grid = getMap()
    map_grid = map_grid[1: -1:]
    xmax = len(map_grid)
    ymax = len(map_grid[0])
    mines_db[mine_id].xpos = randint(0,xmax)
    mines_db[mine_id].ypos = randint(0,ymax)
    return {"message": f"Mine {mine_id} updated successfully."}
#--------------------------------------------------
#
#                 Rover functions
#
#--------------------------------------------------

#GET: Retrieve list of ALL rovers
@app.get('/rovers')
def retrieveListRovers():
    return list(rovers_db.values())

#GET: Retrieve rover specified by ID number
#Throw exception if Rover not found (404 error)
@app.get('/rovers/{rover_id}')
def retrieveRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    return rovers_db[rover_id]

#POST: Create new rover
@app.post('/rovers')
def addRover(rover: Rover):
    # Check if rover with same ID already exists
    if rover.id in rovers_db:
        return {"error": "Rover with the same ID already exists"}
    # Add rover to database
    rovers_db[rover.id] = rover
    return {"message": f"Rover {rover.id} created successfully"}

#Delete: Deletes rover specified by ID
#Throws 404 error if Rover not found
@app.delete('/rovers/{rover_id}')
def deleteRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    del rovers_db[rover_id]
    return {"message": f"Rover {rover_id} has been successfully deleted"}

#PUT: Send list of commands to Rover
#404 error if Rover not found
#Error thrown if Rover Status is "Not Started", or "Finished"
@app.put('/rovers/{rover_id}')
def updateRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    elif rovers_db[rover_id].status == 'Active':
        raise HTTPException(status_code=405, detail="Rover is active")
    # Update the rover object in the database
    response = requests.get('https://coe892.reev.dev/lab1/rover/' + str(rover_id))
    data = json.loads(response.text)
    moves = str([data["data"]["moves"]])
    rovers_db[rover_id].data = moves
    return {"message": f"Rover {rover_id} updated successfully."}


def getMinePIN(x: int, y: int):
    for mine in mines_db:
        if mines_db[mine].xpos == x and mines_db[mine].ypos == y:
            serialNum = mines_db[mine].serialNum
            pin = randint(0,20)
            tempMineKey = str(pin) + str(serialNum)
            encode = tempMineKey.encode()
            hash = hashlib.sha256(encode).hexdigest()
            mines_db[mine].isDefused = True
            return hash
        else:
            return -1


@app.post('/rovers/{rover_id}/dispatchtest')
def dispatchRover(rover_id: int):
    sys.setrecursionlimit(10**6)
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    elif rovers_db[rover_id].status == "Finished":
        raise HTTPException(status_code=405, detail="Rover is finished")
    rovers_db[rover_id].status = "Ready"
    run(rover_id)
    return {"rover_id": rover_id}


def checkForMine(x: int, y: int):
    result = False
    for i in mines_db:
        if mines_db[i].xpos == x and mines_db[i].ypos == y:
            result = True
    return result

def run(rover: int):
        class Pos:
            xpos = rovers_db[rover].xpos
            ypos = rovers_db[rover].ypos

            def __init__(self, x, y):
                Pos.xpos = Pos.xpos + x
                Pos.ypos = Pos.ypos + y


        #for i in range(1, 11):
        i = -1
        while i != 0:
            i = str(rover)
            if i == "0":
                break
            arr = getMap()
            arr = arr[1: -1:]
            arr2 = ""
            for c in arr:
                if c == "0" or c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" or c == "0" or c == ",":
                    arr2 = (arr2 + c)
            arr2 = list(arr2.split(","))
            # arr has all the values of the map in a list
            arr = [arr2[x:x + 6] for x in range(0, len(arr2), 6)]
            #print(arr[0])

            # Start of the main code block
            print("Rover number " + str(i) + " start:")
            Pos.xpos = 0
            Pos.ypos = 0
            arr2 = [["", "", "", "", "", ""],
                    ["", "", "", "", "", ""],
                    ["", "", "", "", "", ""],
                    ["", "", "", "", "", ""]]

            # Starting position for all rovers
            arr2[0][0] = "*"

            val = rovers_db[rover].data
            print("Commands:" + val)
            t = 0

            for q in val:
                dug = val[t + 1]
                if t < len(val) - 2:
                    t = t + 1
                dugged = 0
                if dug == "D":
                    dugged = 1
                if q == "M":
                    print("Move Forward")
                    if (Pos.xpos + 1 < 0) or (Pos.xpos + 1 >= len(arr)) or (Pos.ypos < 0) or (Pos.ypos >= len(arr[0])):
                        print("Cant move forward, stay in the current spot")
                        pass
                    else:
                        if checkForMine(Pos.xpos + 1,Pos.ypos):
                            if dugged == 1:
                                print("dig")
                                pos = arr[Pos.xpos + 1][Pos.ypos]

                                hash = getMinePIN(Pos.xpos+1, Pos.ypos)
                                print("Pin number of the mine: "+hash)
                                # val = hash(int(arr[Pos.xpos + 1][Pos.ypos]))
                                print(str(hash))
                                arr[Pos.xpos + 1][Pos.ypos] = "0"
                                Pos(1, 0)
                                arr2[Pos.xpos][Pos.ypos] = "*"
                                continue
                            print("mine exploded")
                            Pos(1, 0)
                            print("Current Position: [" + str(Pos.xpos) + "," + str(Pos.ypos) + "]")
                            arr[Pos.xpos][Pos.ypos] = "0"
                            arr2[Pos.xpos][Pos.ypos] = "*"
                            break
                        else:
                            print("safe")
                            Pos(1, 0)
                            arr2[Pos.xpos][Pos.ypos] = "*"

                elif q == "L":
                    print("Turn Left")
                    if (Pos.xpos < 0) or (Pos.xpos >= len(arr)) or (Pos.ypos - 1 < 0) or (Pos.ypos - 1 >= len(arr[0])):
                        print("Cant turn left, stay in the current spot")
                        pass
                    else:
                        if checkForMine(Pos.xpos,Pos.ypos - 1):
                            if dugged == 1:
                                print("dig")
                                pos = arr[Pos.xpos][Pos.ypos-1]
                                hash = getMinePIN(Pos.xpos, Pos.yos-1)
                                print("Pin number of the mine: "+hash)
                                # val = hash(int(arr[Pos.xpos - 1][Pos.ypos]))

                                arr[Pos.xpos][Pos.ypos - 1] = "0"
                                Pos(0, -1)
                                arr2[Pos.xpos][Pos.ypos] = "*"
                                continue
                            print("mine exploded")
                            Pos(0, -1)
                            arr2[Pos.xpos][Pos.ypos] = "*"
                            print("Current Position: [" + str(Pos.xpos) + "," + str(Pos.ypos) + "]")
                            arr[Pos.xpos][Pos.ypos] = "0"
                            break
                        else:
                            print("safe")
                            Pos(0, -1)
                            arr2[Pos.xpos][Pos.ypos] = "*"

                elif q == "R":
                    print("Turn Right")
                    if (Pos.xpos < 0) or (Pos.xpos >= len(arr)) or (Pos.ypos + 1 < 0) or (Pos.ypos + 1 >= len(arr[0])):
                        print("Cant turn right, stay in the current spot")
                        pass
                    else:
                        if checkForMine(Pos.xpos,Pos.ypos + 1):
                            if dugged == 1:
                                print("dig")
                                pos = arr[Pos.xpos][Pos.ypos + 1]


                                pin = getMinePIN(Pos.xpos,Pos.ypos + 1)
                                print("Pin number of the mine: "+pin)

                                arr[Pos.xpos][Pos.ypos + 1] = "0"
                                Pos(0, 1)
                                arr2[Pos.xpos][Pos.ypos] = "*"
                                continue
                            print("mine exploded")
                            Pos(0, 1)
                            arr2[Pos.xpos][Pos.ypos] = "*"
                            print("Current Position: [" + str(Pos.xpos) + "," + str(Pos.ypos) + "]")
                            arr[Pos.xpos][Pos.ypos] = "0"
                            break
                        else:
                            print("safe")
                            Pos(0, 1)
                            arr2[Pos.xpos][Pos.ypos] = "*"

                print("Current Position: [" + str(Pos.xpos) + "," + str(Pos.ypos) + "]")
            print("Rover number " + str(i) + " completed")
            print("")
            print("Status of the 2D Array:")
            for a in arr:
                print(a)
            print("")
            print("Path of Rover number " + str(i) + ":")
            f = open("path_" + str(i) + ".txt", "w+")
            for b in arr2:
                f.write(str(b) + "\n")
                print(b)
            f.close()
            if q == "C":
                rovers_db[rover].status = "Finished"
            print("_______________________________________________")
            break
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
#      Map, Rover, and Mine Objects
#------------------------------------------

#Todo: Create objects for Map, Rover, and Mines
class Map(BaseModel):
    data: List[List[int]]



class Rover(BaseModel):
    id: int
    data: str
    status: str
    xpos: int
    ypos: int
    direction: str

#db to store all rovers
rovers_db = {}

class Mine(BaseModel):
    xpos: int
    ypos: int
    isDefused: bool = False
    serialNum: int
    id: int

mines_db = {}

#--------------------------------------------------
#
#                 Map functions
#
#--------------------------------------------------

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
    return map


#PUT: Update height and width of field
@app.put('/map')
def updateField(map_data: Map):
    with open("map.txt", "w") as f:
        for row in map_data.data:
            f.write(" ".join(str(cell) for cell in row))
            f.write("\n")
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
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")
    return mines_db[mine_id]

#DELETE: Delete a mine specified by their ID
#Throws 404 error if Mine not found
@app.delete('/mines/{mine_id}')
def deleteMine(mine_id: int):
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")
    del mines_db[mine_id]
    return {"message": f"Mine {mine_id} has been successfully deleted"}

#POST: Create a new mine
@app.post('/mines')
def addMine(mine: Mine):
    # Check if rover with same ID already exists
    if mine.id in mines_db:
        return {"error": "Rover with the same ID already exists"}
    # Add rover to database
    mines_db[mine.id] = mine
    return {"message": f"Rover {mine.id} created successfully"}

#PUT: Update a mine
#404 error if Mine not found
@app.put('/mines/{mine_id}')
def updateMine(mine_id: int):
    if mine_id not in mines_db:
        raise HTTPException(status_code=404, detail="Mine not found")
    elif mines_db[mine_id].isDefused == True:
        raise HTTPException(status_code=405, detail="Mine has been defused. CTs Win!")
    mines_db[mine_id].xpos = randint(1,5)
    mines_db[mine_id].ypos = randint(1,5)
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


#POST: Dispatch Rover with specified ID
@app.post('/rovers/{rover_id}/dispatch')
def dispatchRover(rover_id: int):
    sys.setrecursionlimit(10**6)
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    elif rovers_db[rover_id].status == "Finished":
        raise HTTPException(status_code=405, detail="Rover is finished")
    rovers_db[rover_id].status = "Ready"
    move_rover(rover_id)
    return {"rover_id": rover_id}


def move_rover(rover_id: int):
    commands = rovers_db[rover_id].data
    for i in range(len(commands)):
        if commands[i] == "M":
            move_forward(rover_id)
        elif commands[i] == "L":
            turn_left(rover_id)
        elif commands[i] == "R":
            turn_right(rover_id)
        elif commands[i] == "D":
            dig(rover_id)
        else:
            raise ValueError(f"Invalid command")


def move_forward(rover_id):
    if (Pos.xpos + 1 < 0) or (Pos.xpos + 1 >= len(arr)) or (Pos.ypos < 0) or (Pos.ypos >= len(arr[0])):
        pass
    else:
        if rovers_db[rover_id].direction == "N":
            rovers_db[rover_id].ypos += 1
        elif rovers_db[rover_id].direction == "E":
            rovers_db[rover_id].xpos += 1
        elif rovers_db[rover_id].direction == "S":
            rovers_db[rover_id].ypos -= 1
        elif rovers_db[rover_id].direction == "W":
            rovers_db[rover_id].xpos -= 1

def turn_left(rover_id: int):
    if rovers_db[rover_id].direction == "N":
        rovers_db[rover_id].direction = "W"
    elif rovers_db[rover_id].direction == "W":
        rovers_db[rover_id].direction = "S"
    elif rovers_db[rover_id].direction == "S":
        rovers_db[rover_id].direction = "E"
    elif rovers_db[rover_id].direction == "E":
        rovers_db[rover_id].direction = "N"

def turn_right(rover_id: int):
    if rovers_db[rover_id].direction == "N":
        rovers_db[rover_id].direction = "E"
    elif rovers_db[rover_id].direction == "E":
        rovers_db[rover_id].direction = "S"
    elif rovers_db[rover_id].direction == "S":
        rovers_db[rover_id].direction = "W"
    elif rovers_db[rover_id].direction == "W":
        rovers_db[rover_id].direction = "N"

def dig(rover_id):
    x = rovers_db[rover_id].xpos
    y = rovers_db[rover_id].ypos
    for mine in mines_db:
        if mines_db[mine].xpos == x and mines_db[mine].ypos == y:
            serialNum = getMineSerialNum(x,y)
            pin = getMinePIN(x,y)
            mines_db[mine].isDefused = True
            return {"message": f"Defused mine with Serial Number {serialNum}, and PIN {pin}"}
        else:
            return {"message": f"No mine here!"}


def getMineSerialNum(x: int, y: int):
    for mine in mines_db:
        if mines_db[mine].xpos == x and mines_db[mine].ypos == y:
            serialNum = mines_db[mine].serialNum
            return serialNum

def getMinePIN(x: int, y: int):
    for mine in mines_db:
        if mines_db[mine].xpos == x and mines_db[mine].ypos == y:
            serialNum = mines_db[mine].serialNum
            pin = randint(0,20)
            tempMineKey = str(pin) + str(serialNum)
            encode = tempMineKey.encode()
            hash = hashlib.sha256(encode).hexdigest()
            return hash
        else:
            return -1
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

map_grid = []

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
    pin: int

mines_db = {}

#--------------------------------------------------
#
#                 Map functions
#
#--------------------------------------------------

#GET: Retrieve 2D array of the field
#@app.get('/map')
#def getMap():
#    with open("map.txt", "r") as f:
#        map_data = f.read()
#    return {"Map": map_data}

@app.get('/map')
def getMap():
    with open("map.txt", 'r') as f:
        map_lines = f.readlines()
    map_lines = [line.strip() for line in map_lines]
    map_grid = [list(line) for line in map_lines]
    return map_grid


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
def addMine(mine_data: Mine):
    mine_id = len(mines_db) + 1
    mine = Mine(id=mine_id, **mine_data.dict())
    mine.serialNum = randint(100, 999)
    mine.pin = randint(1000, 9999)
    mines_db[mine_id] = mine
    return mine

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
def addRover(rover_data: Rover):
    rover_id = len(rovers_db) + 1
    rover = Rover(id=rover_id, **rover_data.dict())
    rovers_db[rover_id] = rover
    return rover

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
    elif rovers_db[rover_id].status == 'NotStarted':
        raise HTTPException(status_code=405, detail="Rover has not started")
    elif rovers_db[rover_id].status == 'Finished':
        raise HTTPException(status_code=405, detail="Rover is finished")
    # Update the rover object in the database
    response = requests.get('https://coe892.reev.dev/lab1/rover/' + str(rover_id))
    data = response.text
    parse_json = json.loads(data)
    moves = parse_json['data']['moves']
    rovers_db[rover_id].data = moves
    return {"message": f"Rover {rover_id} updated successfully."}


#POST: Dispatch Rover with specified ID
@app.post('/rovers/{rover_id}/dispatch')
def dispatchRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    elif rovers_db[rover_id].status == "Finished":
        raise HTTPException(status_code=405, detail="Rover is finished")
    rovers_db[rover_id].status = "Ready"
    roverMovement(rover_id)
    return {"rover_id": rover_id}

def roverMovement(rover_id: int):
    #todo: Create function that handles movement of rover.
    #This function will be called in dispatchRover()
    commands = rovers_db[rover_id].data
    for i in range(len(commands)):
        if(commands[i] == 'M'):
            moveForward(rover_id)
        elif(commands[i] == 'L'):
            rovers_db[rover_id].direction = turnLeft(rovers_db[rover_id].direction)
        elif(commands[i] == 'R'):
            rovers_db[rover_id].direction = turnRight(rovers_db[rover_id].direction)
        elif(commands[i] == 'D'):
            x = rovers_db[rover_id].xpos
            y = rovers_db[rover_id].ypos
            if(getMineID(x,y) != -1):
                print("Mine has been defused! CTs Win!")
                print("PIN of Defused Mine is ", getMineID(x,y))
            else:
                print("No Mine here!")


def moveForward(rover_id: int):
    try:
        if(rovers_db[rover_id].direction == 'North'):
            xnew = rovers_db[rover_id].xpos
            ynew = rovers_db[rover_id].ypos + 1
            if(map_grid[xnew][ynew] != '#'):
                rovers_db[rover_id].ypos = ynew

        elif(rovers_db[rover_id].direction == 'South'):
            xnew = rovers_db[rover_id].xpos
            ynew = rovers_db[rover_id].ypos - 1
            if(map_grid[xnew][ynew] != '#'):
                rovers_db[rover_id].ypos = ynew

        elif(rovers_db[rover_id].direction == "East"):
            xnew = rovers_db[rover_id].xpos + 1
            ynew = rovers_db[rover_id].ypos
            if(map_grid[xnew][ynew] != '#'):
                rovers_db[rover_id].xpos = xnew

        elif(rovers_db[rover_id].direction == "West"):
            xnew = rovers_db[rover_id].xpos - 1
            ynew = rovers_db[rover_id].ypos
            if(map_grid[xnew][ynew] != '#'):
                rovers_db[rover_id].xpos = xnew
    except IndexError:
        print("Index Out of Range")


def turnLeft(rover_id: int):
    if (rovers_db[rover_id].direction == 'North'):
        rovers_db[rover_id].direction = 'West'
    elif (rovers_db[rover_id].direction == 'East'):
        rovers_db[rover_id].direction = 'North'
    elif (rovers_db[rover_id].direction == 'South'):
        rovers_db[rover_id].direction = 'East'
    elif (rovers_db[rover_id].direction == 'West'):
        rovers_db[rover_id].direction = 'South'
    return rovers_db[rover_id].direction


def turnRight(rover_id: int):
    if (rovers_db[rover_id].direction == 'North'):
        rovers_db[rover_id].direction = 'East'
    elif (rovers_db[rover_id].direction == 'East'):
        rovers_db[rover_id].direction = 'South'
    elif (rovers_db[rover_id].direction == 'South'):
        rovers_db[rover_id].direction = 'West'
    elif (rovers_db[rover_id].direction == 'West'):
        rovers_db[rover_id].direction = 'North'
    return rovers_db[rover_id].direction

def getMineID(x: int, y: int):
    for mine in mines_db:
        if mine.xpos == x and mine.ypos == y:
            print(f"Mine {mine.id} Identified")
            return mine.pin
        else:
            return -1

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
import uvicorn
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
    roverMovement(rover_id)
    return {"rover_id": rover_id}

def roverMovement(rover_id: int):
    #todo: Create function that handles movement of rover.
    #This function will be called in dispatchRover()
    commands = rovers_db[rover_id].data
    for i in range(len(commands)):
        if(commands[i] == 'M'):
            move_rover(rovers_db[rover_id])
        elif(commands[i] == 'L'):
            #rovers_db[rover_id].direction = turnLeft(rovers_db[rover_id].direction)
            rovers_db[rover_id].direction = turn_left(rovers_db[rover_id])
        elif(commands[i] == 'R'):
            rovers_db[rover_id].direction = turn_right(rovers_db[rover_id])
        elif(commands[i] == 'D'):
            x = rovers_db[rover_id].xpos
            y = rovers_db[rover_id].ypos
            if(getMineID(x,y) != -1):
                print("Mine has been defused! CTs Win!")
                print("PIN of Defused Mine is ", getMineID(x,y))
            else:
                print("No Mine here!")


def move_rover(rover):
    x = rover.xpos
    y = rover.ypos
    # check if new position is within grid boundaries

    if rover.direction == "North":
        if y == 0 or map_grid[y-1][x] == "#":  # check if next position is a wall
            print("Cannot move, wall in front of rover!")
        else:
            rover.ypos = rover.ypos-1
    elif rover.direction == "East":
        if x == len(map_grid[0])-1 or map_grid[y][x+1] == "#":  # check if next position is a wall
            print("Cannot move, wall in front of rover!")
        else:
            rover.xpos = rover.xpos+1
    elif rover.direction == "South":
        if y == len(map_grid)-1 or map_grid[y+1][x] == "#":  # check if next position is a wall
            print("Cannot move, wall in front of rover!")
        else:
            rover.ypos = rover.ypos+1
    elif rover.direction == "West":
        if x == 0 or map_grid[y][x-1] == "#":  # check if next position is a wall
            print("Cannot move, wall in front of rover!")
        else:
            rover.xpos = rover.xpos-1



def turn_right(rover):
    """Updates the rover's direction to the left of its current direction"""
    directions = ['North', 'East', 'South', 'West']
    current_direction = rover.direction
    current_index = directions.index(current_direction)
    new_index = (current_index + 1) % 4  # wraps around to end of list if index becomes negative
    new_direction = directions[new_index]
    rover.direction = new_direction
    return rover

def turn_left(rover):
    """Updates the rover's direction to the left of its current direction"""
    directions = ['North', 'East', 'South', 'West']
    current_direction = rover.direction
    current_index = directions.index(current_direction)
    new_index = (current_index - 1) % 4  # wraps around to end of list if index becomes negative
    new_direction = directions[new_index]
    rover.direction = new_direction
    return rover


def getMineID(x: int, y: int):
    for mine in mines_db:
        if mine.xpos == x and mine.ypos == y:
            print(f"Mine {mine.id} Identified")
            return mine.pin
        else:
            return -1
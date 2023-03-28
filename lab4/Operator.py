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

mines_db = {}

#--------------------------------------------------
#
#                 Map functions
#
#--------------------------------------------------

#GET: Retrieve 2D array of the field
@app.get('/map')
def getMap():
    with open("map.txt", "r") as f:
        map_data = f.read()
    return {"Map": map_data}

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
    elif rovers_db[rover_id].status == 'ns':
        raise HTTPException(status_code=405, detail="Rover has not started")
    elif rovers_db[rover_id].status == 'fin':
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
    roverMovement(rover_id)
    return {"rover_id": rover_id}

def roverMovement(rover_id: int):
    #todo: Create function that handles movement of rover.
    #This function will be called in dispatchRover()
    commands = rovers_db[rover_id].data
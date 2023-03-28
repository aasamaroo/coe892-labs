#----------------------------------------------------
#
#          COE892 Lab 4/5: FastAPI
#                 Main.py
#       Made by Anand Alexander Samaroo
#             Github: aasamaroo
#
#-----------------------------------------------------

from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()


#------------------------------------------
#      Map, Rover, and Mine Objects
#------------------------------------------

#Todo: Create objects for Map, Rover, and Mines
class Map(BaseModel):
    data: List[List][int]

class Rover(BaseModel):
    id: int
    data: str
    status: str
    xpos: int
    ypos: int

#db to store all rovers
rovers_db = {}

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
    #do something
    return {'Output': 'This is a test for the Get Mines.'}

#GET: Retrieve specified mine with serial number and coordinates
#Throws exception if Mine not found (404 error)
@app.get('/mines/:id')
def retrieveMine():
    #do something
    return {'Output': 'This is a test for the Get Mine with ID.'}

#DELETE: Delete a mine specified by their ID
#Throws 404 error if Mine not found
@app.delete('/mines/:id')
def deleteMine():
    #do something
    return {'Output': 'This is a test for the Delete Mine.'}

#POST: Create a new mine
@app.post('/mines')
def addMine():
    #add the mine
    return {'Output': 'This is a test for the Add Mine.'}

#PUT: Update a mine
#404 error if Mine not found
@app.put('/mines/:id')
def updateMine():
    #do something
    return {'Output': 'This is a test for the Put Mine.'}

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
@app.get('/rovers/:id')
def retrieveRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    return rovers_db[rover_id]

#POST: Create new rover
@app.post('/rovers')
def addRover():
    #add the mine
    return {'Output': 'This is a test for the Add Rover.'}

#Delete: Deletes rover specified by ID
#Throws 404 error if Rover not found
@app.delete('/rovers/{rover_id}')
def deleteRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    del rovers_db[rover_id]
    return {"message": f"Rpver {rover_id} has been successfully deleted"}

#PUT: Send list of commands to Rover
#404 error if Rover not found
#Error thrown if Rover Status is "Not Started", or "Finished"
@app.put('/rovers/{rover_id}')
def updateRover(rover_id: int):
    if rover_id not in rovers_db:
        raise HTTPException(status_code=404, detail="Rover not found")
    if rovers_db[rover_id].status == 'ns':
        raise HTTPException(status_code=405, detail="Rover has not started")
    elif rovers_db[rover_id].status == 'fin':
        raise HTTPException(status_code=405, detail="Rover is finished")
    # Update the rover object in the database
    response = requests.get('https://coe892.reev.dev/lab1/rover/' + str(number))
    data = response.text
    parse_json = json.loads(data)
    moves = parse_json['data']['moves']
    rovers_db[rover_id].data = moves
    return {"message": f"Rover {rover_id} updated successfully."}


#POST: Dispatch Rover with specified ID
@app.post('/rovers/{rover_id}/dispatch')
def dispatchRover():
    #do something
    return {'Output': 'This is a test for the Dispatch Rovers.'}

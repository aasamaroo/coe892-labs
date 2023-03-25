#----------------------------------------------------
#
#          COE892 Lab 4/5: FastAPI
#                 Main.py
#       Made by Anand Alexander Samaroo
#             Github: aasamaroo
#
#-----------------------------------------------------

from fastapi import FastAPI

app = FastAPI()


#------------------------------------------
#      Map, Rover, and Mine Objects
#------------------------------------------

#Todo: Create objects for Map, Rover, and Mines


#--------------------------------------------------
#
#                 Map functions
#
#--------------------------------------------------

#GET: Retrieve 2D array of the field
@app.get('/map')
def getMap():
    #do something
    return {'Output': 'This is a test for the Get Map.'}

#PUT: Update height and width of field
@app.put('/map')
def updateField():
    #do something
    return {'Output': 'This is a test for the Put Map.'}

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
    #do something
    return {'Output': 'This is a test for the Get Rovers.'}

#GET: Retrieve rover specified by ID number
#Throw exception if Rover not found (404 error)
@app.get('/rovers/:id')
def retrieveRover():
    #do something
    return {'Output': 'This is a test for the Get Rover with ID.'}

#POST: Create new rover
@app.post('/rovers')
def addRover():
    #add the mine
    return {'Output': 'This is a test for the Add Rover.'}

#Delete: Deletes rover specified by ID
#Throws 404 error if Rover not found
@app.delete('/rovers/:id')
def deleteRover():
    #do something
    return {'Output': 'This is a test for the Delete Rover.'}

#PUT: Send list of commands to Rover
#404 error if Rover not found
#Error thrown if Rover Status is "Not Started", or "Finished"
@app.put('/rovers/:id')
def updateRover():
    #do something
    return {'Output': 'This is a test for the Put Mine.'}

#POST: Dispatch Rover with specified ID
@app.post('/rovers/:id/dispatch')
def dispatchRover():
    #do something
    return {'Output': 'This is a test for the Dispatch Rovers.'}

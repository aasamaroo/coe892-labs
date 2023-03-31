#--------------------------------------------------------------------
#
#         This is the server program for COE892 Lab 4/5
#          All it pretty much does is run the requests
#
#--------------------------------------------------------------------

import requests
import json
import Operator


#-----------------------------------------
#
#           Working Requests
#
#-----------------------------------------

create_rover_url = 'http://127.0.0.1:8000/rovers/'
dispatch_rover_url = 'http://127.0.0.1:8000/rovers/{}/dispatch'

new_rover_data = {
    "x_pos": 0,
    "y_pos": 0,
    "status": "NotStarted",
    "direction": "North"
}

response = requests.post(create_rover_url, json.dumps(new_rover_data))
if response.status_code == 200:
    print('New rover created successfully.')
else:
    print('Error creating new rover.')

rover_id = response.json()['id']




#--------------------------------
#
#   Test Cases for Failures
#
#--------------------------------




#Read/Update/Delete (RUD) a mine that does not exist

#GET
print(requests.get(''))

#PUT
print(requests.put(''))

#DELETE
print(requests.delete(''))



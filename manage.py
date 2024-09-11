from datetime import datetime
from app import app
from app.user.model import User
from helpers.area_list import initialize_area

with app.app_context():
    # pass
    
    initialize_area() # This will initialize the database with all existing LGAs
        
    # TODO:
    # Remove the pass keyword and
    # Run some actions you want to be be performed
    # on your server either when deployed or locally.
    # TODO: WARNING: This will also execute when deployed
    print('Ready!')
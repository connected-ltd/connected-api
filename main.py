import sys
sys.dont_write_bytecode = True
from helpers.area_list import initialize_area

from app import app

@app.route("/")
def index():
    # WARNING: Only uncomment when trying to set up project locally
    # initialize_area()
    return {'name':"connected-api", 'version':"0.0.1", 'status':"OK"}

@app.route('/health')
def health():
    # TODO do some checks here to confirm everything works
    return {'status':'OK'}, 200

if __name__ == '__main__':
    app.run(debug=True)
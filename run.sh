
# export environment file
export `tail -1 .env`

# run flask app
export FLASK_APP=pathfinder/api.py
flask run


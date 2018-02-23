from flask import Flask, jsonify, request
from datetime import datetime
import os
import logging
from core import activities


def init_logger():
    level = logging.INFO
    if 'LOG_LEVEL' in os.environ:
        if os.environ['LOG_LEVEL'] == 'DEBUG':
            level = logging.DEBUG
        elif os.environ['LOG_LEVEL'] == 'INFO':
            level = logging.INFO
        elif os.environ['LOG_LEVEL'] == 'WARNING':
            level = logging.WARNING

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=level)

init_logger()
start_time = datetime.now()
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def info():
    global start_time
    response = {
        'error': "",
        'msg': "Hello World",
        'started_at': str(start_time)
    }

    return jsonify(response)


@app.route('/activities', methods=['POST'])
def get_acivities():
    logging.info("recieved activities request")
    data = request.get_json()

    ori = (data['origin']['lon'], data['origin']['lat'])
    dst = (data['destination']['lon'], data['destination']['lat'])
    checkin = datetime.strptime(data['checkin'], '%d-%m-%Y')
    checkout = datetime.strptime(data['checkout'], '%d-%m-%Y')

    acts = activities.get_activities_path(ori, dst, checkin, checkout)

    return jsonify({'activities': acts})


@app.route('/ancillaries', methods=['POST'])
def get_ancillaries():
    logging.info("recieved ancillaries request")
    response = {
        'hotels': [
            {
                'id': 'H000',
                'name': 'Hotel Travesuras',
                'lon': 2.742436,
                'lat': 39.643097,
                'description': "Todo muy serio ****",
                'adress': "Santa Maria también, como el karate",
                'photo': "",
                'tags': ["hotel", "dormir"],
                'avail': [
                    {
                        'date': '01-06-2018',
                        'time': '17:00',
                        'price': 20
                    },
                    {
                        'date': '02-06-2018',
                        'time': '17:00',
                        'price': 20
                    },
                    {
                        'date': '02-06-2018',
                        'time': '19:30',
                        'price': 20
                    },
                    {
                        'date': '03-06-2018',
                        'time': '17:00',
                        'price': 20
                    }
                ]
            },
            {
                'id': 'H001',
                'name': 'Hotel Aragonia',
                'lon': 2.896245,
                'lat': 39.714968,
                'description': "The best hotel in Mallorca",
                'adress': "Omnipresente",
                'photo': "https://res.cloudinary.com/teepublic/image/private/s--m-6jzJG3--/t_Preview/b_rgb:0f7b47,c_limit,f_jpg,h_630,q_90,w_630/v1491197195/production/designs/1379547_1.jpg",
                'tags': ["best"],
                'avail': [
                    {
                        'date': '03-06-2018',
                        'time': '10:00',
                        'price': 99.99
                    },
                    {
                        'date': '02-06-2018',
                        'time': '17:00',
                        'price': 99.99
                    },
                    {
                        'date': '03-06-2018',
                        'time': '19:30',
                        'price': 99.99
                    },
                    {
                        'date': '04-06-2018',
                        'time': '17:00',
                        'price': 99.99
                    }
                ]
            }
        ],
        'restaurants': [
            {
                'id': 'R000',
                'name': 'Can Joan de s\'aigo',
                'lon': 2.871869,
                'lat': 39.660543,
                'description': "es bo aixooo",
                'adress': "Cami 33, 27A. Biniagual",
                'photo': "http://menorcana.com/wp-content/uploads/2011/01/COCA-DE-PATATA-021-515x386.jpg",
                'tags': ["mallorca", "typical", "bo"]
            },
        ]
    }

    return jsonify(response)


@app.route('/agenda', methods=['POST'])
def make_agenda():
    logging.info("recieved agenda request")
    data = request.get_json()
    agenda_id = 'A1234'
    if 'id' in data and data['id']:
        agenda_id = data['id']
    response = { 'id': agenda_id }

    return jsonify(response)


@app.errorhandler(500)
def error_handler(ex):
    logging.error(str(ex))
    return jsonify({'error': str(ex)}), 500

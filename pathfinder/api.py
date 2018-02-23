from flask import Flask, jsonify, request
from datetime import datetime
from core.ancillaries import get_integration_ancillaries
import os
import logging


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
    response = {
        'activities': [
            {
                'id': '000',
                'name': 'Malú in concert',
                'lon': 2.855046,
                'lat': 39.676928,
                'description': "No voy ni que me paguen",
                'adress': "Calle 13, Binissalem",
                'photo': "http://www.festivalperalada.com/media/cache/thumb_giant/uploads/images/4414_POSTS_FESTIVAL8.jpg",
                'tags': ["music", "people"],
                'avail': [
                    {
                        'date': '01-06-2018',
                        'time': '17:00',
                        'price': 17.25
                    },
                    {
                        'date': '02-06-2018',
                        'time': '17:00',
                        'price': 20
                    },
                    {
                        'date': '02-06-2018',
                        'time': '19:30',
                        'price': 22.5
                    },
                    {
                        'date': '03-06-2018',
                        'time': '17:00',
                        'price': 20
                    }
                ]
            },
            {
                'id': '001',
                'name': 'Karate nudista',
                'lon': 2.767155,
                'lat': 39.636752,
                'description': "El deporte de los hombres de verdad",
                'adress': "Santa Maria del Camí",
                'photo': "https://s3.pixers.pics/pixers/700/FO/26/38/72/20/700_FO26387220_95ee8d10dcb393464e82512232ad1549.jpg",
                'tags': ["deporte", "karate", "nude"],
                'avail': [
                    {
                        'date': '03-06-2018',
                        'time': '17:00',
                        'price': 0
                    },
                    {
                        'date': '02-06-2018',
                        'time': '17:00',
                        'price': 10
                    },
                    {
                        'date': '03-06-2018',
                        'time': '19:30',
                        'price': 5.75
                    },
                    {
                        'date': '04-06-2018',
                        'time': '17:00',
                        'price': 10.99
                    }
                ]
            }
        ]
    }

    return jsonify(response)


@app.route('/ancillaries', methods=['POST'])
def get_ancillaries():
    logging.info("recieved ancillaries request")
    data = request.get_json()
    inDate = datetime.strptime(data['checkin'], '&d-%m-%Y')
    outDate = datetime.strptime(data['checkout'], '&d-%m-%Y')
    response = get_integration_ancillaries(data['lon'], data['lat'], inDate, outDate)
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

from flask import Flask, render_template, jsonify, json, request
from flask_socketio import SocketIO, emit, send
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
# app.config['SERVER_NAME'] = '0.0.0.0:5000'
socketio = SocketIO(app)

@socketio.on('join')
def test_message(message):
    print("message: %s" % message)
    emit('my response', {'data': 'got it!'})

@socketio.on('walk')
def update_position(latlon):
    print("latlon: {}".format(latlon))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['GET'])
def simulate():
    traces = json.load(open('./traces.json'))
    routes = traces['data']
    for route in routes:
        socketio.emit('walk', route)
        time.sleep(0.5)
    # return render_template('index.html')
    return "walking, position {}\n".format(latlon)

@app.route('/walk', methods=['POST'])
def walk():
    param_data = request.form
    payload = {
        "id": param_data['id'],
        "latlon": param_data['latlong']
    }
    latlon = param_data['latlong']
    socketio.emit('walk', payload)
    return "walking, position {}\n".format(latlon)

if __name__ == '__main__':
    socketio.run(app)
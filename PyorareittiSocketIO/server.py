import json

from flask import Flask, Response, render_template, request
from flask_cors import CORS, cross_origin  # pip install flask-cors
from flask_socketio import SocketIO, emit

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

# lista mittauksista
measurements = []

# Näyttää listassa olevat paikkatiedot kartalla
# Selainohjelma hakee mittaukset fetch:llä (GET)
@cross_origin()
@app.route('/')
def get_all_measurements_map():
    print(measurements)
    return render_template('kartta.html')

# palvelin saa listan koordinaateista JSON-muodossa kutsumalla tätä
@cross_origin()
@app.route('/api/meas')
def get_all_measurements():
    return(json.dumps(measurements))            

# avaa sivun result.html ja näyttää paikkatiedon HTML-taulukkona.
# tiedot välitetään templaten avulla
@cross_origin()
@app.route('/template')
def get_all_measurements_template():
    print("hei",measurements)
    return render_template('result.html', result = measurements)

# Näyttää paikkatiedot kartalla sitä mukaan kuin ne saapuvat
# Paikkatiedot välitetään socketio:n kautta 
@cross_origin()
@app.route('/socketio')
def get_all_measurements_socketio():
    #print(measurements)
    return render_template('karttasocketio.html')

# Näyttää listassa olevat paikkatiedot kartalla
# Selainohjelma hakee mittaukset fetch:llä (GET)
# saadessaan socketio-viestin
@cross_origin()
@app.route('/socketiofetch')
def get_all_measurements_map3():
    print(measurements)
    return render_template('karttasocketio2.html')

@cross_origin()
@app.route('/uusimittaus', methods = ['POST'])
def new_measurement():
    # lisää uusi mittaus taulukkoon
    p = request.get_json(force=True)
    
    measurements.append(p)

    x = json.dumps(p, indent=True)
    socketio.emit('position', {'data': x})
    return x

if __name__ == '__main__':
   socketio.run(app)

# google: flask socketio

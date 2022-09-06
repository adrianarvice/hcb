import os
import sys
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import base64
import numpy as np

from pathlib import Path
from flask import Flask, render_template, request, redirect, Response
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.route("/")
def main():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/polyphonic_encryption")
def polyphonic_encryption():
    return render_template('polyphonic_encryption.html')

@app.route("/polyphonic_decryption")
def polyphonic_decryption():
    return render_template('polyphonic_decryption.html')

@app.route("/polyphonic_decryption", methods=["GET", "POST"])
def get_polyphonic_decryption_data():
    if request.method == "POST":
        ciphertext = request.form["polyphonic_input_ciphertext"]
        print(ciphertext)
    return redirect(request.referrer)


@app.route('/plot.png')
def plot_png():

    '''
    y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    x = np.arange(10)
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(x, y, label='$y = numbers')
    plt.title('Legend inside')
    ax.legend()

    '''


    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')

@socket.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socket.on('polyphonic_decryption_analyzer')
def polyphonic_decryption_analyzer():
    print("PYTHON WORKING")
    from socket_bridge import start_all
    start_all()


if __name__ == "__main__":
    socket.run(app, host=os.getenv("IP", "127.0.0.1"), port=int(os.getenv("PORT", 5010)), debug=True)



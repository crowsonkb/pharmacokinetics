"""A Flask web application to calculate and plot drug concentration over time."""

# pylint: disable=wrong-import-position

import binascii
from dataclasses import asdict, dataclass
import io
from typing import List

from flask import Flask, make_response, jsonify, request
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import numpy as np

import pk


app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


class Concentration:
    def __init__(self, form):
        self.hl = float(form['hl'])
        self.t_max = float(form['t-max'])
        self.duration = float(form['duration'])
        drug = pk.Drug(self.hl, self.t_max)
        self.steps = 60
        self.num = round(self.duration * self.steps + 1)
        self.x = np.arange(self.num) / self.steps
        self.y = drug.concentration(self.num, 1/self.steps, {0: 1})


@dataclass
class ConcentrationResponse:
    num: int
    steps: int
    concentration: List[float]


@app.route('/concentration', methods=['POST'])
def concentration():
    conc = Concentration(request.form)
    msg = ConcentrationResponse(conc.num, conc.steps, list(conc.y))
    return jsonify(asdict(msg))


@app.route('/concentration_svg', methods=['POST'])
def concentration_svg():
    conc = Concentration(request.form)

    fig, ax = plt.subplots(figsize=(8, 5.33), tight_layout=True)
    ax.set_xlabel('Hours', fontsize=14)
    ax.set_ylabel('Concentration', fontsize=14)
    ax.plot(conc.x, conc.y)
    ax.grid(linestyle='--')

    buf = io.BytesIO()
    fig.savefig(buf, format='svg')
    url = 'data:image/svg+xml;base64,' + binascii.b2a_base64(buf.getvalue()).decode()
    return make_response(url)

"""A Flask web application to calculate and plot drug concentration over time."""

# pylint: disable=wrong-import-position

import io

from flask import Flask, jsonify, Response, request
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import numpy as np
from werkzeug.exceptions import BadRequest

import pk

MAX_DURATION = 720


app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


class Concentration:
    def __init__(self, **kwargs):
        self.hl_e = float(kwargs['hl'])
        if self.hl_e <= 0:
            raise BadRequest('hl must be positive.')
        self.t_max = float(kwargs['t-max'])
        if self.t_max <= 0:
            raise BadRequest('t_max must be positive.')
        self.duration = float(kwargs['duration'])
        if self.duration <= 0:
            raise BadRequest('Duration must be positive.')
        if self.duration > MAX_DURATION:
            raise BadRequest('Duration exceeds the maximum.')
        dose_qs = map(float, kwargs['doses'].split())
        offsets = map(float, kwargs['offsets'].split())
        self.doses = dict(zip(offsets, dose_qs))
        self.drug = pk.Drug(self.hl_e, self.t_max)
        self.steps = 60
        self.num = round(self.duration * self.steps + 1)
        self.x = np.arange(self.num) / self.steps
        self.y = self.drug.concentration(self.num, 1/self.steps, self.doses)


@app.route('/concentration.csv')
def concentration_csv():
    conc = Concentration(**request.args.to_dict())
    x = np.c_[conc.x, conc.y]
    buf = io.BytesIO()
    np.savetxt(buf, x, delimiter=',', header='hours,concentration', comments='')
    return Response(buf.getvalue(), mimetype='text/csv')


@app.route('/concentration.json')
def concentration_json():
    conc = Concentration(**request.args.to_dict())
    msg = {'concentration': list(conc.y),
           'drug': {'c_0': conc.drug.c_0,
                    'hl_a': conc.drug.hl_a,
                    'hl_e': conc.drug.hl_e,
                    't_max': conc.drug.t_max},
           'doses': conc.doses,
           'steps': conc.steps}
    return jsonify(msg)


@app.route('/concentration.svg')
def concentration_svg():
    conc = Concentration(**request.args.to_dict())

    fig, ax = plt.subplots(figsize=(8, 5.33), tight_layout=True)
    ax.set_xlabel('Hours', fontsize=14)
    ax.set_ylabel('Concentration', fontsize=14)
    ax.plot(conc.x, conc.y)
    ax.grid(linestyle='--')

    buf = io.BytesIO()
    fig.savefig(buf, format='svg')
    plt.close(fig)
    return Response(buf.getvalue(), mimetype='image/svg+xml')

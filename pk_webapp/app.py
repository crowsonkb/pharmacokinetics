"""A Flask web application to calculate and plot drug concentration over time."""

# pylint: disable=wrong-import-position

import io

from flask import Flask, jsonify, Response, request
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import numpy as np

import pk


app = Flask(__name__, static_url_path='')
app.config.from_object('pk_webapp_config')


@app.route('/')
def root():
    return app.send_static_file('index.html')


class Concentration:
    def __init__(self, **kwargs):
        self.hl = float(kwargs['hl'])
        self.t_max = float(kwargs['t-max'])
        self.duration = float(kwargs['duration'])
        dose_qs = map(float, kwargs['doses'].split())
        offsets = map(float, kwargs['offsets'].split())
        self.doses = dict(zip(offsets, dose_qs))
        drug = pk.Drug(self.hl, self.t_max)
        self.steps = 60
        self.num = round(self.duration * self.steps + 1)
        self.x = np.arange(self.num) / self.steps
        self.y = drug.concentration(self.num, 1/self.steps, self.doses)


@app.route('/concentration.json')
def concentration_json():
    conc = Concentration(**request.args.to_dict())
    msg = {'concentration': list(conc.y), 'steps': conc.steps}
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

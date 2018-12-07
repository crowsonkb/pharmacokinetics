"""Calculates and plots drug concentration over time."""

import argparse

import matplotlib.pyplot as plt
import numpy as np

import pk


def main():
    """The main function."""
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--hl', type=float, required=True, metavar='HOURS',
                    help='the drug\'s terminal half-life, in hours')
    ap.add_argument('--tmax', type=float, required=True, metavar='HOURS',
                    help='the drug\'s time to maximum concentration, in hours')
    ap.add_argument('--time', type=float, default=24, metavar='HOURS',
                    help='the number of hours to simulate concentrations for')
    ap.add_argument('--doses', type=float, nargs='+', default=[1], metavar='DOSE',
                    help='the magnitudes of each dose')
    ap.add_argument('--offsets', type=float, nargs='+', default=[0], metavar='OFFSET',
                    help='the time, in hours, each dose is given at')
    ap.add_argument('--output', default='output.png', help='the output image file')
    args = ap.parse_args()

    step = 1/60

    drug = pk.Drug(args.hl, args.tmax)
    num = round(args.time / step + 1)
    x = np.arange(num) * step
    y = drug.concentration_sum_of_doses(num, step, args.doses, args.offsets)

    plt.rcParams['font.size'] = 12

    fig, ax = plt.subplots(figsize=(12, 8), tight_layout=True)
    ax.set_xlabel('Hours', fontsize=18)
    ax.set_ylabel('Concentration', fontsize=18)
    ax.grid(linestyle='--')
    ax.plot(x, y)
    fig.savefig(args.output, dpi=150)


if __name__ == '__main__':
    main()

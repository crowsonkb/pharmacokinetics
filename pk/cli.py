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
                    help='the drug\'s elimination half-life, in hours')
    ap.add_argument('--tmax', type=float, required=True, metavar='HOURS',
                    help='the drug\'s time to maximum concentration, in hours')
    ap.add_argument('--duration', type=float, default=24, metavar='HOURS',
                    help='the duration, in hours, to simulate concentrations for')
    ap.add_argument('--doses', type=float, nargs='+', default=[1], metavar='DOSE',
                    help='the magnitudes of each dose (units are arbitrary)')
    ap.add_argument('--offsets', type=float, nargs='+', default=[0], metavar='OFFSET',
                    help='the time, in hours, that each dose is given at')
    ap.add_argument('--output', default='output.png', metavar='FILE',
                    help='the output image filename')
    ap.add_argument('--output-size', type=int, nargs=2, default=[1920, 1280], metavar=('W', 'H'),
                    help='the output width and height in pixels')
    ap.add_argument('--dpi', type=float, default=160, help='the output dots per inch (dpi)')
    args = ap.parse_args()

    step = 1/60

    drug = pk.Drug(args.hl, args.tmax)
    num = round(args.duration / step + 1)
    x = np.arange(num) * step
    y = drug.concentration(num, step, dict(zip(args.offsets, args.doses)))

    plt.rcParams['font.size'] = 12

    fig_width = args.output_size[0] / args.dpi
    fig_height = args.output_size[1] / args.dpi
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), tight_layout=True)
    ax.plot(x, y)
    ax.set_xlabel('Hours', fontsize=18)
    ax.set_ylabel('Concentration', fontsize=18)
    ax.grid(linestyle='--')
    hour_tick_steps = [1, 1.2, 1.6, 1.68, 2, 2.4, 3, 4, 4.8, 6, 8, 9.6, 10]
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins='auto', integer=True, steps=hour_tick_steps))
    ax.margins(0.025, 0.05)
    ax.autoscale()
    fig.savefig(args.output, dpi=args.dpi)

if __name__ == '__main__':
    main()

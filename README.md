pharmacokinetics
================

Calculates and plots drug concentration over time.

Example output
--------------

Here, `pk` computes the concentration of a drug with a terminal half-life (t<sub>½</sub>) of 6 hours and a time to maximum concentration (t<sub>max</sub>) of 2 hours. Doses of 1 unit each were given at t+0, t+4, and t+8 hours.

```bash
pk --hl 6 --tmax 2 --doses 1 1 1 --offsets 0 4 8 --output demo.png
```

<img src="demo.png" width="900" height="600">

Installation
------------

```bash
python3 setup.py install
```

Usage
-----

```
usage: pk [-h] --hl HOURS --tmax HOURS [--duration HOURS]
          [--doses DOSE [DOSE ...]] [--offsets OFFSET [OFFSET ...]]
          [--output FILE] [--output-size W H] [--dpi DPI]

Calculates and plots drug concentration over time.

optional arguments:
  -h, --help            show this help message and exit
  --hl HOURS            the drug's elimination half-life, in hours (default:
                        None)
  --tmax HOURS          the drug's time to maximum concentration, in hours
                        (default: None)
  --duration HOURS      the duration, in hours, to simulate concentrations for
                        (default: 24)
  --doses DOSE [DOSE ...]
                        the magnitudes of each dose (units are arbitrary)
                        (default: [1])
  --offsets OFFSET [OFFSET ...]
                        the time, in hours, that each dose is given at
                        (default: [0])
  --output FILE         the output image filename (default: output.png)
  --output-size W H     the output width and height in pixels (default: [1920,
                        1280])
  --dpi DPI             the output dots per inch (dpi) (default: 160)
```

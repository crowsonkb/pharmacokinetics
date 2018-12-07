"""Calculates drug concentration over time."""

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brent


class Drug:
    """A drug's pharmacokinetic parameters.

    :param c_0: The initial concentration normalization factor.
    :type c_0: float
    :param hl_a: The drug's absorption half-life.
    :type hl_a: float
    :param hl_e: The drug's elimination half-life.
    :type hl_e: float
    :param t_max: The drug's time to maximum concentration.
    :type t_max: float
    """

    def __init__(self, hl, t_max):
        """Initializes a Drug.

        :param hl: The drug's elimination half-life.
        :type hl: float
        :param t_max: The drug's time at maximum concentration.
        :type t_max: float
        """
        self.t_max = float(t_max)
        self.hl_e = float(hl)
        self.hl_a = brent(lambda hl_a: (self._t_max_given_hls(hl_a, self.hl_e) - self.t_max)**2)
        self.c_0 = 1 / self._concentration_at_time(self.t_max, self.hl_a, self.hl_e)

    def __repr__(self):
        return f'Drug(c_0={self.c_0}, hl_a={self.hl_a}, hl_e={self.hl_e}, t_max={self.t_max})'

    @staticmethod
    def _concentration(num, step, hl_a, hl_e, doses):
        """Calculates drug concentration at the given times.

        :param num: The number of timesteps to use.
        :type num: int
        :param step: The timestep size.
        :type step: float
        :param hl_a: The drug's absorption half-life.
        :type hl_a: float
        :param hl_e: The drug's elimination half-life.
        :type hl_e: float
        :param doses: Maps the offset time of each dose to its magnitude.
        :type doses: dict(float, float)
        :return: The drug concentration at the given times.
        :rtype: numpy.ndarray
        """
        k_a = np.log(2) / hl_a
        k_e = np.log(2) / hl_e
        mat = np.float64([[k_a, -k_a, 0], [0, k_e, -k_e], [0, 0, 0]])
        mat_step = expm(-mat * step)
        solution = np.zeros((num, 3))
        try:
            indexed_doses = {int(round(offset / step)): dose for offset, dose in doses.items()}
        except ZeroDivisionError:
            indexed_doses = {0: sum(doses.values())}
        for i in range(num):
            if i in indexed_doses:
                solution[i] += [indexed_doses[i], 0, 0]
            solution[i] += mat_step.T @ solution[i-1]
        return solution[:, 1]

    @classmethod
    def _concentration_at_time(cls, t, hl_a, hl_e):
        """Calculates drug concentration at the given instance in time.

        :param t: The time to compute the concentration at.
        :type t: float
        :param hl_a: The drug's absorption half-life.
        :type hl_a: float
        :param hl_e: The drug's elimination half-life.
        :type hl_e: float
        :return: The drug concentration at the given instance in time.
        :rtype: float
        """
        return cls._concentration(2, t, hl_a, hl_e, {0: 1})[1]

    @classmethod
    def _t_max_given_hls(cls, hl_a, hl_e):
        """Calculates the time to maximum concentration given drug half-lives.

        :param hl_a: The drug's absorption half-life.
        :type hl_a: float
        :param hl_e: The drug's elimination half-life.
        :type hl_e: float
        :return: The drug's time to maximum concentration (t_max).
        :rtype: float
        """
        if hl_a == 0:
            return 0
        if hl_a < 0:
            return np.inf
        return brent(lambda t: -cls._concentration_at_time(t, hl_a, hl_e))

    def concentration(self, num, step, doses=None):
        """Calculates drug concentration at the given times.

        :param num: The number of timesteps to use.
        :type num: int
        :param step: The timestep size.
        :type step: float
        :param doses: Maps the offset time of each dose to its magnitude.
        :type doses: dict(float, float)
        :return: The drug concentration at the given times.
        :rtype: numpy.ndarray
        """
        if doses is None:
            doses = {0: self.c_0}
        else:
            doses = {offset: dose * self.c_0 for offset, dose in doses.items()}
        return self._concentration(num, step, self.hl_a, self.hl_e, doses)

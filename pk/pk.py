"""Calculates drug concentrations over time."""

from functools import partial

import numpy as np
from scipy import linalg, optimize


class Drug:
    """A drug's pharmacokinetic parameters.

    Attributes:
        hl1 (float): The drug's absorption half-life.
        hl2 (float): The drug's terminal half-life.
        n_0 (float): The initial concentration normalization factor.
        tmax (float): The drug's time to maximum concentration.
    """

    def __init__(self, tmax, hl2):
        """Initializes a Drug.

        Args:
            tmax (float): The drug's time to maximum concentration.
            hl2 (float): The drug's terminal half-life.
        """
        self.tmax = float(tmax)
        self.hl2 = float(hl2)
        self.hl1 = optimize.brent(lambda hl1: (self._tmax_given_hls(hl1, self.hl2) - self.tmax)**2)
        self.n_0 = 1 / self._concentration_at_time(self.tmax, self.hl1, self.hl2)

    def __repr__(self):
        return f'Dose(hl1={self.hl1}, hl2={self.hl2}, n_0={self.n_0}, tmax={self.tmax})'

    @staticmethod
    def _concentration(num, step, hl1, hl2, offset):
        """Calculates drug concentration at the given times.

        Args:
            num (int): The number of timesteps to use.
            step (int): The timestep size.
            hl1 (float): The drug's absorption half-life.
            hl2 (float): The drug's terminal half-life.
            offset (float): The time to offset the initial dose by.

        Returns:
            ndarray: The drug concentration at the given times.
        """
        rate_1 = np.log(2) / hl1
        rate_2 = np.log(2) / hl2
        mat = np.float64([[rate_1, -rate_1, 0], [0, rate_2, -rate_2], [0, 0, 0]])
        mat_offset = linalg.expm(mat * offset)
        mat_step = linalg.expm(-mat * step)
        solution = np.zeros((num, 3))
        solution[0] = [1, 0, 0] @ mat_offset
        for i in range(1, num):
            solution[i] = mat_step.T @ solution[i-1]
        return np.maximum(0, solution[:, 1])

    @classmethod
    def _concentration_at_time(cls, t, hl1, hl2):
        """Calculates drug concentration at the given single time.

        Args:
            t (float): The time to compute the concentration at.
            hl1 (float): The drug's absorption half-life.
            hl2 (float): The drug's terminal half-life.

        Returns:
            float: The drug concentration at the given time.
        """
        return cls._concentration(2, t, hl1, hl2, 0)[1]

    @classmethod
    def _tmax_given_hls(cls, hl1, hl2):
        """Calculates the time to maximum concentration given drug half-lives.

        Args:
            hl1 (float): The drug's absorption half-life.
            hl2 (float): The drug's terminal half-life.

        Returns:
            float: The drug's time to maximum concentration (tmax).
        """
        if hl1 == 0:
            return 0
        if hl1 < 0:
            return np.inf
        return optimize.brent(lambda t: -cls._concentration_at_time(t, hl1, hl2))

    def concentration(self, num, step, dose=1, offset=0):
        """Calculates drug concentrations at the given times.

        Args:
            num (int): The number of timesteps to use.
            step (int): The timestep size.
            dose (float): The magnitude of the initial dose.
            offset (float): The time to offset the initial dose by.

        Returns:
            ndarray: The drug concentrations at the given times.
        """
        return self._concentration(num, step, self.hl1, self.hl2, offset) * (self.n_0 * dose)

    def concentration_sum_of_doses(self, num, step, doses, offsets):
        """Calculates drug concentrations at the given times for multiple doses.

        Args:
            num (int): The number of timesteps to use.
            step (int): The timestep size.
            doses (ndarray): The magnitudes of each dose.
            offsets (ndarray): The time each dose is given at.

        Returns:
            ndarray: The drug concentrations at the given times.
        """
        return sum(map(partial(self.concentration, num, step), doses, offsets))

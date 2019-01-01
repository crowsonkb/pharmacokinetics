"""Calculates drug concentration over time."""

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq


class Drug:
    """A drug's pharmacokinetic parameters.

    :ivar c_0: The initial concentration normalization factor.
    :vartype c_0: float
    :ivar hl_a: The drug's absorption half-life.
    :vartype hl_a: float
    :ivar hl_e: The drug's elimination half-life.
    :vartype hl_e: float
    :ivar t_max: The drug's time to maximum concentration.
    :vartype t_max: float
    """

    def __init__(self, hl, t_max):
        """Initializes a Drug.

        :param hl: The drug's elimination half-life.
        :type hl: float
        :param t_max: The drug's time at maximum concentration.
        :type t_max: float
        """
        self.hl_e = float(hl)
        self.t_max = float(t_max)

        def diff_at_tmax(hl_a):
            return self._concentration_at_time(self.t_max, hl_a, self.hl_e, return_diff=True)[1]
        a, b = 1, 1
        while diff_at_tmax(a) > 0:
            a /= 10
        while diff_at_tmax(b) < 0:
            b *= 10
        self.hl_a = brentq(diff_at_tmax, a, b)

        self.c_0 = 1 / self._concentration_at_time(self.t_max, self.hl_a, self.hl_e)

    def __repr__(self):
        s = 'Drug(c_0={}, hl_a={}, hl_e={}, t_max={})'
        return s.format(self.c_0, self.hl_a, self.hl_e, self.t_max)

    @staticmethod
    def _concentration(num, step, hl_a, hl_e, doses, return_diff=False):
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
        mat = np.float64([[-k_a, k_a, 0], [0, -k_e, k_e], [0, 0, 0]])
        mat_step = expm(mat * step)
        solution = np.zeros((num, 3))
        if return_diff:
            mat_tangent = np.copy(mat)
            diff = np.zeros(num)
        try:
            indexed_doses = {int(round(offset / step)): dose for offset, dose in doses.items()}
        except ZeroDivisionError:
            indexed_doses = {0: sum(doses.values())}
        for i in range(num):
            if i:
                solution[i] = mat_step.T @ solution[i-1]
            if i in indexed_doses:
                solution[i, 0] += indexed_doses[i]
            if return_diff:
                diff[i] = mat_tangent[0, 1] * solution[0, 0]
                mat_tangent[...] = mat_tangent @ mat_step
        if return_diff:
            return solution[:, 1], diff
        return solution[:, 1]

    @classmethod
    def _concentration_at_time(cls, t, hl_a, hl_e, return_diff=False):
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
        res = cls._concentration(2, t, hl_a, hl_e, {0: 1}, return_diff)
        if return_diff:
            return res[0][1], res[1][1]
        return res[1]

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

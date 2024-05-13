import numpy as np


class BernoulliBandit:
    """
    A Bernoulli bandit with a single arm.

    Attributes
    ----------
    p : float
        The probability of the arm returning a reward of 1.

    Methods
    -------
    pull()
        Simulate pulling the arm of the bandit.

    Examples
    --------
    >>> import numpy as np
    >>> np.random.seed(0)
    >>> import pybandit as pb
    >>> bandit = pb.bandit.BernoulliBandit(0.7)
    >>> bandit.pull()
    1
    >>> [bandit.pull() for _ in range(5)]
    [0, 1, 1, 1, 1]
    """

    def __init__(self, p):
        """
        Parameters
        ----------
        p : float
            The probability of the arm returning a reward of 1, must be between 0 and 1.
        """
        if not (0 <= p <= 1):
            raise ValueError("Probability p must be between 0 and 1")
        self.p = p

    def pull(self):
        """
        Pull the bandit's arm.

        Returns
        -------
        int
            The reward from pulling the arm, either 0 or 1.
        """
        return np.random.binomial(1, self.p)

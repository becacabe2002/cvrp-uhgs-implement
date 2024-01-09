import numpy as np
import csv
import math

class parame:
    """
    Read and store the parameters from the problem instance file
    """
    def __init__(self, fileName, minSol, maxSol, omega, muelite, prep, itMax, itDiv, near, muclose):
        self.fileName = fileName
        self.minSol = minSol
        self.maxSol = maxSol
        self.omega = omega
        self.muelite = muelite
        self.Prep = prep
        self.itMax = itMax
        self.itDiv = itDiv
        self.near = near
        self.muclose = muclose
        # with open(fileName) as tsv:
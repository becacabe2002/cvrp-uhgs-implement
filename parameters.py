import numpy as np
import csv
import math


class param:
    # Minimun cardinality for positive solution and negative solution
    minSol = 30
    # Cardinality limit for positive solution and negative solution
    maxSol = 70
    # weight of load excess
    omega = 40
    # weight of diversity (relative to maxSol) (the higher it is, the less it weighs)
    muelite = 1.5
    # Probability of repairing infeasible solutions
    Prep = 0.5
    # Maximum number of iterations without improvements
    itMax = 2000
    # # Iterations (relative to itMax) before diversification
    itDiv = 0.4
    # Percentage of nodes to consider as neighbors in education
    near = 0.2
    # Percentage of individuals to consider as neighbors in the calculation of diversity
    muclose = 1
    generation_size = maxSol - minSol
    csi_ref = 0.2

    '''
    The `param.py` file is a crucial part of the Unified Hybrid Genetic Search (UHGS) algorithm implementation. It is responsible for defining various parameters that control the behavior of the algorithm. Here's a more detailed explanation of the parameters:

        1. `minSol`: This parameter represents the minimum number of solutions that the algorithm should maintain in the population. It is used to ensure that the population size does not shrink too much, which could lead to a lack of diversity and premature convergence to suboptimal solutions.

        2. `maxSol`: This parameter represents the maximum number of solutions that the algorithm should maintain in the population. It is used to control the population size and prevent it from growing too large, which could slow down the algorithm and consume too much memory.

        3. `omega`: This parameter represents the penalty for load excess in the Capacitated Vehicle Routing Problem (CVRP). If a solution assigns more demand to a vehicle than its capacity allows, this penalty is added to the solution's cost to discourage such infeasible solutions.

        4. `muelite`: This parameter represents the weight of diversity in the population. The algorithm tries to maintain a diverse population to explore different parts of the solution space. The higher this parameter, the less the algorithm focuses on diversity.

        5. `Prep`: This parameter represents the probability of repairing infeasible solutions. If a solution is infeasible, the algorithm may attempt to repair it with this probability instead of discarding it.

        6. `itMax`: This parameter represents the maximum number of iterations that the algorithm should perform without finding any improvements. If the algorithm does not find a better solution for this many iterations, it terminates.

        7. `itDiv`: This parameter represents the number of iterations (relative to `itMax`) before the algorithm performs a diversification step. Diversification is a strategy to escape from local optima by introducing more diversity into the population.

        8. `near`: This parameter represents the percentage of nodes to consider as neighbors in the education phase. In the education phase, the algorithm tries to improve solutions by considering moves that involve their neighboring nodes.

        9. `diversity`: This parameter represents the percentage of individuals to consider as neighbors in the calculation of diversity. The algorithm calculates the diversity of the population as the average distance between each solution and its nearest neighbors.

    The `param.py` file also reads the problem instance from a file and calculates the distances between nodes. The problem instance includes the coordinates of the nodes, the demand at each node, and the capacity of the vehicles. The distances between nodes are used to calculate the cost of the solutions.
    '''

    def __init__(self, filename, minSol, maxSol, omega, muelite, prep, itMax, itDiv, near, muclose):
        self.filename = filename
        self.minSol = minSol
        self.maxSol = maxSol
        self.omega = omega
        self.muelite = muelite
        self.Prep = prep
        self.itMax = itMax
        self.itDiv = itDiv
        self.near = near
        self.muclose = muclose
        with open(filename) as tsv:  # read from file
            readpos = False
            readdemand = False
            i = -1
            j = -1
            for line in csv.reader(tsv, dialect="excel-tab"):
                if line[0].startswith("NODE_COORD_SECTION"):
                    readpos = True
                if line[0].startswith("DEMAND_SECTION"):
                    readpos = False
                    readdemand = True
                if line[0].startswith("DEPOT_SECTION"):
                    readdemand = False
                if line[0].startswith("DIMENSION"):
                    self.n = int(line[1])
                    self.demand = np.zeros(self.n, dtype=int)
                    self.pos = np.zeros((self.n + 1, 2), dtype=int)
                if line[0].startswith("CAPACITY"):
                    self.C = int(line[1])
                if readpos:
                    if i != -1:
                        self.pos[i][0] = line[1]
                        self.pos[i][1] = line[2]
                    i += 1
                if readdemand:
                    if j != -1:
                        self.demand[j] = int(line[1])
                    j += 1

        self.dist = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):
            for j in range(self.n):
                self.dist[i][j] = int(round(math.sqrt(math.pow(
                    self.pos[i][0] - self.pos[j][0], 2) + math.pow(self.pos[i][1] - self.pos[j][1], 2))))

        self.neigh = []
        numNeigh = int(self.n * self.near)
        for i in range(1, self.n):
            auxdist = list(self.dist[i])
            auxdist[i] = math.inf
            for k in range(numNeigh):
                j = auxdist.index(min(auxdist))
                self.neigh.append([i, j])
                auxdist[j] = math.inf

    def printparam(self):
        print("filename: ", self.filename)
        print("minsol: ", self.minSol)
        print("maxsol: ", self.maxSol)
        print("omega: ", self.omega)
        print("muelite: ", self.muelite)
        print("Prep: ", self.Prep)
        print("itMax: ", self.itMax)
        print("itDiv: ", self.itDiv)
        print("near: ", self.near)
        print("muclose: ", self.muclose)

    def printonfile(self, filename):
        myfile = open(filename, 'a')
        myfile.write("filename: ")
        myfile.write(self.filename)
        myfile.write("\nminsol: ")
        myfile.write(str(self.minSol))
        myfile.write("\nmaxsol: ")
        myfile.write(str(self.maxSol))
        myfile.write("\nomega: ")
        myfile.write(str(self.omega))
        myfile.write("\nmuelite: ")
        myfile.write(str(self.muelite))
        myfile.write("\nPrep: ")
        myfile.write(str(self.Prep))
        myfile.write("\nitMax: ")
        myfile.write(str(self.itMax))
        myfile.write("\nitDiv: ")
        myfile.write(str(self.itDiv))
        myfile.write("\nnear: ")
        myfile.write(str(self.near))
        myfile.write("\nmuclose: ")
        myfile.write(str(self.muclose))
        myfile.close()

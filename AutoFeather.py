import pickle
from math import floor, ceil
from queue import PriorityQueue

class Orion:
    def __init__(self):
        self.lvl = {}
        self.sgen_costs = {}
        self.lvl["sgen"] = 0
        self.gen_costs = {}
        self.lvl["gen"] = 1
        self.mult_costs = {}
        self.lvl["mult"] = 0
        self.disc_costs = {}
        self.lvl["disc"] = 0
        self.sdisc_costs = {}
        self.lvl["sdisc"] = 0
        self.state = 0
        self.feathers = 0
        self.total = 0
        self.path = ""
        self.time = 0

    def __lt__(self, other):
        ret = self.time < other.time

    def __gt__(self, other):
        ret = self.time > other.time
        for i in self.lvl:
            ret = ret and self.lvl[i] > other.lvl[i]
        return ret

    def __str__(self):
        s = "State:\nGenerator level: " + str(self.lvl["gen"]) + "\nMultiplier level: " + str(self.lvl["mult"]) + "\ndiscout level:" + str(self.lvl["disc"])
        s += "\nSuper Generator level: " + str(self.lvl["sgen"]) + "\nSuper discount level: " + str(self.lvl["sdisc"]) 
        s += "\nTotal discount: " + str(self.discount() * self.sdiscount())
        s += "\nIncome: " + str(self.income())
        s += "\nFeathers: " + str(self.feathers)
        s += "\nTotal Feathers: " + str(self.total)
        s += "\nTime: " + "{:.2e}".format(self.time) + " s"
        s += "\nPath: " + self.printPath()
        #s += "\nNeighbours: " + str(self.neighbours())

        return s

    def printPath(self):
        s = self.path[0] if self.path != "" else ""
        counter = 1
        ret = ""
        for i in self.path[1:]:
            if i == s:
                counter += 1
            else:
                if counter > 1:
                    ret += str(counter) + s + " "
                else:
                    ret += s + " "
                counter = 1
                s = i
        if counter > 1:
            ret += str(counter) + s
        else:
            ret += s
        return ret

    def priority(self, goal):
        return self.time, self

    def step(self, dt):
        df = self.income() * dt
        self.feathers += df
        self.total += df
        
    def walk(self, path):
        for i in path:
            if i == "g":
                self.upgrade_gen()
            elif i == "m":
                self.upgrade_mult()
            elif i == "d":
                self.upgrade_disc()
            elif i == "G":
                self.upgrade_sgen()
            elif i == "D":
                self.upgrade_sdisc()

    def totalWait(self, goal):
        return self.wait(goal) + self.time

    def wait(self, goal):
        dt = max(goal-self.feathers, 0)
        dt /= self.income()
        dt = ceil(dt)
        return dt

    def finish(self, goal):
        self.time += self.wait(goal)

    def discount(self):
        return (1 + .1 * self.lvl["disc"])

    def sdiscount(self):
        return (1 + .2 * self.lvl["sdisc"])

    def upgrade(self, parameter, costs, prod, base):
        cost = prod*base**self.lvl[parameter]
        if self.lvl[parameter] + 1 not in costs:
            costs[self.lvl[parameter] + 1] = cost
        cost = cost/(self.discount() * self.sdiscount())
        dt = self.wait(cost)
        self.time += dt
        self.step(dt)
        self.feathers -= cost
        self.lvl[parameter] += 1

    def upgrade_gen(self):
        self.upgrade("gen", self.gen_costs, 5, 1.075)
        self.path += "g"

    def upgrade_mult(self):
        self.upgrade("mult", self.mult_costs, 500, 1.11)
        self.path += "m"

    def upgrade_disc(self):
        self.upgrade("disc", self.disc_costs, 3000, 1.16)
        self.path += "d"

    def upgrade_sgen(self):
        self.upgrade("sgen", self.sgen_costs, 2*10**6, 1.12)
        self.path += "G"

    def upgrade_sdisc(self):
        self.upgrade("mult", self.mult_costs, 50*10**6, 1.27)
        self.path += "D"

    def income(self):
        return (self.lvl["gen"] + 5 * self.lvl["sgen"]) * (1 + .05 * self.lvl["mult"])

    def next_incomes(self):
        incomes = {}
        incomes["gen"] = (self.lvl["gen"] + 1 + 5 * sgen_lvl) * (1 + .05 * self.lvl["mult"])
        incomes["mult"] = (self.lvl["gen"] + 5 * sgen_lvl) * (1.05 + .05 * self.lvl["mult"])
        incomes["disc"] = (1.1 + .1 * self.lvl["disc"]) / self.discount()
        incomes["sgen"] = (self.lvl["gen"] + 5 * (self.lvl["sgen"] + 1)) * (1 + .05 * self.lvl["mult"])
        incomes["sdisc"] = (1.2 + .2 * self.lvl["sdisc"]) / self.sdiscount()
        return incomes["gen"], incomes["mult"], incomes["disc"], incomes["sgen"], incomes["sdisc"]

    def neighbours(self):
        s = "g"
        if self.total > 2500:
            s += "m"
        if self.total > 30000:
            s += "d"
        if self.total > 10*10**6:
            s += "GD"

        return [self.path + i for i in s]


def bfs(visited, node, goal, maxsize): #function for BFS
  visited.append(node.path)
  sep()
  best = node.priority(goal)
  queue.put(node.priority(goal))
  count = 0
  while queue and (queue.qsize()) + 5 < maxsize:          # Creating loop to visit each node
    count += 1
    if count % 100 == 0:
        print(queue.qsize())
        
    m = queue.get()[1]

    for neighbour in m.neighbours():
      if neighbour not in visited:
        visited.append(neighbour)
        temp = Orion()
        temp.walk(neighbour)
        if temp.totalWait(goal) < best[1].totalWait(goal):
            best = temp.priority(goal) 
        if temp > best[1]:
            continue
        else:
            queue.put(temp.priority(goal))
  return best

def sep():
    print("*"*80)

if __name__== "__main__":

    goal = 10**10
    maxsize = 5**5
    best = Orion()
    visited = [] # List for visited nodes
    queue = PriorityQueue()     #Initialize a queue
    # Driver Code
    print("Following is the Breadth-First Search")
    for i in range(100):
        print(i)
        best = bfs(visited, best, goal = goal, maxsize = maxsize)[1]    # function calling
        visited = [] # List for visited nodes
        queue = PriorityQueue()     #Initialize a queue
    print("Time to goal: ", "{:.2e}".format(best.totalWait(goal)))
    print(best)

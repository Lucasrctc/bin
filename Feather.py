import pickle

class Orion:
    def __init__(self):
        self.gen_costs = {}
        self.gen_lvl = 0
        self.mult_lvl = 0
        self.mult_costs = {}
        self.disc_costs = {}
        self.disc_lvl = 0
        self.state = 0

    def __str__(self):
        s = ""
        s += "Generator costs:"
        for i in self.gen_costs:
            s+="\n" + str(i) + ": " + str(self.gen_costs[i])
        s += "\nMultiplier costs:"
        for i in self.mult_costs:
            s+="\n" + str(i) + ": " + str(self.mult_costs[i])

        s += "\nDiscount costs:"
        for i in self.disc_costs:
            s+="\n" + str(i) + ": " + str(self.disc_costs[i])

        s += "\n\nState:\nGenerator level: " + str(self.gen_lvl) + "\n Multiplier level: " + str(self.mult_lvl) + "\n discout level:" + str(self.disc_lvl)
        
        s += "\nTotal discount: " + str(self.discount())
        s += "\nIncome: " + str(self.income())

        return s

    def discount(self):
        return (1 + .1 * self.disc_lvl)

    def upgrade_gen(self, value):
        self.gen_lvl += 1
        if self.gen_lvl not in self.gen_costs:
            self.gen_costs[self.gen_lvl] = value * self.discount()

    def upgrade_mult(self, value):
        self.mult_lvl += 1
        if self.mult_lvl not in self.mult_costs:
            self.mult_costs[self.mult_lvl] = value * self.discount()

    def upgrade_disc(self, value):
        self.disc_lvl += 1
        if self.disc_lvl not in self.disc_costs:
            self.disc_costs[self.disc_lvl] = value * self.discount()

    def save(self):
        with open('Orion.pickle', 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def income(self):
        return self.gen_lvl * (1 + .05 * self.mult_lvl)

    def next_incomes(self):
        return (self.gen_lvl + 1) * (1 + .05 * self.mult_lvl), self.gen_lvl * (1.05 + .05 * self.mult_lvl), (1.1 + .1 * self.disc_lvl) / self.discount()

    def decide(self):
        disc_0, disc_1, disc_2 = self.next_incomes()

        if self.gen_lvl < 20:
            disc_0 = 1
            disc_1 = 0
        elif self.mult_lvl == 0:
            disc_1 = 1
            disc_0 = 0
        else:
            disc_0 /= self.gen_costs[self.gen_lvl]
            disc_1 /= self.mult_costs[self.mult_lvl]
            if 1 in self.disc_costs:
                mincost = min(self.mult_costs[self.mult_lvl], self.gen_costs[self.gen_lvl])
                disc_2 = mincost * (disc_2 - 1)/disc_2
                print("Discriminators: ")
                print(disc_0, disc_1, disc_2)
                disc_2 = 0 if disc_2 > self.disc_costs[self.disc_lvl]/self.discount() else 2
            else:
                disc_2 = 0

        if disc_2 == 0:
            self.state = 2
            print("discount")

        elif disc_0 > disc_1:
            self.state = 0
            print("left")

        else:
            self.state = 1
            print("right")

    def curlvl(self):
        return self.gen_lvl, self.mult_lvl, self.disc_lvl

    def upgrade_skip(self):
        if self.state == 0:
            self.gen_lvl += 1
        elif self.state == 1:
            self.mult_lvl += 1
        elif self.state == 2:
            self.disc_lvl += 1

    def upgrade(self, value):
        if self.state == 0:
            self.upgrade_gen(value)
        elif self.state == 1:
            self.upgrade_mult(value)
        elif self.state == 2:
            self.upgrade_disc(value)


if __name__== "__main__":
	with open('Orion.pickle', 'rb') as handle:
	    b = pickle.load(handle)
	
	#b = Orion()
	
	def income(gen, mult):
	    return gen * (1 + .05 * mult)
	
	lvl = 0
	while True:
	    b.decide()
	    a = input()
	    if a == "q":
	        break
	    if lvl > sum(b.curlvl()):
	        b.upgrade_skip()
	    else:
	        a = int(a)
	        b.upgrade(a)
	        b.save()
	
	print(b)

import math


class CreteDetector:
    sample_params = {
        "resistor": 100_000,
        "capacity": 1e-6
    }

    def __init__(self, app, inductor, params):
        self.params = params
        self.app = app
        self.inductor = inductor 
        self.output = 0
        self.time = 0
        self.minReachedInitialCondition = 0
        self.maxReached = 5
        self.minReached = 0
        self.charge = False
        self.update_params()

    def update_params(self):
        self.time = 0

    def name(self):
        return f"Detecteur de crêtes ({self.inductor.name()})"

    def step(self, time):
        self.time += time
        if self.inductor.output >= self.output:
            if not self.charge:
                self.time = time % self.time
                self.charge = True
                self.minReached = self.output
                self.minReachedInitialCondition = self.output / self.maxReached
            self.output = self.inductor.output
        else:
            if self.charge:
                self.charge = False
                self.maxReached = self.output
                self.time = time % self.time
            self.output = self.maxReached * math.exp(-self.time/(self.params["resistor"]*self.params["capacity"]))


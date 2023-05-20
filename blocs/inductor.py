import math


class Inductor:
    COUNT = 0
    params = {
        "resistor": 330,
        "inductance": 0.00083,
    }

    def __init__(self, app, oscillator):
        self.app = app
        self.oscillator = oscillator
        self.charge = True
        self.output = 0
        self.period = 0
        self.maxReached = app.globals["vdd"]
        self.minReachedInitialCondition = 0
        self.time = 0
        self.update_params()


    def update_params(self):
        self.params = Inductor.params.copy()
        self.time = 0

    def name(self):
        return f'Inductance {self.params["inductance"]} -  {self.params["resistor"]} ohm'

    def step(self, time):
        input = self.oscillator.output
        self.time += time
        if input > 0:
            if not self.charge:
                self.time = 0
                self.charge = True
                """
                self.minReachedInitialCondition = self.output / self.maxReached
            startingPoint = 1 + self.minReachedInitialCondition
            self.output = self.maxReached * (startingPoint - math.exp(-self.time * self.params["resistor"] / self.params["inductance"]))
                """

                self.minReachedInitialCondition = self.output
            self.output = (self.app.globals["vdd"] - self.minReachedInitialCondition) * (1 - math.exp(-self.time * self.params["resistor"] / self.params["inductance"])) + self.minReachedInitialCondition

        else:
            if self.charge:
                self.charge = False
                self.time = 0
                self.maxReached = self.output
                #ourVersion =(self.app.globals["vdd"] * math.exp(-(self.app.oscillator.period/2)*self.params["resistor"]/self.params["inductance"])) / 1+(math.exp(-(self.app.oscillator.period/2)*self.params["resistor"]/self.params["inductance"]))
                #print(f"maxReached: {self.maxReached:.2f}V - inductance {self.params['inductance']}")
            self.output = self.maxReached * math.exp(-self.time * self.params["resistor"] / self.params["inductance"])


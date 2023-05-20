import math


class Oscillator:
    """
    These parameters are useless. They are just here to give you an idea of what they look like in self.params
    """


    def __init__(self, app, params):
        self.params = params
        self.app = app
        self.output = 0
        self.time = 0
        self.update_params()

    def update_params(self):
        #self.period = 2 * self.params["capacity"] * self.params["potentiometer"] * math.log(2)  # math.log is ln
        #self.period = 8.037216901779176e-6
        self.params["period"] = 1 / self.params["frequency"]
        print(self.params["period"])
        print("La fréquence de l'oscillateur vaut", 1/self.params["period"])
        self.time = 0

    def name(self):
        return f'Oscillateur {1/self.params["period"]:.2f} Hz'
    def step(self, time):
        self.time += time
        self.output = self.app.globals["vdd"]
        if self.time > (self.params["period"] / 2):
            self.output = self.app.globals["gnd"]
        if self.time > self.params["period"]:
            self.time = self.time % self.params["period"]



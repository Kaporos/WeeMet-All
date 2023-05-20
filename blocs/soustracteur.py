def san(self, d):
    return str(d).replace(".",",")
class Soustractor:
    """
    These parameters are useless. They are just here to give you an idea of what they look like in self.params
    """
    sampleParams = {
        "r4": 0,
        "r1": 0
    }

    def __init__(self, app, crete, params):
        self.params = params
        self.app = app
        self.crete = crete
        self.output = 0
        self.update_params()


    def update_params(self):
        self.time = 0

    def name(self):
        return f'Soustracteur ({self.crete.inductor.name()})'

    def step(self, time):
        input = self.crete.output
        v2 = self.app.globals["vdd"]
        self.output = max(0, min(v2, v2 *  (100_000 - self.params["r4"])*(100_000) / ((100_000)*self.params["r1"]) - ((input*(100_000 - self.params["r1"]))/self.params["r1"])))


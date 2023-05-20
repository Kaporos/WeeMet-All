import math

import blocs
import tomllib

class Line:
    def name(self):
        return f'y = {self.output}'

    def __init__(self, value):
        self.output = value


class WeMeetAll:
    def __init__(self, data):
        self.globals = {
            "gnd": 0
        }

        self.globals["vdd"] = data["global"]["vdd"]
        self.inductancesKeys = list(filter(lambda x: x.startswith("inductance"), list(data.keys())))
        self.oscillator = blocs.Oscillator(self, data["oscillator"])
        self.wanted = [self.oscillator]  if data["oscillator"]["shown"] else  []
        for (i, inductanceKey) in enumerate(self.inductancesKeys):
            inductanceData = data[inductanceKey]
            inductance = inductanceData["value"]
            i += 1
            inductor = blocs.Inductor(self, self.oscillator)
            inductor.params["inductance"] = inductance
            crete = blocs.CreteDetector(self, inductor, data["crete"])
            soustractor = blocs.Soustractor(self, crete, data["soustractor"])
            vmax = Line(self.globals["vdd"] / (1 + math.exp(
                (-1 * self.oscillator.params["period"] * inductor.params["resistor"]) / (
                            2 * inductor.params["inductance"]))))
            vmin = Line(self.globals["vdd"] * math.exp(
                (-1 * self.oscillator.params["period"] * inductor.params["resistor"]) / (
                            2 * inductor.params["inductance"])) / (1 + math.exp(
                (-1 * self.oscillator.params["period"] * inductor.params["resistor"]) / (
                            2 * inductor.params["inductance"]))))
        
            self.__dict__[f"inductor{i}"] = inductor
            self.__dict__[f"soustractor{i}"] = soustractor
            self.__dict__[f"crete{i}"] = crete
            self.__dict__[f"vmax{i}"] = vmax
            self.__dict__[f"vmin{i}"] = vmin
            try:
                if inductanceData["crete"]:
                    self.wanted.append(crete)
                if inductanceData["rl"]:
                    self.wanted.append(inductor)
                if inductanceData["soustractor"]:
                    self.wanted.append(soustractor)
                if inductanceData["vmax"]:
                    self.wanted.append(vmax)
                if inductanceData["vmin"]:
                    self.wanted.append(vmin)
            except KeyError as e :
                print("There is an error in your config.toml, you forgot property ", e, "on one of your inductances.")
                import sys; sys.exit(1)

    def step(self, time):
        self.oscillator.step(time)
        for i in range(len(self.inductancesKeys)):
            i += 1
            self.__dict__[f"inductor{i}"].step(time)
            self.__dict__[f"soustractor{i}"].step(time)
            self.__dict__[f"crete{i}"].step(time)

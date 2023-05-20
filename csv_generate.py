import wemeetall
import numpy as np
import csv, tomllib

with open("config.toml", "rb") as f:
    data = tomllib.load(f)

app = wemeetall.WeMeetAll(data)
wanted = app.wanted

# Global parameters

step = data["simulation"]["step"]
time = data["simulation"]["csv"]["time"]
#warmup = 0.00025
warmup = data["simulation"]["warmup"]
# Wanna be more precise about output ?
xOffset = data["simulation"]["csv"]["xOffset"]

shouldWaitFor = data["simulation"]["csv"]["shouldWaitFor"]
waitValue = data["simulation"]["csv"]["waitValue"]
waitItem = app.__dict__[data["simulation"]["csv"]["waitItem"]]
precision = data["simulation"]["csv"]["precision"]


outputDir = data["simulation"]["csv"]["outputDir"]

# Stepping through offset.
print("Warmup of simulation.")
for i in range(0, int(warmup // step)):
	app.step(step)

if shouldWaitFor:
	print(f"Waiting for a value of {waitItem.name()} (y = {waitValue:.2})")
	while abs(waitItem.output - waitValue) > precision:
		app.step(step)
	

count = int(time // step)
x = np.linspace(0, count * step, count)
y = np.zeros((len(wanted), count))
print("Recording simulation..")
for i in range(0, len(x)):
	app.step(step)
	for j in range(0, len(wanted)):
		y[j][i] = wanted[j].output

print("Saving to csv file..")
for i,item in enumerate(wanted):
	filename = f"{outputDir}/{item.name()} - Simulation.csv"
	print(f"Created {filename}")
	with open(filename, "w", newline="") as csvfile:
		writer = csv.writer(csvfile, delimiter=";")
		writer.writerow(["Time", "Channel A", "Channel B"])
		for j, yi in enumerate(y[i]):
			writer.writerow([xOffset  + (x[j]/1e-6), yi, 0])
			
	
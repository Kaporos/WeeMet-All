# WeeMet-All Circuit Simulation

# Usage

Just clone this repository, and edit `config.toml` to your needs !


To start animation of the simulation:

  py main.py

To generate some csv files (default output in csv_output dir): 

  py main.py csv

# Configuration

config.toml is self-explained, but i will put some details here.

Each bloc is configured once BUT.

You can simulate multiple inductances to see differences between them.

How to configure which CSV will be generated / will bloc will be shown on animation ?

For the oscillator, because it does not depend of inductance, just put `shown` to true or false. 

For everyother blocs, visibility setting is inside respective inductances blocs.

You can add as many inductances as you want, and for each, configure which bloc you wanna see on screen (or generate)





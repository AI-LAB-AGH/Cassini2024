from skfuzzy import control as ctrl
from rules import *

mobility_ctrl = ctrl.ControlSystem(rules=rules)
mobility_sim = ctrl.ControlSystemSimulation(mobility_ctrl)

def inference(terrain, vehicle, weight, speed):
    mobility_sim.input['terrain'] = terrain
    mobility_sim.input['vehicle'] = vehicle
    mobility_sim.input['weight'] = weight
    mobility_sim.input['speed'] = speed
    mobility_sim.compute()
    print(f"Mobility score: {mobility_sim.output['mobility']}")

# TERRAIN:
#     - dry: 0
#     - wet: 1
#     - snow: 2
#     - sand: 3

# VEHICLE:
#     - wheel: 0
#     - track: 1

# WEIGHT: [0, 30000]

# SPEED: [0, 100]

# terrain, veh_type, weight, speed
tests = [
    [3, 1, 13000, 80],  # .4782
    [2, 1, 13000, 32],  # .3617
    [0, 0, 22000, 80],  # .8089
    [1, 0, 32000, 32],  # .4077
    [0, 0, 9000, 96],   # .9139
    [3, 0, 22000, 63],  # .3568
    [0, 1, 11000, 72]   # .5469
]

for test in tests:
    inference(test[0], test[1], test[2], test[3])

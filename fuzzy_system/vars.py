import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

terrain = ctrl.Antecedent(np.arange(0, 4, 1), 'terrain')
vehicle = ctrl.Antecedent(np.arange(0, 2, 1), 'vehicle')
weight = ctrl.Antecedent(np.arange(0, 30001, 1), 'weight')
speed = ctrl.Antecedent(np.arange(0, 101, 1), 'speed')
mobility = ctrl.Consequent(np.arange(0., 1.01, .01), 'mobility')

terrain['dry'] = fuzz.trimf(terrain.universe, [0, 0, 0.5])
terrain['wet'] = fuzz.trimf(terrain.universe, [0.5, 1, 1.5])
terrain['snow'] = fuzz.trimf(terrain.universe, [1.5, 2, 2.5])
terrain['sand'] = fuzz.trimf(terrain.universe, [2.5, 3, 3])

vehicle['wheel'] = fuzz.trimf(vehicle.universe, [0, 0, 0.5])
vehicle['track'] = fuzz.trimf(vehicle.universe, [0.5, 1, 1])

weight['low'] = fuzz.trapmf(weight.universe, [0, 0, 10000, 13000])
weight['medium'] = fuzz.trimf(weight.universe, [10000, 16000, 22000])
weight['high'] = fuzz.trapmf(weight.universe, [19000, 22000, 30000, 30000])

speed['low'] = fuzz.trapmf(speed.universe, [0, 0, 20, 40])
speed['medium'] = fuzz.trapmf(speed.universe, [40, 40, 60, 60])
speed['high'] = fuzz.trapmf(speed.universe, [60, 80, 100, 100])

mobility['low'] = fuzz.trimf(mobility.universe, [0., 0., .2])
mobility['mediumlow'] = fuzz.trimf(mobility.universe, [.15, .30, .45])
mobility['medium'] = fuzz.trimf(mobility.universe, [.40, .50, .60])
mobility['mediumhigh'] = fuzz.trimf(mobility.universe, [.55, .70, .85])
mobility['high'] = fuzz.trimf(mobility.universe, [.80, 1., 1.])
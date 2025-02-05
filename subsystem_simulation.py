import random
import numpy as np
import time


class SubsystemSimulation:
    def __init__(self, fan_speeds):
        self.temperature = random.uniform(20, 30)  # Initial random temp between 20 and 30°C
        self.fan_speeds = fan_speeds

    def update_temperature(self):
        cooling_factor = np.mean(self.fan_speeds) / 100  # Higher fan speeds cool more
        self.temperature -= cooling_factor * 0.1  # Cooling effect
        if random.random() < 0.1:  # Random spike to simulate load
            self.temperature += random.uniform(1, 3)
        self.temperature = max(self.temperature, 20)  # Ensure temperature doesn't go below 20°C
        return self.temperature

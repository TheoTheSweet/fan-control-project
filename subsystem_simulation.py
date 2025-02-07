import random
import numpy as np

# Class to simulate the behavior of a subsystem
class SubsystemSimulation:
    def __init__(self):
        self.temperature = random.uniform(25, 45)
        self.fan_speeds = None

    """
    Description: Sets the fan speeds for the subsystem.
    Parameters: fan_speeds (list of floats)
    """
    def set_fan_speeds(self, fan_speeds):
        self.fan_speeds = fan_speeds

    """
    Description: Simulates the temperature output of the subsystem based on the current fan speeds and other factors.
    Returns: float
    """
    def output_temperature(self):
        if self.fan_speeds is None:
            return self.temperature
        cooling_factor = np.mean(self.fan_speeds) / 2000
        self.temperature -= cooling_factor * 0.5
        if random.random() < 0.2:
            self.temperature += random.uniform(1, 3)
        self.temperature = max(self.temperature, 20)
        return self.temperature

    """
    Description: Returns the current temperature of the subsystem.
    Returns: float
    """
    def get_temperature(self):
        return self.temperature

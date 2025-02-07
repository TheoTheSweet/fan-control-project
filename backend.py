import numpy as np
import pandas as pd
import time

"""Description: Backend class to handle the logic of the system. It is initialized with the number of fans, 
number of subsystems, and the maximum RPMs of the fans. It holds the fan speeds, subsystem temperatures, and logs the 
data for CSV export as well as data for the GUI graphs."""
class Backend:
    def __init__(self, num_fans, num_subsystems, max_rpms):
        self.num_fans = num_fans
        self.num_subsystems = num_subsystems
        self.max_rpms = np.array(max_rpms)
        self.fan_speeds = np.zeros(num_fans)
        self.subsystem_temperatures = np.zeros(num_subsystems)
        self.temp_log = []
        self.speed_log = []
        self.start_time = time.time()

    """
    Description: Sets the temperatures of the subsystems.
    Parameters: temperatures (list of floats)
    """
    def sample_temperatures(self, temperatures):
        if len(temperatures) == self.num_subsystems:
            self.subsystem_temperatures = np.array(temperatures)
        else:
            raise ValueError("Number of temperatures must match the number of subsystems.")

    """
    Description: Updates the fan speeds based on the maximum temperature of the subsystems.
    """
    def update_fan_speeds(self):
        max_temp = np.max(self.subsystem_temperatures)
        if max_temp <= 25:
            fan_speed_percentage = 0.20
        elif max_temp >= 75:
            fan_speed_percentage = 1.0
        else:
            fan_speed_percentage = 0.20 + (max_temp - 25) * (0.80 / 50)
        self.fan_speeds = self.max_rpms * fan_speed_percentage
        self._log_data()

    """
    Description: Logs the data for the current time step.
    """
    def _log_data(self):
        elapsed_time = time.time() - self.start_time
        self.temp_log.append((elapsed_time, self.subsystem_temperatures.copy()))
        self.speed_log.append((elapsed_time, self.fan_speeds.copy()))
        self.temp_log = [log for log in self.temp_log if log[0] > elapsed_time - 300]
        self.speed_log = [log for log in self.speed_log if log[0] > elapsed_time - 300]

    """
    Description: Requests a CSV file with the logged data.
    Returns: str
    """
    def request_csv(self):
        if not self.temp_log or not self.speed_log:
            return "No data to write."
        timestamps = [log[0] for log in self.temp_log]
        timestamps = [f"{int(t // 3600):02}:{int((t % 3600) // 60):02}:{int(t % 60):02}.{int((t % 1) * 1000):03}" for t in timestamps]
        temp_data = np.array([log[1] for log in self.temp_log])
        speed_data = np.array([log[1] for log in self.speed_log])
        temp_columns = [f"Temp{i + 1} (°C)" for i in range(self.num_subsystems)]
        speed_columns = [f"Fan{i + 1} Speed (RPM)" for i in range(self.num_fans)]
        df = pd.DataFrame({"Time (HH:MM:SS)": timestamps})
        temp_df = pd.DataFrame(temp_data, columns=temp_columns)
        speed_df = pd.DataFrame(speed_data, columns=speed_columns)
        df = pd.concat([df, temp_df, speed_df], axis=1)
        filename = "temp_speed_log.csv"
        df.to_csv(filename, index=False)
        return filename

    """
    Description: Returns the current data of the subsystem temperatures and fan speeds.
    Returns: tuple of numpy arrays
    """
    def get_current_data(self):
        return self.subsystem_temperatures, self.fan_speeds
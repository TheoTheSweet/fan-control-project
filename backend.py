import numpy as np
import pandas as pd
import time


class Backend:
    def __init__(self, num_fans, num_subsystems, max_rpms):
        """
        Initialize the system with fan details and subsystem settings.

        :param num_fans: Number of fans
        :param num_subsystems: Number of subsystems
        :param max_rpms: List of maximum RPMs for each fan
        """
        self.num_fans = num_fans
        self.num_subsystems = num_subsystems
        self.max_rpms = np.array(max_rpms)  # List of maximum RPMs for each fan
        self.fan_speeds = np.zeros(num_fans)  # Fan speeds (in RPM) initialized to 0
        self.subsystem_temperatures = np.zeros(num_subsystems)  # Subsystem temperatures (°C)

        # To store the data for the last 5 minutes
        self.temp_log = []  # List to store temperature logs
        self.speed_log = []  # List to store fan speed logs

        # Timestamps will be recorded since initialization
        self.start_time = time.time()

    def update_temperatures(self, temperatures):
        """
        Update the subsystem temperatures.

        :param temperatures: List or numpy array of new temperatures from subsystems
        """
        if len(temperatures) == self.num_subsystems:
            self.subsystem_temperatures = np.array(temperatures)
        else:
            raise ValueError("Number of temperatures must match the number of subsystems.")

    def update_fan_speeds(self):
        """
        Update fan speeds based on the current subsystem temperatures.
        """
        max_temp = np.max(self.subsystem_temperatures)

        # Calculate the fan speed percentage based on temperature
        if max_temp <= 25:
            fan_speed_percentage = 0.20  # 20% max speed
        elif max_temp >= 75:
            fan_speed_percentage = 1.0  # 100% max speed
        else:
            # Linear interpolation between 25°C (20%) and 75°C (100%)
            fan_speed_percentage = 0.20 + (max_temp - 25) * (0.80 / 50)  # 50°C range between 20% and 100%

        # Update fan speeds according to the percentage of each fan's max RPM
        self.fan_speeds = self.max_rpms * fan_speed_percentage
        self._log_data()

    def _log_data(self):
        """
        Log the temperature and fan speeds at the current time.
        """
        elapsed_time = time.time() - self.start_time
        self.temp_log.append((elapsed_time, self.subsystem_temperatures.copy()))
        self.speed_log.append((elapsed_time, self.fan_speeds.copy()))

        # Keep only the last 5 minutes of data (300 seconds)
        self.temp_log = [log for log in self.temp_log if log[0] > elapsed_time - 300]
        self.speed_log = [log for log in self.speed_log if log[0] > elapsed_time - 300]

    def request_csv(self):
        if not self.temp_log or not self.speed_log:
            return "No data to write."

        # Extract timestamps, temperatures, and fan speeds
        timestamps = [log[0] for log in self.temp_log]
        # convert to hh:mm:ss format
        timestamps = [f"{int(t // 3600):02}:{int((t % 3600) // 60):02}:{int(t % 60):02}.{int((t % 1) * 1000):03}" for t in timestamps]
        temp_data = np.array([log[1] for log in self.temp_log])
        speed_data = np.array([log[1] for log in self.speed_log])

        # Create column names
        temp_columns = [f"Temp{i + 1} (°C)" for i in range(self.num_subsystems)]
        speed_columns = [f"Fan{i + 1} Speed (RPM)" for i in range(self.num_fans)]

        # Combine into a DataFrame
        df = pd.DataFrame({"Time (HH:MM:SS)": timestamps})
        temp_df = pd.DataFrame(temp_data, columns=temp_columns)
        speed_df = pd.DataFrame(speed_data, columns=speed_columns)

        df = pd.concat([df, temp_df, speed_df], axis=1)

        # Save to CSV
        filename = "temp_speed_log.csv"
        df.to_csv(filename, index=False)
        return filename

    def get_current_data(self):
        """
        Get current temperature and fan speed data.

        :return: Current data (temperature, fan speed)
        Both outputs are numpy arrays.
        """
        return self.subsystem_temperatures, self.fan_speeds


# Example usage (this would typically be in the main program)
if __name__ == "__main__":
    num_fans = 3
    num_subsystems = 5
    max_rpms = [3000, 2500, 3500]  # Different max RPMs for each fan

    system = Backend(num_fans, num_subsystems, max_rpms)

    # Example: Simulating new temperature readings
    # sleep for 0.1 seconds to simulate real-time data
    # initial temperatures
    initial_temperatures = [30, 40, 50, 60, 55]
    for i in range(10):
        new_temperatures = [temp + np.random.uniform(-20, 20) for temp in initial_temperatures]
        system.update_temperatures(new_temperatures)
        system.update_fan_speeds()
        time.sleep(0.1)

    # Print current data
    temperatures, fan_speeds = system.get_current_data()
    print("Current Temperatures:", temperatures)
    print("Current Fan Speeds:", fan_speeds)

    # Request CSV file
    filename = system.request_csv()
    print(f"CSV file created: {filename}")

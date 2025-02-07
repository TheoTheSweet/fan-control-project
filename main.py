import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from backend import Backend
from subsystem_simulation import SubsystemSimulation
from ui import UI

'''
Description: Main application class that handles the logic of the system. It initializes the backend, subsystems, and UI.
'''
class MainApp:
    def __init__(self):
        self.state = "menu"
        self.backend = None
        self.ui = UI(self)
        self.ui.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
        self.timer10cycles = 0
        self.subsystems = []
        self.start_time = None

    """
    Description: Updates the application based on the current state.
    """
    def update(self):
        if self.state == "menu":
            pass  # Menu state logic handled by UI
        elif self.state == "data_tracking":
            self.run_data_tracking()

    """
    Description: Runs the data tracking logic for the application. It samples the temperatures of the subsystems, updates
    the fan speeds, and logs the data.
    """
    def run_data_tracking(self):
        if self.backend is None:
            print("Backend is not initialized.")
            return
        try:
            # Update subsystem temperatures
            new_temperatures = [subsystem.output_temperature() for subsystem in self.subsystems]

            self.timer10cycles += 1
            if self.timer10cycles == 10:
                self.timer10cycles = 0
                self.backend.sample_temperatures(new_temperatures)
                self.backend.update_fan_speeds()

                # Update the fan speeds in subsystems
                for subsystem in self.subsystems:
                    subsystem.set_fan_speeds(self.backend.fan_speeds)
                # temperatures, fan_speeds = self.backend.get_current_data()
                # print("Current Temperatures:", temperatures)
                # print("Current Fan Speeds:", fan_speeds)

                # Update UI
                self.ui.update_ui()
        except Exception as e:
            print(f"Error in run_data_tracking: {e}")

    """
    Description: Changes the state of the application.
    Parameters: new_state (str)
    """
    def change_state(self, new_state):
        try:
            if new_state == "menu":
                print("Changing state to menu")
                self.state = "menu"
                self.ui.init_ui()
                self.backend = None
                self.subsystems = []
            elif new_state == "data_tracking":
                print("Changing state to data_tracking")
                if self.backend is None:
                    print("Backend is not initialized.")
                    return
                self.state = "data_tracking"
                self.ui.setup_data_tracking_ui()
                self.start_time = time.time()
                print("UI setup for data tracking")
        except Exception as e:
            print(f"Error in change_state: {e}")

    """
    Description: Initializes the application with the specified number of fans, subsystems, and maximum RPMs.
    Parameters: num_fans (int), num_subsystems (int), max_rpms (list of floats
    """
    def initialize(self, num_fans, num_subsystems, max_rpms):
        try:
            self.backend = Backend(num_fans, num_subsystems, max_rpms)
            self.subsystems = [SubsystemSimulation() for _ in range(num_subsystems)]
            self.ui.backend = self.backend  # Update the UI's backend reference
            self.change_state("data_tracking")
            print("MainApp fully initialized for the data tracking state.")
        except Exception as e:
            print(f"Error in initialize: {e}")

    """
    Description: Quits the application.
    """
    def quit_application(self):
        QApplication.quit()

    """
    Description: Returns the elapsed time since the start of the data tracking state.
    Returns: str
    """
    def get_elapsed_time(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            return f"{elapsed // 3600:02}:{(elapsed % 3600) // 60:02}:{elapsed % 60:02}"
        return "00:00:00"

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())

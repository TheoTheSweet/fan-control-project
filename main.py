import time
from backend import Backend
from subsystem_simulation import SubsystemSimulation
from ui import UI
from PyQt6.QtWidgets import QApplication


def main():
    num_fans = 3
    num_subsystems = 5
    max_rpm = 3000

    backend = Backend(num_fans, num_subsystems, max_rpm)
    ui = UI(backend)

    # Simulating subsystems
    subsystems = [SubsystemSimulation(backend.fan_speeds) for _ in range(num_subsystems)]

    app = QApplication([])

    # Main simulation loop
    while True:
        # Update subsystem temperatures
        new_temperatures = [subsystem.update_temperature() for subsystem in subsystems]
        backend.update_temperatures(new_temperatures)

        ui.update_ui()
        time.sleep(0.1)


if __name__ == '__main__':
    main()

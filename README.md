# Fan Control System

This project simulates a fan control system for a robot with multiple subsystems. The system monitors temperatures, adjusts fan speeds, and logs data. The user can interact with the system via a graphical user interface (GUI) built with PyQt6.

## Requirements
- numpy
- pandas
- pyqtgraph
- pyqt6

## Running the Application
1. Install the required libraries using `pip install numpy pandas pyqtgraph pyqt6`.
2. Run the `main.py` script: `python main.py`.
3. The GUI will allow you to configure the system, view real-time data, and export it to a CSV file.

## Structure
- `backend.py`: Manages fan speed, temperature data, and control logic.
- `subsystem_simulation.py`: Simulates subsystem behavior and temperature variations.
- `ui.py`: Provides a GUI for user interaction.
- `main.py`: Runs the application.

## Notes
The system simulates fan speeds and temperatures in real-time, updating every 0.1 seconds. The CSV export functionality allows for saving system data for analysis.

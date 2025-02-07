# Robotic Subsystem Fan Control and Data Log

This application simulates fan control for the cooling of robotic subsystems. It allows the user to set the number of fans and subsystems, along with the maximum RPM for each fan. The application tracks temperature and fan speed data over time and provides a graphical interface to monitor the data. If requested, the application can also log the data to a CSV file, which has the name 'temp_speed_log.csv'. Keep in mind that the file will be overwritten upon each new request to log data.

## How to Use

### Option 1: Running the Prebuilt Executable (Recommended)
1. **Locate the Executable**  
   - The standalone executable `FanController.exe` is provided in the `dist/` directory of the project.  

2. **Run the Application**  
   - Navigate to the `dist/` folder and double-click `FanController.exe` to start the application.  
   - No additional installation is required.  

3. **Best Display Settings**  
   - **For the best experience, maximize or fullscreen the application window.**  
   - This ensures all UI elements and data visualizations are properly displayed.

### Option 2: Running the Application from Source
If you prefer to run the application using Python instead of the prebuilt executable, follow these steps:

1. **Download the Required Files**  
   - Ensure you have the following files in the same directory:  
     - `main.py`  
     - `backend.py`  
     - `subsystem_simulation.py`  
     - `ui.py`  

2. **Install Required Libraries**  
   - You need the following Python libraries:  
     - `PyQt6`  
     - `numpy`  
     - `pandas`  
     - `matplotlib`  
   - Install them using:  
     ```bash
     pip install PyQt6 numpy pandas matplotlib
     ```

3. **Run the Application**  
   ```bash
   python main.py
   ```

4. **Maximize the Window**
   - If running from source, ensure the application window is maximized for the best UI experience.

## Project Structure

The project is organized as follows:

- `main.py`: This is the main script to run the application. It initializes the UI, backend, and subsystem simulations. It functions as a state machine to handle user inputs and update the UI, while passing data between the other module scripts.
- `backend.py`: Contains the backend logic for controlling the fans and logging data. It stores the last 300 data points for temperature and fan speed.
- `ui.py`: Defines the graphical user interface using PyQt6. There are two UI states: one for setting the fan parameters and another for displaying the temperature and fan speed data.
- `subsystem_simulation.py`: Simulates the subsystems and provides temperature outputs to the backend. The output temperatures have some random component to simulate real-world conditions, and are also based off the fan speeds.

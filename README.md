# Robotic Subsystem Fan Control and Data Log

This application simulates fan control for the cooling of robotic subsystems. It allows you to set the number of fans and subsystems, along with the maximum RPM for each fan. The application tracks temperature and fan speed data over time and provides a graphical interface to monitor the data.

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

- `main.py`: Initializes and runs the application.
- `backend.py`: Implements the core functionality and business logic.
- `ui.py`: Defines the graphical user interface using PyQt6.
- `subsystem_simulation.py`: Simulates the subsystems and provides temperature outputs to the backend.

# STEP File Face Coloring Tool

A lightweight **Python application** for Windows that orients a solid body and colors faces of STEP files (`.stp` / `.step`) according to user-defined criteria.
The app provides a **simple graphical interface** and outputs a new STEP file with “\_colored” appended to the original filename.

---

## ✨ Features

- **Automatic orientation** of the solid body based on defined criteria.
- **Face selection & coloring** according to specified properties.
- Supports both **`.stp` and `.step`** file formats.
- Generates output files named:

  ```
  original_filename_colored.step
  ```

- **Simplistic GUI** – select files and criteria with just a few clicks.
- Full **source code and build files** for easy tweaking.

---

## 🛠 Requirements

- **Windows 10 or later**
- **Python 3.10** (included in the setup)
- **Administrator privileges** (for installation)
- **Internet connection** (for downloading dependencies)

---

## 🖥 Windows Setup

### Automatic Installation (Recommended)

1. **Download the application**
   - Download the ZIP file from the repository and extract it to your desired location
   - Or clone the repository using Git:
     ```
     git clone https://github.com/yourusername/STEP-file-face-coloring-tool.git
     ```

2. **Run the setup script**
   - Navigate to the extracted folder
   - Right-click on `setup.bat` and select **Run as administrator**
   - Follow the on-screen instructions
   - The setup will:
     - Install Python 3.10 if not already installed
     - Install all required dependencies
     - Create a desktop shortcut
     - Create a run script

3. **Launch the application**
   - Double-click the desktop shortcut named "STEP File Face Coloring Tool"
   - Or run `run.bat` from the application folder

### Manual Installation (Advanced)

If you prefer to set up the environment manually:

1. **Install Python 3.10**
   - Download Python 3.10 from [python.org](https://www.python.org/downloads/windows/)
   - During installation, select "Add Python to PATH"

2. **Install dependencies**
   Open Command Prompt as administrator and run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```
   python main.py
   ```

---

## ▶️ Usage

### Windows
1. **Using Desktop Shortcut**
   - Double-click the "STEP File Face Coloring Tool" shortcut on your desktop

2. **Using Run Script**
   - Navigate to the application folder
   - Double-click `run.bat`

3. **From Command Line**
   ```
   python main.py
   ```
   or
   ```
   .\run.bat
   ```

### Other Platforms
1. Launch the app:
   ```bash
   python main.py
   ```

2. In the GUI:

   - Click **Select File** to choose a `.stp` or `.step` file.
   - Adjust orientation / coloring criteria if needed.
   - Click **Process File**.

3. The colored STEP file will be saved in the same folder as:

   ```
   original_filename_colored.step
   ```

---

## 📂 Project Structure

```
STEP-file-face-coloring-tool/
├─ main.py                    # Application entry point
├─ gui/                       # GUI components
│  ├─ __init__.py
│  └─ main_window.py         # Main GUI window with PyQt5
├─ core/                      # STEP processing logic
│  ├─ __init__.py
│  └─ step_processor.py      # STEP file processing and coloring
├─ stp_files/                # Sample STEP files for testing
├─ requirements.txt          # Python dependencies (pip)
├─ environment.yml           # Conda environment specification
├─ setup.sh                 # Setup script (creates venv, installs deps)
├─ setup_conda.sh           # Conda setup script (installs Miniforge + env)
├─ run.sh                   # Run script (activates venv, runs app)
├─ run_conda.sh             # Run script (activates conda env, runs app)
├─ install.py               # Python installation script
├─ test_structure.py        # Project structure verification
└─ README.md
```

## 🚀 Quick Start Linux

### Option 1: Conda Setup (Recommended - Hybrid conda/pip approach)

```bash
# Make conda setup script executable and run it
chmod +x setup_conda.sh
./setup_conda.sh

# Run the application
./run_conda.sh
```

**Note**: This uses a hybrid approach:

- **Conda**: Installs `occt`, `pyqt`, `numpy` (system dependencies)
- **Pip**: Installs `pythonocc-core` (Python bindings)

### Option 2: Using Virtual Environment Setup

```bash
# Make setup script executable and run it
chmod +x setup.sh
./setup.sh

# Run the application
./run.sh
```

### Option 3: Manual Conda Setup

```bash
# Install Miniforge (if conda not available)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/miniforge.sh
bash /tmp/miniforge.sh -b -p $HOME/miniforge3
$HOME/miniforge3/bin/conda init zsh
source ~/.zshrc

# Create environment and install dependencies
conda env create -f environment.yml
conda activate step-face-coloring

# Run the application
python main.py
```

### Option 4: Manual Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 5: Using Python Installation Script

```bash
python3 install.py
python main.py
```

---

## 🐳 Docker

The project includes a production-ready `Dockerfile` that builds a single conda environment (`step-env`) and installs extra pip packages. This makes local development and deployments reproducible.

### Build

```bash
docker build -t step-file-face-coloring:latest .
```

### Run (default command runs `python main.py` inside `step-env`)

```bash
docker run --rm -it step-file-face-coloring:latest
```

### Override command at runtime

```bash
docker run --rm -it step-file-face-coloring:latest python -m pip list
docker run --rm -it step-file-face-coloring:latest python core/step_processor.py --help
```

### Mount local STEP files into the container

- Linux/macOS:

  ```bash
  docker run --rm -it \
    -v "$(pwd)/stp_files:/app/stp_files" \
    step-file-face-coloring:latest
  ```

- Windows PowerShell:

  ```powershell
  docker run --rm -it `
    -v ${PWD}/stp_files:/app/stp_files `
    step-file-face-coloring:latest
  ```

### Notes for GUI (PyQt5/VTK) inside Docker

Running GUI apps in containers needs display access:

- Linux with X11:

  ```bash
  xhost +local:root
  docker run --rm -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    --device /dev/dri \
    step-file-face-coloring:latest
  ```

- Windows/macOS (Docker Desktop): use an X server (e.g., VcXsrv on Windows, XQuartz on macOS) and set `DISPLAY` accordingly, or run the app in batch/headless modes if available.

---

## 🔧 Development

### Testing Project Structure

```bash
python3 test_structure.py
```

### Dependencies

- **pythonocc-core**: For STEP file processing and CAD operations
- **PyQt5**: For the graphical user interface
- **numpy**: For numerical operations and color generation

### Key Components

- **`core/step_processor.py`**: Handles STEP file loading, orientation, and face coloring
- **`gui/main_window.py`**: PyQt5-based GUI with file selection and processing controls
- **`main.py`**: Application entry point with error handling

---

## 🐛 Troubleshooting

### Common Issues

1. **"pythonocc-core installation fails"**

   - **Recommended**: Use hybrid conda/pip setup: `./setup_conda.sh`
   - The setup installs system dependencies via conda (`occt`, `pyqt`, `numpy`) and Python bindings via pip (`pythonocc-core`)
   - Ensure you have the required system dependencies
   - On Ubuntu/Debian: `sudo apt-get install libgl1-mesa-glx libglu1-mesa`

2. **"PyQt5 not found"**

   - **Recommended**: Use conda setup: `./setup_conda.sh`
   - Install system packages: `sudo apt-get install python3-pyqt5`
   - Or use pip: `pip install PyQt5`

3. **Windows-specific Issues**
   - If you get a "Windows protected your PC" message when running the setup:
     1. Right-click on `setup.bat`
     2. Select "Properties"
     3. Check "Unblock" at the bottom of the General tab
     4. Click "Apply" and try running again
   - If Python is not found after installation:
     1. Restart your computer to update environment variables
     2. Or manually add Python to your system PATH

4. **"Permission denied" on setup scripts** (Linux/macOS)
   - Make executable: `chmod +x setup.sh setup_conda.sh run.sh run_conda.sh`

5. **Virtual environment issues**

   - Ensure python3-venv is installed: `sudo apt-get install python3-venv`
   - Or use conda setup instead: `./setup_conda.sh`

5. **Conda not found**

   - Run `./setup_conda.sh` which will install Miniforge automatically
   - Or manually install Miniforge from: https://github.com/conda-forge/miniforge

6. **GUI not displaying (WSL2)**
   - Ensure WSLg is enabled (Windows 11)
   - Or install X server: `sudo apt-get install x11-apps` and use `export DISPLAY=:0`

### Testing

The project includes sample STEP files in the `stp_files/` directory for testing the application functionality.

# Chemical Equipment Parameter Visualizer

A hybrid application (Django Backend + PyQt5 Desktop App) for visualizing equipment data.

## Features
- CSV Upload and Parsing
- Summary Statistics (Count, Averages)
- Equipment Type Distribution Charts
- Upload History
- Desktop GUI

## Setup Instructions

### Backend
1. Navigate to `backend/` folder.
2. Install dependencies:
   ```bash
   pip install django djangorestframework pandas django-cors-headers reportlab
   ```
3. Run Migrations:
   ```bash
   python manage.py migrate
   ```
4. Start Server:
   ```bash
   python manage.py runserver
   ```
   Server runs at `http://127.0.0.1:8000/`.

### Desktop App
1. Navigate to `frontend-desktop/` folder (or root).
2. Install dependencies:
   ```bash
   pip install PyQt5 matplotlib requests
   ```
3. Run the App:
   ```bash
   python frontend-desktop/main.py
   ```

### Web Frontend (React)
1. **Prerequisite**: Ensure Node.js is installed.
2. Navigate to `frontend-web/` folder.
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start Development Server:
   ```bash
   npm run dev
   ```
   Or use the provided script: `run_frontend.bat`.
   
   Access at `http://localhost:5173`.
   
### Helper Scripts (Windows)
We have provided easy-to-use batch scripts in the root directory:
- `run_backend.bat`: Sets up environment and starts Django.
- `run_frontend.bat`: Installs dependencies and starts React.

## Usage

### 1. Start the Backend (Required)
Open a terminal in the root directory and run:
```bash
run_backend.bat
```
*Or manually: activates venv and runs `python manage.py runserver` inside `backend/`.*

### 2. Run the Web Version
Open a new terminal and run:
```bash
run_frontend.bat
```
*Or manually: `cd frontend-web` and `npm run dev`.*
- Open `http://localhost:5173` in your browser.

### 3. Run the Desktop Version
Open a new terminal and run:
```bash
python frontend-desktop/main.py
```
*(Ensure `.venv` is active and dependencies are installed).*

### Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

### Common Actions
1. **Upload Data**: Use "Upload New CSV" to upload `sample_equipment_data.csv`.
2. **Visualize**: View Stats, Charts, and Data in the respective tabs.

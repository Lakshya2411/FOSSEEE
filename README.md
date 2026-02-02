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

## Note on Web Frontend
The Web Frontend (React) setup requires Node.js, which was not detected in the environment. Thus only the Desktop frontend is implemented.

## Usage
1. Start the Backend Server.
2. Launch the Desktop App.
3. Click "Login" (Enter any credentials).
4. Use "Upload New CSV" to upload `sample_equipment_data.csv`.
5. View Stats, Charts, and Data in the tabs.

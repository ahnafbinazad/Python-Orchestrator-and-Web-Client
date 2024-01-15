# Social Trip Planning Application

## Overview

This project serves as the backend API for a social trip planning website. It consists of two primary components: the **Client** and the **Orchestrator**. The Orchestrator handles user registration, login processes, and trip proposal functionalities, while the Client interacts with the Orchestrator to provide a seamless user experience.

## Tech Stack

### Orchestrator Service:

- **Programming Language:** Python
- **Web Framework:** Flask
- **Database:** TinyDB
- **External Services:**
  - RandomIdService
  - WeatherForecastService
- **Deployment:** Gunicorn

### Python Client:

- **Frontend:**
  - HTML/CSS/JavaScript
  - jQuery for AJAX requests

## Key Features

- User registration and login functionalities.
- Trip proposal and planning features.
- Real-time weather information integration.
- Express interest in proposed trips.
- Scalable and modular architecture for future enhancements.

## How to Set Up

### Orchestrator Setup

1. **Install Dependencies:**

   - **Windows:**
     ```bash
     pip install -r orchestrator_service/requirements.txt
     ```

   - **Mac:**
     ```bash
     pip3 install -r orchestrator_service/requirements.txt
     ```

2. **Start Orchestrator Server:**

   - Navigate to the Orchestrator package directory in the terminal.

   - **Windows:**
     ```bash
     cd orchestrator_service
     gunicorn -w 4 -b 0.0.0.0:8000 orchestrator_service:app
     ```

   - **Mac:**
     ```bash
     cd orchestrator_service
     gunicorn -w 4 -b 0.0.0.0:8000 orchestrator_service:app
     ```

   Adjust the `-w` (workers) and `-b` (bind) parameters as needed.

### Client Setup

1. **Install Dependencies:**

   - **Windows:**
     ```bash
     pip install -r client/requirements.txt
     ```

   - **Mac:**
     ```bash
     pip3 install -r client/requirements.txt
     ```

2. **Run Client Application:**

   - **Windows:**
     ```bash
     python client/app.py
     ```

   - **Mac:**
     ```bash
     python3 client/app.py
     ```

3. **Change Client Port (Optional):**

   - Open `client/app.py` and locate the line:
     ```python
     app.run(debug=False, port=8080)
     ```
   - Change the `port` parameter to the desired port number.

4. **Access the Application:**

   Open your web browser and navigate to the specified port to use the application.


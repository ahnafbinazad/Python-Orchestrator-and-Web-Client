# Project Overview

This project consists of two separate components: the **Client** and the **Orchestrator**. Follow the instructions below to set up and run both components.

## Orchestrator Setup

1. **Install Dependencies:**

   - **Windows:**
     ```bash
     pip install -r requirements.txt
     ```

   - **Mac:**
     ```bash
     pip3 install -r requirements.txt
     ```

2. **Start Orchestrator Server:**

   - Navigate to the Orchestrator package directory in the terminal.

   - **Windows:**
     ```bash
     cd path/to/orchestrator_package
     gunicorn -w 4 -b 0.0.0.0:8000 orchestrator_service:app
     ```

   - **Mac:**
     ```bash
     cd path/to/orchestrator_package
     gunicorn -w 4 -b 0.0.0.0:8000 orchestrator_service:app
     ```

   Adjust the `-w` (workers) and `-b` (bind) parameters as needed. Change the port or processor count accordingly.

## Client Setup

1. **Install Dependencies:**

   - **Windows:**
     ```bash
     pip install -r requirements.txt
     ```

   - **Mac:**
     ```bash
     pip3 install -r requirements.txt
     ```

2. **Run Client Application:**

   - **Windows:**
     ```bash
     python app.py
     ```

   - **Mac:**
     ```bash
     python3 app.py
     ```

3. **Change Client Port (Optional):**

   - Open `app.py` and locate the line:
     ```python
     app.run(debug=False, port=8080)
     ```
   - Change the `port` parameter to the desired port number.

4. **Access the Application:**

   Open your web browser and navigate to the specified port to use the application.
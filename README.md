
# Commutify: Measuring Urban Access

Commutify is a Python application that generates heatmaps to measure urban access based on public transportation points like bus stops and metro stations.

## Requirements

- Python 3.7+

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LucasZick/Commutify
   cd commutify
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Set the FLASK_APP environment variable:**

   On Linux/MacOS:
   ```bash
   export FLASK_APP=app.py
   ```

   On Windows:
   ```bash
   set FLASK_APP=app.py
   ```

2. **Start the Flask server:**

   ```bash
   flask run
   ```
   
   or
   
   ```bash
   python app.py
   ```

3. **Access the application:**

   Open your browser and go to `http://127.0.0.1:5000/`.

## Project Structure

```plaintext
commutify/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── README.md
```

- `app.py`: Main Flask application file.
- `requirements.txt`: Project dependencies.
- `templates/`: Directory for HTML templates.

## License

This project is licensed under the MIT License.

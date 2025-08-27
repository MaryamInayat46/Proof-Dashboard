# Proof Dashboard

Proof Dashboard is a Flask-based task management and file proof system.  
It allows teams to create, update, delete, and visualize tasks with file uploads (PDF, Word, Excel, Images) and multiple links.  
The dashboard also includes interactive graphs to track team and project activities.

---

## 🚀 Features
- CRUD operations (Add, Edit, Delete tasks).
- Upload multiple files (PDF, Word, Excel, Images, etc.).
- Add multiple dynamic links for each task.
- Visual graphs for better visibility of projects and teams.
- File management (download, delete).
- SQLite database with Flask-Migrate support.

---

## 🛠️ Tech Stack
- **Backend**: Flask, SQLAlchemy, Flask-Migrate  
- **Frontend**: Jinja2, Bootstrap  
- **Database**: SQLite (default, easy to switch to MySQL/Postgres)  
- **Graphs**: Chart.js  

---

## 📂 Project Structure
Proof-Dashboard/
│── app.py # Main Flask application
│── requirements.txt # Python dependencies
│── README.md # Project documentation
│── .gitignore # Ignored files for Git
│── /templates # HTML templates
│── /static # CSS, JS, Images
│── /uploads # Uploaded files (ignored in git)
│── /migrations # Database migrations

yaml
Copy code

---

## ⚡ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/proof-dashboard.git
cd proof-dashboard
2. Create virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the app
bash
Copy code
python app.py
App will run at: http://127.0.0.1:5000/

📊 Future Improvements
User authentication system

Role-based access (Admin, Team Member)

Cloud file storage (S3, GCP, Azure)

More advanced analytics

👨‍💻 Author
Developed by Your Name

📧 Contact: your.email@example.com

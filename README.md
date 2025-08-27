# 📊 Proof Dashboard

**Proof Dashboard** is a Flask-based task management and file proofing system.  
It allows teams to create, update, delete, and visualize tasks with file uploads (PDF, Word, Excel, Images) and multiple links.  
The dashboard also includes interactive graphs to track team and project activities.

---

## 🚀 Features
- ✅ CRUD operations (Add, Edit, Delete tasks).  
- 📂 Upload multiple files (PDF, Word, Excel, Images, etc.).  
- 🔗 Add multiple dynamic links for each task.  
- 📊 Visual graphs for better visibility of projects and teams.  
- 📥 File management (download, delete).  
- 🗄️ SQLite database with Flask-Migrate support.  

---

## 🛠️ Tech Stack
- **Backend**: Flask, SQLAlchemy, Flask-Migrate  
- **Frontend**: Jinja2, Bootstrap  
- **Database**: SQLite (default, can switch to MySQL/Postgres)  
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


---

## ⚡ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/proof-dashboard.git
cd proof-dashboard

2️⃣ Create a virtual environment
python -m venv venv

Activate it:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
python app.py


App will be available at: http://127.0.0.1:5000/
 🎉

🔮 Future Improvements

🔑 User authentication system

👥 Role-based access (Admin, Team Member)

☁️ Cloud file storage (AWS S3, GCP, Azure)

📈 More advanced analytics

👨‍💻 Author

Developed by Your Name
📧 Contact: maryam.inayat21@gmail.com

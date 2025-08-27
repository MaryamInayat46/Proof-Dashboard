from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os, json
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['SECRET_KEY'] = "supersecretkey"

# Initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(50), nullable=False)
    project = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    links = db.Column(db.Text, nullable=True)  # JSON string
    files = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Home & Create Task
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team = request.form['team']
        project = request.form['project']
        task_type = request.form['task_type']
        description = request.form['description']

        # Handle multiple links
        links = request.form.getlist('links[]')
        links = [link for link in links if link.strip()]
        links_json = json.dumps(links) if links else None

        # Handle multiple files
        uploaded_files = request.files.getlist('files[]')
        file_names = []
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        for file in uploaded_files:
            if file and file.filename.strip():
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_names.append(filename)
        files_json = json.dumps(file_names) if file_names else None

        new_task = Task(team=team, project=project, task_type=task_type,
                        description=description, links=links_json, files=files_json)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for('index'))

    # Filters
    filter_team = request.args.get("team")
    filter_project = request.args.get("project")

    query = Task.query
    if filter_team and filter_team != "All":
        query = query.filter_by(team=filter_team)
    if filter_project and filter_project != "All":
        query = query.filter_by(project=filter_project)

    tasks_raw = query.order_by(Task.created_at.desc()).all()

    # Parse JSON for links and files
    tasks = []
    for t in tasks_raw:
        tasks.append({
            "id": t.id,
            "team": t.team,
            "project": t.project,
            "task_type": t.task_type,
            "description": t.description,
            "links": json.loads(t.links) if t.links else [],
            "files": json.loads(t.files) if t.files else [],
            "created_at": t.created_at
        })

    teams = db.session.query(Task.team).distinct()
    projects = db.session.query(Task.project).distinct()

    tasks_per_team = db.session.query(Task.team, db.func.count(Task.id)).group_by(Task.team).all()
    tasks_per_project = db.session.query(Task.project, db.func.count(Task.id)).group_by(Task.project).all()
    tasks_per_type = db.session.query(Task.task_type, db.func.count(Task.id)).group_by(Task.task_type).all()

    return render_template("index.html", tasks=tasks, teams=teams, projects=projects,
                           tasks_per_team=tasks_per_team, tasks_per_project=tasks_per_project,
                           tasks_per_type=tasks_per_type)

# Delete Task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.files:
        for f in json.loads(task.files):
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
            except:
                pass
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "danger")
    return redirect(url_for('index'))

# Edit Task
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.team = request.form['team']
        task.project = request.form['project']
        task.task_type = request.form['task_type']
        task.description = request.form['description']

        links = request.form.getlist('links[]')
        links = [link for link in links if link.strip()]
        task.links = json.dumps(links) if links else None

        uploaded_files = request.files.getlist('files[]')
        existing_files = json.loads(task.files) if task.files else []
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        for file in uploaded_files:
            if file and file.filename.strip():
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                existing_files.append(filename)
        task.files = json.dumps(existing_files) if existing_files else None

        db.session.commit()
        flash("Task updated successfully!", "info")
        return redirect(url_for('index'))

    existing_links = json.loads(task.links) if task.links else []
    existing_files = json.loads(task.files) if task.files else []

    return render_template("edit.html", task=task, existing_links=existing_links, existing_files=existing_files)

# Delete individual file
@app.route("/delete_file/<int:task_id>/<filename>")
def delete_file(task_id, filename):
    task = Task.query.get_or_404(task_id)
    if task.files:
        files = json.loads(task.files)
        if filename in files:
            files.remove(filename)
            task.files = json.dumps(files) if files else None
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except:
                pass
            db.session.commit()
            flash(f"File '{filename}' deleted successfully!", "warning")
    return redirect(url_for('edit_task', task_id=task_id))

# Delete individual link
@app.route("/delete_link/<int:task_id>/<int:index>")
def delete_link(task_id, index):
    task = Task.query.get_or_404(task_id)
    if task.links:
        links = json.loads(task.links)
        if 0 <= index < len(links):
            removed_link = links.pop(index)
            task.links = json.dumps(links) if links else None
            db.session.commit()
            flash(f"Link '{removed_link}' deleted successfully!", "warning")
    return redirect(url_for('edit_task', task_id=task_id))

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

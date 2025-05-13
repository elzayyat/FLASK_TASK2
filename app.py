from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, Task, User
from forms import AddTaskForm, LoginForm, RegistrationForm

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'klmecmecmdmiomowe  cowencoeniow nodeiioweono'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_tasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {user.username}! You have successfully logged in', 'success')
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('show_tasks')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('show_tasks'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/tasks')
@login_required
def show_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task(title=form.task.data, complete=form.complete.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('show_tasks'))
    return render_template('add_task.html', form=form)

@app.route('/complete/<int:id>')
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You cannot modify this task!', 'danger')
        return redirect(url_for('show_tasks'))
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('show_tasks'))

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You cannot delete this task!', 'danger')
        return redirect(url_for('show_tasks'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('show_tasks'))

# Add this route after your other routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard', 'danger')
        return redirect(url_for('show_tasks'))
    
    # Get all users and their tasks
    users = User.query.all()
    all_tasks = Task.query.all()
    
    return render_template('admin_dashboard.html', users=users, tasks=all_tasks)

# Add this function at the bottom of your file, before the if __name__ == '__main__' block
def create_admin_user():
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin is None:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('adminpassword')  # Set a secure password in production
        db.session.add(admin)
        db.session.commit()
        print('Admin user created!')
    else:
        print('Admin user already exists!')

# Modify your if __name__ == '__main__' block
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        create_admin_user()  # Create admin user if it doesn't exist
    app.run(debug=True)
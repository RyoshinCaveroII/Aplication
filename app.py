from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Book
from forms import LoginForm, BookForm, RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.is_admin == True:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('books'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books'))  

    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            is_admin=False  
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin == True:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('books'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  
            if user.is_admin == True:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('books'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/books')
@login_required
def books():
    if current_user.is_admin == True:
        return redirect(url_for('admin_dashboard'))
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin == True:
        flash('Access denied! Only admins can access this page.', 'danger')
        return redirect(url_for('books'))
    books = Book.query.all()
    return render_template('admin.html', books=books)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin == True:
        flash('Access denied')
        return redirect(url_for('login'))
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            year=form.year.data,
            rating=form.rating.data,
            pages=form.pages.data,
            price=form.price.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('books'))
    return render_template('create.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin == True:
        flash('Access denied')
        return redirect(url_for('login'))
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('books'))
    return render_template('edit.html', form=form, book=book)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if not current_user.is_admin == True:
        flash('Access denied')
        return redirect(url_for('login'))
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username='favio').first()
        if not admin_user:
            admin_user = User(
                username='favio',
                password=generate_password_hash('123456'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Administrador creado con éxito. Usuario: admin, Contraseña: adminpassword")
        else:
            print("El administrador ya existe.")
    app.run(debug=True)
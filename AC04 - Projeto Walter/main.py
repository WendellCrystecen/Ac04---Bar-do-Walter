from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Secret Key"
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/login'
app.config['SECRET_KEY'] = 'mudar123'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
#Classes

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Senha"})

    submit = SubmitField("Cadastrar")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash("Esse apelido já existe. Por favor, escolha outro.")
            raise ValidationError("Esse apelido já existe. Por favor, escolha outro.") 

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Senha"})

    submit = SubmitField("Entrar")


class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    pedidos = db.Column(db.Integer)
    itens_id = db.Column(db.String(100))
    valor = db.Column(db.Float)
    pag_dinheiro = db.Column(db.Integer, default = 0)
    pag_cartao = db.Column(db.Integer, default = 0)
 
 
    def __init__(self, nome, pedidos, itens_id, valor, pag_dinheiro, pag_cartao):
 
        self.nome = nome
        self.pedidos = pedidos
        self.itens_id = itens_id
        self.valor = valor
        self.pag_dinheiro = pag_dinheiro
        self.pag_cartao = pag_cartao

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('Index'))
            else:
                flash("Senha errada, por favor digite novamente!")
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/index')
@login_required
def Index():
    all_pedidos = Pedidos.query.order_by('pedidos').all()
 
    return render_template("index.html", pedidos = all_pedidos)
 
 
#Inserir dados
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        nome = request.form['nome']
        pedidos = request.form['pedidos']
        itens_id = request.form['itens_id'] 
        valor = request.form['valor']
        tipo_pag = request.form.get('tipo_pag')

        valor_cartao = '0'
        valor_dinheiro = '0'
        if tipo_pag != 'naopago':
            if tipo_pag == 'cartao':
                valor_cartao = '1'
            elif tipo_pag == 'dinheiro':
                valor_dinheiro = '1'



        my_data = Pedidos(nome, pedidos, itens_id, valor, valor_dinheiro, valor_cartao)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Pedido Inserido com Sucesso")
 
        return redirect(url_for('Index'))
 
 

@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Pedidos.query.get(request.form.get('id'))
 
        my_data.nome = request.form['nome']
        my_data.pedidos = request.form['pedidos']
        my_data.itens_id = request.form['itens_id']
        my_data.valor = request.form['valor']

        valor_cartao = '0'
        valor_dinheiro = '0'
        tipo_pag = request.form.get('tipo_pag')
        if tipo_pag != 'naopago':
            if tipo_pag == 'cartao':
                valor_cartao = '1'
            elif tipo_pag == 'dinheiro':
                valor_dinheiro = '1'


        my_data.pag_cartao = valor_cartao
        my_data.pag_dinheiro = valor_dinheiro
        db.session.commit()
        flash("Pedido Atualizado com Sucesso")
 
        return redirect(url_for('Index'))

 

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Pedidos.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Pedido Deletado com Sucesso")
 
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from models import Autor, Livro

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'  # para usar flash

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        total_autores = Autor.query.count()
        total_livros  = Livro.query.count()
        return render_template('index.html', total_autores=total_autores, total_livros=total_livros)

    # --------- CRUD AUTORES ----------
    @app.route('/autores')
    def listar_autores():
        autores = Autor.query.order_by(Autor.nome).all()
        return render_template('listar_autores.html', autores=autores)

    @app.route('/autor/novo', methods=['GET','POST'])
    def novo_autor():
        if request.method == 'POST':
            nome = request.form['nome'].strip()
            nacionalidade = request.form['nacionalidade'].strip()
            ano = request.form['ano'] or None
            if not nome:
                flash('Nome é obrigatório.')
                return redirect(url_for('novo_autor'))
            autor = Autor(nome=nome, nacionalidade=nacionalidade, ano_nascimento=ano)
            db.session.add(autor)
            db.session.commit()
            flash('Autor criado com sucesso!')
            return redirect(url_for('listar_autores'))
        return render_template('form_autor.html', autor=None)

    @app.route('/autor/editar/<int:id>', methods=['GET','POST'])
    def editar_autor(id):
        autor = Autor.query.get_or_404(id)
        if request.method == 'POST':
            autor.nome = request.form['nome'].strip()
            autor.nacionalidade = request.form['nacionalidade'].strip()
            autor.ano_nascimento = request.form['ano'] or None
            db.session.commit()
            flash('Autor atualizado!')
            return redirect(url_for('listar_autores'))
        return render_template('form_autor.html', autor=autor)

    @app.route('/autor/excluir/<int:id>', methods=['POST'])
    def excluir_autor(id):
        autor = Autor.query.get_or_404(id)
        db.session.delete(autor)
        db.session.commit()
        flash('Autor excluído!')
        return redirect(url_for('listar_autores'))

    # --------- CRUD LIVROS ----------
    @app.route('/livros')
    def listar_livros():
        livros = Livro.query.order_by(Livro.titulo).all()
        return render_template('listar_livros.html', livros=livros)

    @app.route('/livro/novo', methods=['GET','POST'])
    def novo_livro():
        autores = Autor.query.order_by(Autor.nome).all()
        if request.method == 'POST':
            titulo = request.form['titulo'].strip()
            ano = request.form['ano'] or None
            genero = request.form['genero'].strip()
            autor_id = int(request.form['autor_id'])
            if not titulo:
                flash('Título é obrigatório.')
                return redirect(url_for('novo_livro'))
            livro = Livro(titulo=titulo, ano_publicacao=ano, genero=genero, autor_id=autor_id)
            db.session.add(livro)
            db.session.commit()
            flash('Livro criado com sucesso!')
            return redirect(url_for('listar_livros'))
        return render_template('form_livro.html', livro=None, autores=autores)

    @app.route('/livro/editar/<int:id>', methods=['GET','POST'])
    def editar_livro(id):
        livro = Livro.query.get_or_404(id)
        autores = Autor.query.order_by(Autor.nome).all()
        if request.method == 'POST':
            livro.titulo = request.form['titulo'].strip()
            livro.ano_publicacao = request.form['ano'] or None
            livro.genero = request.form['genero'].strip()
            livro.autor_id = int(request.form['autor_id'])
            db.session.commit()
            flash('Livro atualizado!')
            return redirect(url_for('listar_livros'))
        return render_template('form_livro.html', livro=livro, autores=autores)

    @app.route('/livro/excluir/<int:id>', methods=['POST'])
    def excluir_livro(id):
        livro = Livro.query.get_or_404(id)
        db.session.delete(livro)
        db.session.commit()
        flash('Livro excluído!')
        return redirect(url_for('listar_livros'))


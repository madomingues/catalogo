#!/usr/bin/env python
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, BeerStyle, Cerveja, User
from flask import session as login_session
import random
import string
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///cervejas.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Rotas para login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                    digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['GET', 'POST'])

def gconnect():
    data = request.json
    token = data.get("id_token")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                              CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise ValueError('Wrong issuer')
        userid = idinfo['sub']
    except ValueError:
        pass

    user_id = session.query(User).filter_by(email=idinfo['email'])
    if user_id is None:
        createUser(login_session['email'])

    login_session['username'] = idinfo['name']
    login_session['email'] = idinfo['email']
    login_session['id'] = userid

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("Conectado como %s" % login_session['username'])
    return output

# Helpers para adicionar novos usuarios no banco de dados


def createUser(login_session):
    newUser = User(id=login_session['id'], username=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Rota para logout
@app.route('/gdisconnect', methods=['GET', 'POST'])

def gdisconnect():
    del login_session['username']
    del login_session['email']
    del login_session['id']
    return redirect(url_for('showStyles'))


# Rotas para o site e CRUD
@app.route('/')
@app.route('/1000cervejas')
def showStyles():
    estilos = session.query(BeerStyle).order_by(asc(BeerStyle.name))
    if 'username' not in login_session:
        return render_template('publicShowStyles.html', estilos=estilos)
    else:
        return render_template('showStyles.html', estilos=estilos)


@app.route('/1000cervejas/new', methods=['GET', 'POST'])
def newStyle():
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        if request.method == 'POST':
            novoEstilo = BeerStyle(name=request.form['name'],
                                   descricao=request.form['descricao'])
            session.add(novoEstilo)
            session.commit()
            flash('%s adicionado com sucesso' % novoEstilo.name)
            return redirect(url_for('showStyles'))
        else:
            return render_template('newStyle.html')


@app.route('/1000cervejas/<int:estilo_id>/edit', methods=['GET', 'POST'])
def editStyle(estilo_id):
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        editEstilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
        if editEstilo.user_id != login_session['user_id']:
            return """<script> function userError() {alert('Voce nao esta
            autorizado a editar esse estilo);}</script><body onload =
           'userError()'>"""
        if request.method == 'POST':
            if request.form['name']:
                editEstilo.name = request.form['name']
            if request.form['descricao']:
                editEstilo.descricao = request.form['descricao']
            session.add(editEstilo)
            session.commit()
            flash('%s editado com sucesso' % editEstilo.name)
            return redirect(url_for('beers', estilo_id=estilo_id))
        else:
            return render_template('editStyle.html', estilo_id=estilo_id,
                                   estilo=editEstilo)


@app.route('/1000cervejas/<int:estilo_id>/delete', methods=['GET', 'POST'])
def delStyle(estilo_id):
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        delEstilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
        if delEstilo.user_id != login_session['user_id']:
            return """<script> function userError() {alert('Voce nao esta
            autorizado a deletar esse estilo);}</script><body onload =
            'userError()'>"""
        if request.method == 'POST':
            session.delete(delEstilo)
            session.commit()
            flash('%s deletado com sucesso' % delEstilo.name)
            return redirect(url_for('showStyles'))
        else:
            return render_template('delStyle.html', estilo=delEstilo)


@app.route('/1000cervejas/<int:estilo_id>/beers')
def showBeers(estilo_id):
    estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
    cervejas = session.query(Cerveja).filter_by(estilo_id=estilo_id).all()
    if 'username' not in login_session:
        return render_template('publicShowBeers.html', cervejas=cervejas,
                               estilo=estilo, estilo_id=estilo_id)
    else:
        return render_template('showBeers.html', cervejas=cervejas,
                               estilo=estilo, estilo_id=estilo_id)


@app.route('/1000cervejas/<int:estilo_id>/beers/new', methods=['GET', 'POST'])
def newBeer(estilo_id):
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
        if request.method == 'POST':
            cerveja = Cerveja(name=request.form['name'],
                              descricao=request.form['descricao'],
                              preco=request.form['preco'],
                              familia=request.form['familia'],
                              temperatura=request.form['temperatura'],
                              cor=request.form['cor'],
                              tipo=request.form['tipo'],
                              estilo_id=estilo_id)
            session.add(cerveja)
            session.commit()
            flash('%s adicionado com sucesso' % cerveja.name)
            return redirect(url_for('showBeers', estilo_id=estilo_id))
        else:
            return render_template('newBeer.html', estilo_id=estilo_id,
                                   estilo=estilo)


@app.route('/1000cervejas/<int:estilo_id>/beers/<int:cerveja_id>/edit',
           methods=['GET', 'POST'])
def editBeer(estilo_id, cerveja_id):
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
        editedBeer = session.query(Cerveja).filter_by(id=cerveja_id).one()
        if editedBeer.user_id != login_session['user_id']:
            return """<script> function userError() {alert('Voce nao esta
            autorizado a editar essa cerveja);}</script><body onload =
            'userError()'>"""
        if request.method == 'POST':
            if request.form['name']:
                editedBeer.name = request.form['name']
            if request.form['descricao']:
                editedBeer.descricao = request.form['descricao']
            if request.form['preco']:
                editedBeer.preco = request.form['preco']
            if request.form['familia']:
                editedBeer.familia = request.form['familia']
            if request.form['tipo']:
                editedBeer.tipo = request.form['tipo']
            if request.form['temperatura']:
                editedBeer.temperatura = request.form['temperatura']
            if request.form['cor']:
                editedBeer.cor = request.form['cor']
            session.add(editedBeer)
            session.commit()
            flash('%s editado com sucesso' % editedBeer.name)
            return redirect(url_for('showBeers', estilo_id=estilo_id))
        else:
            return render_template('editBeer.html', cerveja=editedBeer,
                                   estilo=estilo, estilo_id=estilo_id)


@app.route('/1000cervejas/<int:estilo_id>/beers/<int:cerveja_id>/delete',
           methods=['GET', 'POST'])
def deleteBeer(estilo_id, cerveja_id):
    if 'username' not in login_session:
        return render_template('login.html')
    else:
        estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
        delBeer = session.query(Cerveja).filter_by(id=cerveja_id).one()
        if delBeer.user_id != login_session['user_id']:
            return """<script> function userError() {alert('Voce nao esta
            autorizado a editar esse estilo);}</script><body onload =
            'userError()'>"""
        if request.method == 'POST':
            session.delete(delBeer)
            session.commit()
            flash('%s deletado com sucesso' % delBeer.name)
            return redirect(url_for('showBeers', estilo_id=estilo_id))
        else:
            return render_template('deleteBeer.html', cerveja=delBeer,
                                   estilo_id=estilo_id, estilo=estilo)


@app.route('/1000cervejas/<int:estilo_id>/beers/<int:cerveja_id>/descricao')
def descrBeer(estilo_id, cerveja_id):
    estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
    beerDescr = session.query(Cerveja).filter_by(id=cerveja_id).one()
    if 'username' not in login_session:
        return render_template('publicDescrBeer.html', estilo=estilo,
                               cerveja=beerDescr)
    else:
        return render_template('descrBeer.html', estilo=estilo,
                               cerveja=beerDescr)


#Rotas endpoint JSON
@app.route('/1000cervejas/JSON')
def jsonStyles():
    estilos = session.query(BeerStyle)
    return jsonify(estilos = [e.serialize for e in estilos])


@app.route('/1000cervejas/<int:estilo_id>/beers/JSON')
def jsonBeers(estilo_id):
    estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
    cervejas = session.query(Cerveja).filter_by(estilo_id=estilo_id).all()
    return jsonify(cervejas = [c.serialize for c in cervejas])


@app.route('/1000cervejas/<int:estilo_id>/beers/<int:cerveja_id>/JSON')
def jsonDescrBeer(estilo_id,cerveja_id):
    estilo = session.query(BeerStyle).filter_by(id=estilo_id).one()
    beerDescr = session.query(Cerveja).filter_by(id=cerveja_id).one()
    return jsonify(beerDescr = [beerDescr.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

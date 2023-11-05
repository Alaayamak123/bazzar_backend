from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, ForeignKey, or_
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class Catalog(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    count: Mapped[int] = mapped_column(Integer, default=1)
    catalog_id: Mapped[int] = mapped_column(ForeignKey(Catalog.id))
    catalog: Mapped[Catalog] = relationship(Catalog)


with app.app_context():
    db.create_all()

@app.get('/catalogs')
def get_all_catalogs():
    try:
        catalogs = db.session.execute(db.select(Catalog).order_by(Catalog.id)).scalars()
        catalogs_list = [{ 'id': catalog.id,'name': catalog.name } for catalog in catalogs]
        return jsonify({
            'catalogs': catalogs_list
        })

    except:
        json_response = jsonify({
            'error': 'something went wrong'
        })
        return make_response(json_response,500)

@app.post('/catalogs')
def create_catalog():
    try:
        name = request.form['name']
    except:
        json_response = jsonify({
            'error': 'no name was provided'
        })
        return make_response(json_response, 400)

    catalog = Catalog(
        name=name
    )

    db.session.add(catalog)
    db.session.commit()

    return jsonify({
        'success': True,
        'catalog': catalog.name,
        'catalog_id': catalog.id,
    })


@app.get('/books')
def get_all_books():
    try:
        books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
        books_list = [{'id': book.id, 'name': book.name} for book in books]
        return jsonify({
            'books': books_list
        })

    except:
        json_response = jsonify({
            'error': 'something went wrong'
        })
        return make_response(json_response, 500)



@app.post('/books')
def create_book():
    try:
        name = request.form['name']
        catalog = request.form['catalog']
        count = int(request.form['count'])
    except Exception as exc:
        json_response = jsonify({
            'error': 'no name,catalog or count was provided',
        })
        return make_response(json_response, 400)

    book = Book(
        name=name,
        catalog_id=catalog,
        count=count
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({
        'success': True,
        'book': book.name,
        'book_id': book.id,
    })

@app.get('/books/search/<int:id>')
def search_books(id):
    books = db.session.execute(db.select(Book).filter_by(catalog_id=id)).scalars()
    books_list = [{'name': book.name,'count': book.count, 'id': book.id} for book in books]
    return jsonify({
        'books': books_list
    })

@app.get('/books/find')
def get_book_by_name():
    search_string = request.args.get('name','')
    books = db.session.query(Book).filter(or_(Book.name.like(f"%{search_string}%"))).all()

    book_info = [{
        'id': book.id,
        'name': book.name,
        'count': book.count
    } for book in books]
    return jsonify({
        'books': book_info
    })


@app.get('/books/<int:id>')
def get_book(id):
    try:
        book = db.session.execute(db.select(Book).filter_by(id=id)).scalar_one()
        book_info = dict({
            'id': book.id,
            'name': book.name,
            'count': book.count
        })
        return jsonify({
            'books': book_info
        })
    except Exception as exc:
        json_response = jsonify({
            'error': exc.__str__()
        })

        return make_response(json_response,404)
app.run('0.0.0.0', port=4000, debug=True)

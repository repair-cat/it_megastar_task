from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import sys

# конфигурация БД
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/postgres'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# модели
class Writer(db.Model):
    __tablename__ = 'writers'                                               
    id = db.Column(db.Integer(), primary_key=True)                          
    name = db.Column(db.String(255), nullable=False)   

    books = db.relationship("Book", back_populates="writer")                   

    def __repl__(self):
        return '<{}:{}>'.format(id, self.name)


class Book(db.Model):
    __tablename__ = 'books'                              
    id = db.Column(db.Integer(), primary_key=True)                                         
    name = db.Column(db.String(255), nullable=False)                                        

    author_id = db.Column(db.Integer(), db.ForeignKey('writers.id'), nullable=False)
    writer = db.relationship("Writer", back_populates="books")

    def __repl__(self):
        return '<{}:{}>'.format(id, self.name)


# схемы
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'name')

class WriterSchema(ma.Schema):
    class Meta:
        model = Writer
        fields = ('id', 'name', 'books')

    books = fields.Nested(BookSchema, many=True)


writer_schema = WriterSchema()
book_schema = BookSchema()

db.create_all()

# заполняем таблицу данными
lev = Writer(name="Лев Толстой")
gog = Writer(name="Николай Гоголь")
kar = Writer(name="Карлос Кастанеда")
jul = Writer(name="Жюль Верн")
db.session.add_all([lev, gog, kar, jul])

lev_book_1 = Book(name="Война и мир", writer=lev)
lev_book_2 = Book(name="Воскресение", writer=lev)
gog_book_1 = Book(name="ВИЙ", writer=gog)
gog_book_2 = Book(name="Мертвые души", writer=gog)
kar_book_1 = Book(name="Путешествие в Икстлан", writer=kar)
kar_book_2 = Book(name="Сказки о силе", writer=kar)
jul_book_1 = Book(name="20000 лье под водой", writer=jul)
jul_book_2 = Book(name="Капитан Немо", writer=jul)

db.session.add_all([lev_book_1, lev_book_2, gog_book_1, gog_book_2, 
                    kar_book_1, kar_book_2, jul_book_1, jul_book_2])
db.session.commit()


# вьюшка
@app.route('/writers/<int:writer_id>/', methods=['GET'])
def get_writer(writer_id):
    author = Writer.query.get(writer_id)
    return writer_schema.jsonify(author)


# Run server
if __name__ == "__main__":
    if sys.argv[1] == 'init':
        app.run(debug = True)
from mongoengine import connect, Document
from mongoengine.fields import Document, StringField
import requests, gzip, json

connect('mongoengine_db', host='mongo')

class Book(Document):
    title=StringField(max_lenght=50)
    author=StringField(max_lenght=50)
    genre=StringField(max_lenght=50)
    description=StringField(max_lenght=50)
    isbn=StringField(max_lenght=50)
    image=StringField(max_lenght=50)
    published=StringField(max_lenght=50)
    publisher=StringField(max_lenght=50)


def backup():
    # nombre del archivo de backup
    backup_filepath = "backup.gz"

    # realizar el backup
    with gzip.open(backup_filepath, "wb") as f:
        # obtener todos los documentos de la colección y escribirlos en el archivo gzip
        for document in Book.objects:
            # convertir el documento a formato JSON y escribirlo en el archivo gzip
            json_document = json.loads(document.to_json())
            json_document["_id"] = str(document.id) # convertir ObjectId a cadena de texto
            f.write(json.dumps(json_document).encode("utf-8"))
            f.write(b"\n")


def restore():
    backup_filepath = 'backup.gz'

    with gzip.open(backup_filepath, "rb") as f:
        for line in f:
            # decodificar la línea del archivo y convertirla a objeto JSON
            json_line = json.loads(line.decode("utf-8"))
            # convertir la cadena de texto del _id a un objeto ObjectId
            json_line.pop("_id")
            # crear un nuevo documento de la colección y asignar los campos
            document = Book(**json_line)
            # guardar el documento en la base de datos
            document.save()


def poblate():
    r = requests.get('https://fakerapi.it/api/v1/books?_quantity=5')

    for book in r.json()['data']:
        insert_book = Book(
                title=book['title'],
                author=book['author'],
                genre=book['genre'],
                description=book['description'],
                isbn=book['isbn'],
                image=book['image'],
                published=book['published'],
                publisher=book['publisher']
            )
        insert_book.save()

if __name__ == "__main__":
    poblate()
    backup()
    #restore()

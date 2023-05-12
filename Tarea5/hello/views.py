from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from . import populate as p
from .populate import Book
from .models import FormularioLibro

import logging
logger = logging.getLogger(__name__)


def home(request):
    word = "hola"
    if request.method=="POST":
        word = request.POST['word']
    context = {'foo': 'Book Store!', 'word': word}
    return render(request, 'home.html', context)

def poblar(request):
    p.poblate()
    return redirect('books')

def get_all(request):
    try:
        books = p.get_all()
    except Exception:
        # equivalent to logger.error(msg, exc_info=True)
        logger.exception("Algo salio mal al buscar en la BD")  
    
    logger.info("Se han buscado todos los libros en la BD")
    context = {'books': books}
    return render(request, 'list.html', context)

def delete(request, id):
    
    if request.method=="POST":
        p.delete(id)
        logger.info("Borrado el libro " + id)
        return redirect('books')


def search(request):
    word = " "
    if request.method=="POST":
        word = request.POST['word']
        logger.info("Buscando palabra %s", word)

    # rest of your view code here
    books = p.search_by_title(word)
    context = {'books': books}
    return render(request, 'list.html', context)


def busqueda_parcial(request):
    valor = request.GET.get('valor', '')
    logger.debug(f'buscando {valor}')
    books = p.search_by_title(valor)
    datos = []
    for b in books:
        datos.append(
            {
            'title': b.title,
            'author': b.author
            }
        )
    logger.debug(list(books))
    return JsonResponse({'ok': True, 'datos': datos})


def create(request):
    formulario = FormularioLibro()
    if request.method == 'POST':
        formulario = FormularioLibro(request.POST)
        if formulario.is_valid():
            logger.debug(formulario.cleaned_data)
            p.create_book_form(formulario.cleaned_data)
            return redirect('books')
    context = {
        'formulario': formulario
    }

    return render(request, 'create.html', context)

def details(request, id):
    book = p.get(id)
    context = {
        'book': book
    }
    return render(request, 'details.html', context)

def update(request, id):
    book = p.get(id)
    if request.method == "POST":
        title = book.title
        author = book.author
        genre = book.genre
        description = book.description
        isbn = book.isbn
        publisher = book.publisher
        published = book.published

        # creamos el formulario y le pasamos los valores del libro usando el método initial
        formulario = FormularioLibro(initial={
            'title': title,
            'author': author,
            'genre': genre,
            'description': description,
            'isbn': isbn,
            'publisher': publisher,
            'published': published,
        })
    
    return render(request, 'update.html', {'formulario': formulario, "id":id})

def update_data(request, id):
    if request.method == 'POST':
        formulario = FormularioLibro(request.POST)
        if formulario.is_valid():
            logger.debug(formulario.cleaned_data)
            p.update_book_form(formulario.cleaned_data, id)
            return redirect('/get/'+id)

    return redirect('books')


from flask import Flask, jsonify, request, Response

from BookModel import *
from settings import *
import json

@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

# POST /books
# {
#   'name': 'F',
#   'price': 6.99,
#   'isbn': 0123456789
# }
# We need to filter our data and make it safe.
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books', methods=['POST'])
def add_book():
#    return jsonify(request.get_json()) 
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed",
            "helpString": "Data passed in similar to this {'name': 'bookname'}"
        }
        response = Response(invalidBookObjectErrorMsg, status=400, mimetype='application/json')
        return response


@app.route ('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# PUT
@app.route ('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

@app.route ('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number provided was not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype="application/json")
    return response

app.run(port = 5000)

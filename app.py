from flask import Flask, jsonify, request, Response
app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        "isbn": 9780394800165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]

@app.route('/books')
def get_books():
    return jsonify({'books': books})

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
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

# PUT
@app.route ('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

@app.route ('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if(book["isbn"] == isbn):
            books.pop(i)
            response = Response("", status=204)
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number provided was not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype="application/json")
    return response

app.run(port = 5000)

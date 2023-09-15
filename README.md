# Library Management System
 ##### (A Django REST API Project)

### Registration: 
Any user can register providing an email ID and password making a  POST request to the following endpoint: http://localhost:8000/users/users/

### Log-in: 
A registered user can login into the system providing those email ID and password using the POST method in the endpoint: http://localhost:8000/users/login/  where an access token will be generated. 

In order to access the API, this access token has to be used with ‘Token’ as prefix in the 
Authorization header. For example: 
Authorization: Token 024a1be3f6738543d6b1e25b64c76c091c9ec11f

### Add book: 
A book can be added making a POST request to the endpoint: http://localhost:8000/books/books/

### View books: 
The list of books can be viewed using GET method in the same endpoint: http://localhost:8000/books/books/

### Update book: 
A specific book can be viewed or modified using the GET or PUT/PATCH method in the endpoint: http://localhost:8000/books/books/<id>/

### Borrow book:  
Books can be borrowed by a user by making a POST request to the http://localhost:8000/books/borrowings/  endpoint. 

### Return book: 
Books can be returned using the endpoint http://localhost:8000/books/borrowings/<borrowing_id>/return_book/  

### Reserve book: 
Making a POST request, the endpoint http://localhost:8000/books/books/<book_id>/reserve/  can be used to reserve a book.

### Add to wishlist: 
Books can also be added to the wishlist of any user by making a POST request to the endpoint http://localhost:8000/books/wishlist/  so that they can view them later making a GET request.

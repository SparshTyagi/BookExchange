// Get the book list element
const bookList = document.getElementById('book-list');

// Get the user list element
const userList = document.getElementById('user-list');

// Fetch books from the API
fetch('/books')
    .then(response => response.json())
    .then(data => {
        // Populate the book list
        data.forEach(book => {
            const bookListItem = document.createElement('li');
            bookListItem.textContent = `${book.title} by ${book.author}`;
            bookList.appendChild(bookListItem);
        });
    })
    .catch(error => console.error(error));

// Fetch users from the API
fetch('/users')
    .then(response => response.json())
    .then(data => {
        // Populate the user list
        data.forEach(user => {
            const userListItem = document.createElement('li');
            userListItem.textContent = user.username;
            userList.appendChild(userListItem);
        });
    })
    .catch(error => console.error(error));
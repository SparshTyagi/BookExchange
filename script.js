// fetch user profiles
fetch('/user_profiles')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// fetch books
fetch('/books')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// fetch exchange requests
fetch('/exchange_requests')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// fetch discussion posts
fetch('/discussion_posts')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
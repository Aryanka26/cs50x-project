# CS50X Final Project: 📚 BookNest

Demo video link :   

**BookNest** is a full-stack web application that allows users to discover books, write reviews, track their reading activity, and build a personalized reading profile.

This project was created as the **final project for CS50x**, showcasing backend development, database design, authentication, external API usage, and frontend UI/UX improvements.

---

## Features

- **User Authentication**
  - Register, log in, and log out
  - Secure password hashing
  - Session-based authentication

- **Book Search**
  - Search books by title, author, or ISBN
  - Dynamic book cover images

- **Book Details**
  - Dedicated page for each book
  - Additional data fetched from Open Library API

- **Reviews & Ratings**
  - Users can submit one review per book
  - Ratings from 1–5 stars
  - View reviews by other users

- **User Profile**
  - Upload and update profile avatar
  - View personal review history
  - See total reviews and average rating given

- **Dark Mode**
  - Toggle between light and dark themes
  - Clean and modern interface

---

## Technologies Used

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Jinja2  
- **Database:** SQLite  
- **Authentication:** Flask-Session, Werkzeug  
- **External API:** Open Library API  
- **Version Control:** Git  

---

## File Descriptions

This section briefly explains the purpose of each major file and directory used in the project.

- **app.py**  
  The main Flask application file.  
  Handles routing, user authentication, database queries, and core application logic.

- **helpers.py**  
  Contains helper functions used across the application, including login protection, error handling, and external API lookups.

- **schema.sql**  
  Defines the database schema, including tables for users, books, reviews, and searches.

- **books.db**  
  SQLite database storing all application data such as users, books, reviews, and search history.

- **templates/**  
  Contains all HTML templates rendered using Jinja2.
  - **layout.html** – Base layout with navbar and theme toggle
  - **login.html** – Login page
  - **register.html** – User registration page
  - **index.html** – User dashboard (home page)
  - **search.html** – Book search page
  - **book.html** – Individual book detail and review page
  - **profile.html** – User profile page with avatar and review history
  - **apology.html** – Error page for displaying user-friendly messages

- **static/**  
  Contains static assets such as stylesheets and images.
  - **styles.css** – Main stylesheet for layout, dark mode, and UI styling
  - **avatars/** – Stores uploaded user profile avatars
  - **images/** – Stores images used for UI aesthetics (e.g., auth page visuals)

- **README.md**  
  Documentation describing the project, features, setup instructions, and design decisions.

- **requirements.txt**
  Contains names of all the libraries needed to be installed.
---

## How to Run the Application

1. **Install required dependencies**

   Run this in the terminal:
   ```bash
   pip install -r requirements.txt
    ```
2. **Ensure the database file is present**

   This project includes a pre-populated `books.db` file containing book data. No additional database setup is required.

3. **Run the Flask application**

   ```bash
   flask run
    ```   
4. **Open the application in your browser**

    Visit Port 5000 or click on "Open in Browser" on the notification which pops once you run the application.

5. **Using the application**

    - Register a new account.
    - Log in with your credentials.
    - Search for books by title, author, or ISBN.
    - View book details and submit reviews.
    - Visit your profile to view your reviewed books and upload an avatar.
    - Toggle between light and dark mode.

---

## Acknowledgements

- CS50 Staff and Community
- Open Library API
- Flask Documentation
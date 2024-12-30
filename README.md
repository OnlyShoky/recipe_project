# Recipe API and Web Application

Welcome to the **Recipe API and Web Application**! This project is designed to help users explore, manage, and share recipes through a beautifully crafted frontend and a robust backend API.

---

## 🌟 Features

- **Frontend**: An elegant home page showcasing popular recipes and detailed recipe pages.
- **Backend API**: A fully functional API to manage recipes, search, and retrieve details in JSON format.
- **Extensibility**: Modular architecture with separate apps for recipes, API, and frontend.

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/recipe-project.git
cd recipe-project
```

### 2. Install Dependencies
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Populate the Database (Optional)
Add some sample recipes to the database:
```bash
python manage.py loaddata sample_recipes.json
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Visit the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🛠️ Project Structure

```
recipe_project/
    manage.py               # Django management script
    recipe_project/         # Project settings and configurations
        settings.py         # Main settings file
        urls.py             # URL routing
    recipes/                # App for recipe-related functionality
        models.py           # Database models
        serializers.py      # API serializers
        views.py            # Logic for displaying recipes
    api/                    # App for API-related functionality
        views.py            # API views
        urls.py             # API routes
    frontend/               # App for frontend templates and views
        templates/          # HTML files
        static/             # Static files (CSS, JS, Images)
    requirements.txt        # List of dependencies
```

---

## 🌐 API Endpoints

### Public Endpoints
- **Get All Recipes**: `GET /api/recipes/`
- **Get Recipe Details**: `GET /api/recipes/<id>/`
- **Search Recipes**: `GET /api/json/v1/1/search.php?s=<query>`

---

## 📸 Screenshots

**Home Page:**
> Display a curated list of recipes.

**Recipe Detail Page:**
> Show detailed information about a specific recipe.

---

## 🛡️ Future Updates

- User authentication and favorites.
- Advanced search and filtering options.
- Integration with external recipe APIs.
- Enhanced styling for the frontend.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify it as you wish.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

---

## 💌 Contact

For any inquiries, feel free to contact us:

- **Email**: mohamed.elmoag@gmail.com
- **GitHub**: [OnlyShoky](https://github.com/onlyshoky)

---

Thank you for checking out this project! 😊


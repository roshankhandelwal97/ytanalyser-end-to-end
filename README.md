# YTVideoAnalyser

This project is an end-to-end solution for analyzing YouTube videos. It includes both a frontend and a backend, designed to interact with a Python model using LLM (Large Language Models) and RAG (Retrieval-Augmented Generation) techniques. The backend is built with Django, and the frontend is created using React.js.

## Project Structure

The project is divided into two main parts:

- `backend`: Contains the Django backend code.
- `frontend`: Contains the React.js frontend code.

### Backend Structure

The backend is a Django application responsible for handling API requests and interacting with the Python model and Pinecone for saving vector embeddings.

### Backend

```
backend/
├── manage.py
├── backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── migrations/
│       └── __init__.py
```

### Frontend Structure

The frontend is a React.js application responsible for the user interface, interacting with the backend via API calls.

```
frontend/
├── public/
│ ├── index.html
│ └── ...
├── src/
│ ├── App.js
│ ├── index.js
│ ├── components/
│ │ ├── Header.js
│ │ ├── Chat.js
│ │ └── YoutubeForm.js
│ ├── services/
│ │ └── api.js
│ └── styles/
│ └── App.css

```


## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js
- npm or yarn
- Django
- React.js

### Backend Installation

1. Navigate to the `backend` directory:

   ```bash
   cd backend
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations and start the Django server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Installation

1. Navigate to the `frontend` directory:

   ```bash
   cd frontend
   ```

2. Install the required npm packages:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

## Usage

1. Ensure both the backend and frontend servers are running.
2. Open your browser and navigate to `http://localhost:3000` to access the frontend interface.
3. Use the interface to interact with the YouTube analysis functionalities.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.


## Contact

For any inquiries or issues, please contact [Roshan Khandelwal](https://github.com/roshankhandelwal97).

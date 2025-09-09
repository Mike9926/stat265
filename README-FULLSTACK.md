# Project layout (frontend/backend)

- frontend/  -> Vite + React app (UI)
- backend/   -> Django project (APIs)

Backend run (Python + venv):

cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Frontend run (node):

cd frontend
npm install
npm run dev

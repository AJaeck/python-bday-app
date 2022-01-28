# Anna's Birthday App

## First Steps for Development and Deployment

Source: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-app-using-gunicorn-to-app-platform

### Production

1. Create virtual env with:
   "source ~/.venvs/flask/Scripts/activate"

2. If Development Env necessary, set env variables with:
   export FLASK_ENV=development
   export FLASK_APP=app.py

3. Make sure to use Git Dev branch for development

### Deployment

3. For deployment, merge Dev branch with Main branch which will trigger Digital Ocean App Deployment

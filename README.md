# anna-bday-app

## First Steps for Development and Deployment

Source: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-app-using-gunicorn-to-app-platform

1. Create virtual env with:
   "source ~/.venvs/flask/Scripts/activate"

2. If Development Env necessary, set env variables with:
   "export FLASK_ENV=development"
   "export FLASK_APP=app.py"

3. If Deploy necessary, push to heroku with:
   > Commit repo changes
   > Login to Heroku: "heroku login"
   > Push to Heroku: "git push heroku master"

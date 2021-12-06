REM login to your Heroku account
heroku login

REM change dash-app to a unique name
heroku create multipage-erlt-dashboard-4
REM change remote
heroku git:remote -a multipage-erlt-dashboard-4
git remote -v

REM deploy to Heroku
git push heroku master

REM run the app with a 1 heroku "dyno"
heroku ps:scale web=1


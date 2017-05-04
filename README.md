# Django Rest Framework demo

## Comment API
This project includes an REST api app which has a get endpoint which returns all comments for a page by content url, such as '/comment-api/<content_url>', and a post endpoint, at '/comment-api', for posting new comments for a content url.

An example get request to retrieve all comments on a page called "pop-quiz" could be done with curl as follows:
```
curl http://<base_url>/comment-api/pop-quiz"
```

An example post request to create a comment on the same page could be done like this:
```
curl -H "Content-Type: application/json" -X POST -d {"username":"test_user","text":"test comment","content_url":"pop-quiz","ip":"1.160.10.240"} http://<base_url>/comment-api
```
## Throttling
It also includes a custom throttling implementation that locks out users for posting duplicate comments within a set timeframe from their posting for an adjustable amount of time, locks out users for a separately adjustable amount of time for posting above some number of comments within an independent timeframe, and rate limits get requests.

- Throttle settings are stored in the database so that they can be adjusted by an admin.

- If you want to look at the admin there is an admin account of {demo_admin: demo_password}.

- If necessary, you can set initial setting values by loading the included fixture like so:
```
python manage.py loaddata initial_data.json
```

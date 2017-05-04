# Django Rest Framework demo

## Comment API
This project includes an REST api app which has a get endpoint which returns all comments for a page by content url, such as '/comment-api/<content_url>', and a post endpoint, at '/comment-api', for posting new comments for a content url.

## Throttling
It also includes a custom throttling implementation that locks out users for posting duplicate comments within a set timeframe from their posting for an adjustable amount of time, locks out users for a separately adjustable amount of time for posting above an some number of comments within an independent timeframe, and rate limits get requests.

-Throttle settings are stored in the database so that they can be adjusted by an admin.

-If you want to look at the admin there is an admin account of {demo_admin: demo_password}.

-If necessary, you can set initial setting values by loading the included fixture like so:
```
python manage.py loaddata initial_data.json
```

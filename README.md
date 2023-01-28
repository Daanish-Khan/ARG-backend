# ARG-backend
RESTful API for interacting with the ARG frontend.

## Run Locally
`python backend.py`

## Run on server
Make sure we have latest ver of code. Usually GitHub actions will do this for you but just incase:

`sudo systemctl resart arg-backend`

## Generate Requirements
Run `python -m pipreqs.pipreqs`

### Troubleshooting

Check if service is up using `sudo systemctl status arg-backend.service`. If shows that an error occured, navidate to backend and run `gunicorn --bind 0.0.0.0:5000 wsgi:app`
to get detailed error logs. 

CLIENT_ID = "91SpjoSbNCW7yA"
CLIENT_SECRET = "N8Oy3FIqw62KpbM_5vCJJ5GcbtxQEg"
REDIRECT_URI = "http://127.0.0.1:8080/reddit_callback"

from flask import Flask
app = Flask(__name__)
@app.route('/')
def homepage():
	text = '<a href="%s">Authenticate with reddit</a>'
	return text % make_authorization_url()

def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
	params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "temporary",
			  "scope": "identity read"}
	import urllib
	url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
	return url

from flask import abort, request
@app.route('/reddit_callback')
def reddit_callback():
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = request.args.get('state', '')
	if not is_valid_state(state):
		# Uh-oh, this request wasn't started by us!
		abort(403)
	code = request.args.get('code')
	# We'll change this next line in just a moment
	access_token = get_token(code)
	#print("Your reddit username is: %s" % get_username(access_token))
	return get_wsb_hot(access_token)
	#return "Your reddit username is: %s" % get_username(access_token)

def get_username(access_token):
	headers = {"Authorization": "bearer " + access_token}
	response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
	me_json = response.json()
	#print("uwu %s\n",response)
	return me_json['name']

def get_wsb_hot(access_token):
	headers = {"Authorization": "bearer " + access_token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
	response = requests.get("https://oauth.reddit.com/r/wallstreetbets/hot?limit=1", headers=headers)
	#print("uwu",response)
	me_json = response.json()
	final1 = me_json["data"]
	final2 = final1["children"]
	final3 = final2[0]
	final4 = final3["data"]
	final = final4["title"]
	return "Wall Street Bets Hot: %s" % final

import requests
import requests.auth
def get_token(code):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	response = requests.post("https://ssl.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data,
							 headers=headers)
	token_json = response.json()
	return token_json["access_token"]

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True


if __name__ == '__main__':
	app.run(debug=True, port=8080)
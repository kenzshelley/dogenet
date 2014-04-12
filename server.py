import os
import re
import requests
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, abort, redirect, url_for, request, make_response, Response, stream_with_context, send_file
import pyjade
from StringIO import StringIO

app = Flask(__name__)
# use the jade template engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

def get_route(path):
  host = request.headers.get("Host")
  if host == "127.0.0.1:3000":
    return (path.split('/')[0], ''.join(path.split('/')[1:]))
  return (host, path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  (host, path) = get_route(path)
  print 'You want path: http://%s/%s' % (host, path)
  print request.method
  #if re.match(r'^.*\.(jpeg|jpg|png|gif|bmp)$', path, re.IGNORECASE):
  if host == "nytimes.com":
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
  if request.method == "POST":
    r.requests.post("http://%s/%s" % (host, path), params=dict(request.form))
  else:
    r = requests.get("http://%s/%s" % (host, path))
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



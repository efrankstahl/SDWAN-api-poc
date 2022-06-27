# this will send the script to my api server, 'test-server.py'

import json 
from flask import Flask, request, abort
from pathlib import Path
# this is document.py on his --the document engine. 
from document import Document

app = Flask(__name__)
 
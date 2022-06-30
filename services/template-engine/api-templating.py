import json 
from flask import Flask, request 
from pathlib import Path 
from template_engine import create_doc_outline

app = Flask(__name__)
 
sdwan_template = Path("./templates/doc_v3.jinja2")

# 6/28: this can go.  
loaded_data = {}
parsed_data = {}
doc_outline = []
results = {}
 

@app.route('/')
def homepage():
    return "Template engine homepage."

@app.route('/from-preprocessor', methods=['GET','POST'])
# 6/28:  let's just see if it can receive the post request before we do anything fancy. 
def frompreprocessor():
    if request.method == 'POST':
        raw_incoming = request.form['raw_data']
        # 6/30: in the real one, it's going to take a dictionary that
        # contains entries for product, gdoc_type etc 
        # 6/30: but i don't have how that info will be stored yet.

        # 6/30: it returns a string that is styled like a list, but not 
        # and actual list yet. 
        doc_outline = create_doc_outline(raw_incoming, sdwan_template.read_file())
        
        # FINAL RESULT IS A LIST. 
        print(type(doc_outline))
        # 6/30: make a post request to doc engine?
        return doc_outline
    
        # unpack data from the POST request
        # (eventually) check that it's SDWAN
        # run create_doc_outline on it 
        # 6/29:  !! Make sure your create doc outline functions like
        #        it does in testprocessing.py!
    if request.method == 'GET':
        return 'Placeholder (this will be data the preprocessor sends)'
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)       
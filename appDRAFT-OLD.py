import json 
from flask import Flask, request 
from pathlib import Path
from preprocessorSDWAN import load_data, parse_data
from template_engine import create_doc_outline

app = Flask(__name__)

# Sun 6/26: Will import from the GUI's API call in the final version
# but I'm not sure how to set that up yet. 
yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-tire-kicking-2-poc\raw_data.yaml")
# Sun 6/26: doublecheck that clarifying the path as /templates is neccesary/functional  
sdwan_template = Path("./templates/doc_v2.jinja2")

loaded_data = {}
parsed_data = {}
doc_outline = []

# from an earlier build
to_temp_dict = {}

@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine -currently nonfunctional."
 
@app.route('/from-gui', methods=['GET','POST'])
def fromgui():
    if request.method == 'POST':
        # PLACEHOLDER.  In final version it loads from GUI/ API. 
        loaded_data['raw_data'] = load_data(yaml_raw)
        # Below data will be supplied by the API/GUI, but how?
        # New fields in the YAML file? Or is yaml file just part of json/a dict?
        loaded_data['product'] = "sdwan"
        loaded_data['replacement_values'] = "placeholder"
        loaded_data['gdoc_type'] = True

        parsed_data = parse_data(loaded_data)
        # will eventually run an error check. 
        # Anton 6/28:  Return parsed data, not placeholder
        # Anton: "And that data is what's use din the next method   "
        return "Placeholder."

# IMPORTANT: Is it the template engine that does a GET to access the parsed data? 
# It will return the document outline.
    if request.method == 'GET':
        if not parsed_data:
            return "Error: No data to process."
        else:
            # There's a more elegant way to write this bit, but that's for a later version.
            if parsed_data['product'] == 'sdwan':
                doc_outline = create_doc_outline(parsed_data, sdwan_template)
            elif parsed_data['product'] == 'panos':
                print("Then we'll load a different template string.")
            else: 
                print("Error: Bad product name.")
            return doc_outline

 

# OLD.

@app.route('/to-template', methods=['GET','POST'])
def totemplate():
    # Sun 6/26: eventually we'll need to check what kind of system it's from. 
    if request.method =='POST':
        # 6/24:  how do I get the WHOLE UGLY DICTIONARY TO SEND? 
        to_temp_dict['raw_data'] = request.form['raw_data']
        to_temp_dict['product'] = request.form['product']
        to_temp_dict['replacement_values'] = request.form['replacement_values']
        to_temp_dict['gdoc_type'] = request.form['gdoc_type']

        # Sun 6/26: adding processing for sent data
        # Eventually, there will be separate template_paths depending on the product.
        doc_outline = create_doc_outline(to_temp_dict, sdwan_template)
        # "return" should eventually return a success/error message. 
        return to_temp_dict
    if request.method =='GET':
        if not to_temp_dict:
            return "Error: Requested information from [ip_placeholder]/to-template is unavailable."
        else:
            # 6/26:  Now returns the processed to_temp_dict, not to_temp_dict itself
            return doc_outline
 
if __name__ == '__main__':
    app.run()
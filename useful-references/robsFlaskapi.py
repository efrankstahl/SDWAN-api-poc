import json 
from flask import Flask, request, abort
from pathlib import Path
# this is document.py on his --the document engine. 
from document import Document

app = Flask(__name__)
 
@app.route('/doc-engine', methods=['GET', 'POST'])
def generate_test():
    if request.method == 'POST':
        # Storing API paramaters locally.
        doc_outline = request.form['doc_outline']
        doc_title = request.form['doc_name']
        # replacement_values = request.form['replacement_values']
        gdoc_selected = request.form['gdoc_selected']

        # only this parameter is optional 
        # Eileen:  Oooh, an extra get on the end of the request.form method?
        init_id =request.form.get('init_id')

        # initial parameter pruning 
        # Eileen: whatever that means! I only know how to prune trunks!
        if gdoc_selected != 'True' and gdoc_selected != 'False':
            # oh it's some kinda errorr check 
            abort(400)
        
        # Eileen: Yeah this probably isn't gonna work without document.py
        # !!!!!!! HOWEVER, IT IS IMPORTANT!!!!!!!!!!!!!!!!!!
        # Read the JSON document outline as a string and convert it into a python dict
        doc_outline_dict = json.loads(Path(doc_outline).read_text())

        # Eileen: more stuff that definitely wont work
        if gdoc_selected == 'True':
            # Instantiate the Document object
            # Eileen: WE DONT HAVE THE DOCUMENT FILE CONTAINING DOCUMENT, so this won't work 
            doc_obj = Document(doc_name=doc_title, doc_copy_template=init_id)

            # use the document outline instructions to build out the document base 
            doc_obj.build_from_dict_data(doc_outline_dict,100)

            # perform final replacements
            # doc_obj.replace_m_values(replacement_texts)
            print(doc_obj.get_url())
    return "Hello World"

if __name__ == "__main__":
    app.run()


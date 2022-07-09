# Current as of 7/7

from flask import Flask, request, abort, jsonify
from document import Document

app = Flask(__name__)

def store_parameter(parameter_name, json_received):
    if parameter_name in json_received:
        return json_received[parameter_name]
    else:
        return None

def parameter_extraction():
    print("1. Parameter Extraction - Started")
    json_received = request.get_json()
    if json_received is None:
        abort(400, description='The request does not contain properly formatted JSON data.')
    # Storing API parameters locally
    # Mandatory parameters
    doc_outline = store_parameter('doc_outline', json_received)
    doc_name = store_parameter('doc_name', json_received)
    gdoc_selected = store_parameter('gdoc_selected', json_received)
    # Optional parameters
    init_id = store_parameter('init_id', json_received)
    replacement_values = store_parameter('replacement_values', json_received)
    print("1. Parameter Extraction - Finished")
    return [doc_outline, doc_name, gdoc_selected, init_id, replacement_values]

def parameter_validation(doc_outline, doc_name, gdoc_selected, init_id, replacement_values):
    print("2. Parameter Validation - Started")
    # Checking that all necessary inputs were provided, typed, and formatted correctly
    if not isinstance(doc_outline, list):
        abort(400, description='A doc_outline list input is required.')
    if not isinstance(doc_name, str):
        abort(400, description='A doc_name string input is required.')
    if not isinstance(gdoc_selected, bool):
        abort(400, description='A gdoc_selected boolean input is required.')
    if gdoc_selected and not isinstance(init_id, str):
        abort(400, description='Since gdoc_selected is True, an init_id string input is required.')
    if replacement_values is not None and not isinstance(replacement_values, dict):
        abort(400, description='If replacement_values is provided as an input, it must be a dictionary.')
    print("2. Parameter Validation - Finished")

def document_generation(doc_outline, doc_name, gdoc_selected, init_id, replacement_values):
    print("3. Document Generation - Started")
    doc_product = None
    if gdoc_selected:
        # Instantiate the Google Docs object
        doc_obj = Document(doc_name=doc_name, doc_copy_template=init_id)
        # Use the document outline instructions to build out the document
        doc_obj.build_from_dict_data(doc_outline, 1000)
        # Perform the final replacements
        doc_obj.replace_m_values(**replacement_values)
        doc_product = doc_obj.get_url()
    else:
        doc_product = "foobar"
    print("3. Document Generation - Finished")
    return doc_product

@app.route('/doc-engine', methods=['POST'])
def generate_doc():
    if request.method == 'POST':
        print("A POST request has been received.")
        
        # Step 1: Parameter Extraction
        doc_outline, doc_name, gdoc_selected, init_id, replacement_values = parameter_extraction()
 
        # Step 2: Parameter Validation
        parameter_validation(doc_outline, doc_name, gdoc_selected, init_id, replacement_values)

        # Step 3: Document Generation
        doc_product = document_generation(doc_outline, doc_name, gdoc_selected, init_id, replacement_values)

        data = {'url': doc_product}
        print("A response containing the document has been sent.")
        return jsonify(data), 200

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(port=8000)
import json
import logging
import requests
import sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,format='%(asctime)s -  %(levelname)s -  %(message)s')
logging.disable(logging.DEBUG)

url = "http://127.0.0.1:5000/sdwan-preprocessor"
	

 
# this data directly set up by postman --tested and it does work elsewhere.  
# 7-5:  made this a separate file in a separate folder to check that it's working. 
files=[
	('file',('store_filtered_file.yaml',open(r'C:\Users\estahl\projects\SDWAN-api-poc\yaml\newraw_data_cp.yaml', 'rb'), 'application/octet-stream'))
] 

payload={
	'gdoc_type': True,
	'product': 'sdwan',
	'doc_name': 'Blessed Test Doc that Definitely Works',
	'init_id': 12342311

    # I don't think I put the yaml file here. it's arriving separately from the payload, via files.
}


# read up on diff between data=payload vs json=payload
# does this mean you CAN send api calls as dict objs rather than json strings?
# but steve said only json or xml.......
response = requests.request("POST", url, data=payload, files=files)
logging.info('Reply is: {}'.format(response.text))
#logging.debug('Check contents of "response.json": {}'.format(response.json))
#logging.debug('Check contents of "response.request": {}'.format(response.request))


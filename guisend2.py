import json
import requests

url = "http://127.0.0.1:5000/from-gui"
	

 
# this data directly set up by postman --tested and it does work elsewhere.  
# 7-5:  made this a separate file in a separate folder to check that it's working. 
files=[
	('file',('store_filtered_file.yaml',open(r'C:\Users\estahl\projects\SDWAN-api-poc\yamlclone\newraw_data_cp.yaml', 'rb'), 'application/octet-stream'))
] 

payload={
	'gdoc_type': True,
	'product': 'sdwan'  
    # I don't think I put the yaml file here. it's arriving separately from the payload, via files.
	}


# read up on diff between data=payload vs json=payload
# does this mean you CAN send api calls as dict objs rather than json strings?
# but steve said only json or xml.......
response = requests.request("POST", url, data=payload, files=files)

# can't send as a requests.post because there is no 'files' param 
# ...although 'data' may also parse file object...
# response = requests.post(url, json=payload)

print(response.text)
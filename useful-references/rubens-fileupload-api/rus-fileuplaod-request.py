from Flask import requests

url = "http://127.0.0.1:5000/file-upload"
	
payload={
	'gdoc_type': True,
	'product': 'sdwan'
	}
 
#this data directly set up by postman --it does work. 
# TODO:  Change the url to the actual one used by the yaml file.
files=[
	('file',('store_filtered_file.yaml',open('big_url_to_the_yaml_file.yaml', 'rb'), 'application/octet-stream'))
]

# Could have included a 'headers' dict to send things in http header 
# if so, we would have included "headers=headers"
response = requests.request("POST", url, data=payload, files=files)

respose = requests.post(url, data=payload)
print(response.text)
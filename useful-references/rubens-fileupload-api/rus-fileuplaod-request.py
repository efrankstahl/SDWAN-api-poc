from Flask import requests

url = "http://127.0.0.1:5000/file-upload"
	
payload={
	'gdoc_type': True,
	'product': 'sdwan',
	}
 
#this data directly set up by postman --it does work. 
files=[
	('file',('store_filtered_file.yaml',open('big_url_to_the_yaml_file.yaml', 'rb'),	
		application/octet-stream'))
]

response = requests.request("POST", url, headers=headers, data=payload, files=files)

respose = request.post(url, data=payload)
print(response.text)
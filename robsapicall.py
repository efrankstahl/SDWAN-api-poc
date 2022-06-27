# an api call is a separate script in its own file? 
import requests
url = 'http://127.0.0.1:5000/doc-engine'

payload = {
    'doc_outline': 'doc_outline.json',
    'doc_name': 'As-Built Documentation',
    'gdoc_selected': True,
    'init_id': 'fosakd;fa;dsjghi;fodagjalfdjfalfjasfajsfafa'
}
# send the api above via POST to the url specified
# sooo all we'd need to do is send it to the templating engine!

# here is the actual sending

response = requests.post(url, data=payload)

print(response.text)

 
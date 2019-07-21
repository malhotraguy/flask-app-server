import requests

# url = "http://rss.concured.com:9090//upload-xml"
url="http://0.0.0.0:9090/upload-xml"
# url='http://httpbin.org/post'
# m = MultipartEncoder(fields={'field0': (None,open('Dummy-Blog0_rss.xml', 'rb'), 'text/xml')})

m = {"file": ("", open("Dummy-Blog0_rss.xml", "rb"), "multipart/form-data")}
# m={"file":('image', <FileStorage: 'Dummy-Blog0_rss.xml' ('text/xml'))}
# print(m.to_string() )
r = requests.post(url, files=m)
# r = requests.post(url=url, data=m,
#                   headers={'Content-Type': m.content_type})
print("r=", r)

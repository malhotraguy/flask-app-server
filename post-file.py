import requests
from time import sleep

url = "http://rss.concured.com:9090//upload-xml"
# url = "http://0.0.0.0:9090/upload-xml"
# url='http://httpbin.org/post'
# m = MultipartEncoder(fields={'field0': (None,open('Dummy-Blog0_rss.xml', 'rb'), 'text/xml')})
file_path = "/home/rahul/PycharmProjects/platform/content_crawler/PainKiller Version3/output/Avira-All-News0_rss.xml"
file_name = "Avira-All-News0_rss.xml"
m = {"file": (file_name,
              open(file_path, "rb"),
              "multipart/form-data")}
# m={"file":('image', <FileStorage: 'Dummy-Blog0_rss.xml' ('text/xml'))}
# print(m.to_string() )
r = requests.post(url, files=m)
# r = requests.post(url=url, data=m,
#                   headers={'Content-Type': m.content_type})
print("r=", r)
#sleep(5.0)
file_path = "/home/rahul/PycharmProjects/platform/content_crawler/PainKiller Version3/output/Kasper Sky-Blog1_rss.xml"
file_name = "Kasper Sky-Blog1_rss.xml"
m = {"file": (file_name,
              open(file_path, "rb"),
              "multipart/form-data")}
# m={"file":('image', <FileStorage: 'Dummy-Blog0_rss.xml' ('text/xml'))}
# print(m.to_string() )
r = requests.post(url, files=m)
# r = requests.post(url=url, data=m,
#                   headers={'Content-Type': m.content_type})
print("r=", r)

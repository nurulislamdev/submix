import time
import requests
import sys

site = sys.argv[1]
wordlist = sys.argv[2]

method = int(input("Is target http(1) or https(2):"))
if method == 1:
    method = "http"
    method_message = "method set to http"
else:
    method = "https"
    method_message = "method set to https"

print("trying to find subdomain....")
time.sleep(0.3)
print(method_message)

sub = open(wordlist).read()
subs = sub.splitlines()
for s in subs:
    url = "{}://{}.{}".format(method, s, site)
    try:
        requests.get(url)
    except Exception as ex:
        pass
    else:
        print("[ valid ]", url)

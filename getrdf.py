from __future__ import print_function
import requests
import sys

if sys.argv[1]:
    r = requests.get(sys.argv[1], headers={'Accept':'application/rdf+xml'})
    if r.ok:
        print(r.text)
    else:
        print("Error: %s (%s)", r.status_code, r.reason)
else:
    print("Usage: python getrdf <URL>")







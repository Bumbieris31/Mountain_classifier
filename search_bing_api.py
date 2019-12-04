from requests import exceptions
import argparse
import requests
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
args = vars(ap.parse_args())

#
API_KEY = "5b15f1dd2bc447c3a43759bd1b048a77"
MAX_RESULTS = 300
GROUP_SIZE = 50
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images"

#
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])

#
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

#
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

#
results = search.json()
est_num_results = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(est_num_results, term))

total = 0

for offset in range(0, est_num_results, GROUP_SIZE):
	#
	print("[INFO] making request for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, est_num_results))
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}".format(
		offset, offset + GROUP_SIZE, est_num_results))
	for v in results["value"]:
		try:
			#
			print("[INFO] fetching: {}".format(v["contentURL"]))
			r = requests.get(v["contentURL"], timeout=30)
			#
			ext = v["contentUrl"][v["contentUrl"].rfind("."):]
			p = os.path.sep.join([args["output"], "{}{}".format(
				str(total).zfill(8), ext)])
			#
			f = open(p, "wb")
			f.write(r.content)
			f.close()

		#
		except Exception as e:
			#
			if type(e) in EXCEPTIONS:
				print("[INFO] skipping: {}".format(v["contentUrl"]))
				continue

		#
		image = cv2.imread(p)

		#
		if image is None:
			print("[INFO] deleting: {}".format(p))
			os.remove(p)
			continue

		#
		total += 1

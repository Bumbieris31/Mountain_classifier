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

API_KEY = "5b15f1dd2bc447c3a43759bd1b048a77"
MAX_RESULTS = 300
GROUP_SIZE = 50
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images"


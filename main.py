import http.client
import os
import urllib.request
import webbrowser
from urllib.error import *
import time

toggleMDN = False


def is_it_down(url):
	url = url.strip()
	if "http://" != url[:7] and "https://" != url[:8]:
		url = "https://" + url
	try:
		t1 = round(time.time() * 1000)
		res = urllib.request.urlopen(url)
		t2 = round(time.time() * 1000)
		# print(res.getcode())
		print(res.geturl())
		if res.geturl() != url:
			print(f"[Redirected] {url} → {res.geturl()}")
			url = res.geturl()
		print(f"{url} is up! {t2 - t1}ms")
		return 0
	except HTTPError as e:
		if toggleMDN is False:
			print(f"{url} is down! ({e.code} {e.reason})")
		elif toggleMDN is True:
			print(f"{url} is down! (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{e.code})")
		if e.code == 418:
			webbrowser.open("shorturl.at/mprR9", new=2)
		return 1
	except URLError as e:
		print(f"{e.reason}: {url}")
	except http.client.InvalidURL as e:
		print(f"{url} is not a valid URL.")


print("Welcome to IsItDown.py!")
print("Please write a URL or URLs you want to check. (separated by comma)")
loop = True
while loop:
	url_list = [i for i in input().split(",")]
	if url_list == ["stop"]:
		loop = False
		print("Goodbye!")
		break
	if url_list == ["clear"] or url_list == ["cls"]:
		os.system('cls' if os.name == 'nt' else 'clear')
		continue
	if url_list == ["debug"]:
		debuglist = open("debuglist.txt", "r")
		url_list = [i for i in debuglist.read().split(",")]
		# print(url_list)
		t1 = round(time.time())
		for i in url_list:
			is_it_down(i)
		t2 = round(time.time())
		print(f"Sent requests to {len(url_list)} url(s) from debuglist.txt in {t2 - t1} seconds.")
		continue
	if url_list == ["mdn"]:
		if toggleMDN is True:
			toggleMDN = False
			print("MDN web docs off.")
		elif toggleMDN is False:
			toggleMDN = True
			print("MDN web docs on.")
		continue
	else:
		# print(url_list)
		up = 0
		down = 0
		for i in url_list:
			retVal = is_it_down(i)
			if retVal == 0:
				up += 1
			elif retVal == 1:
				down += 1
		print(f"Up: {up}, Down: {down}")
		continue

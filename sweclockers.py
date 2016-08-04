#! /bin/python3

import requests, time
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

pb = Pushbullet("API KEY")

# Only first page
catalog = requests.get("http://www.sweclockers.com/forum/118-annonskommentarer")
catalog = BeautifulSoup(catalog.content, "html.parser")

# Gets the keywords from a txt file
with open("keywords.txt") as keywords_txt:
		keywords = keywords_txt.read().split(",")

print(keywords)

class sweclockers(object):
	# Class for induvidial articles
	def __init__(self, url):
		self.url = url
		self.content = BeautifulSoup(requests.get(url).content, "html.parser")

	def headline(self):
		# Gets headline
		return str(self.content.find("h1").get_text())

	def main_post(self):
		# Gets the op
		text = ""
		for div in self.content.find_all("div"):
			if div.get("class") == ["forumPosts"]:
				page = div.find("div")

		for div in page.find_all("div"):
			if div.get("class") == ["text"]:
				page = div
		for p in page.find_all("p"):
			text += str(p)
	
		return text

	def amount_replies(self):
		# DOESN'T WORK
		replies = 0

		for div in self.content.find_all("div"):
			if div.get("class") == ["forumPosts"]:
				for i in div.find_all("div"):
					print(div.get("class"))
					if "forumPost" in div.get("class"):
						replies += 1
				break
		return replies

	def check_keyword(self):
		# Checks the op for the keywords
		post = self.main_post()

		for keyword in keywords:
			if keyword in post:
				return True
		else:
			return False

def get_catalog():
	articles = []
	# Gets the all the articles as a link and puts them in a list
	for tbody in catalog.find_all("tbody"):
		if tbody.get("class")[0] == "body":
			for tr in tbody.find_all("tr"):
				# The index thing is for that the url has some uneccesery stuff in it at the end
				articles.append("http://www.sweclockers.com%s" % tr.a.get("href")[:len(tr.a.get("href"))-13])
			break

	else:
		quit()

	return articles
while True:
	# Forever loop that checks the keywords and if true sends a pushbullet
	for article_url in get_catalog():
		article = sweclockers(article_url)
		if article.check_keyword():
			push = pb.push_link(article.headline(), article.url)
	time.sleep(600)

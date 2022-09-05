import requests, json
from bs4 import BeautifulSoup


def get_tags(url):
	tags = BeautifulSoup(requests.get(url).text, 'html.parser').find_all(class_="detail__body-tag")
	if len(tags) < 1: return []
	return [i.text for i in BeautifulSoup(str(tags[0]), 'html.parser').find_all("a")]


def list_news(query, saveTo):
	pagination = 1
	result = []
	while True:
		url = "https://www.detik.com/search/searchall?query="+query
		if pagination != 1 or pagination != 0: url+="&sortby=time&page="+str(pagination)
		all_news = BeautifulSoup(requests.get(url).text, 'html.parser').find_all("article")
		if len(all_news) < 1: break
		for news in all_news:
			article = BeautifulSoup(str(news.extract()), 'html.parser')
			# Get url
			url = article.find_all("a", href=True)
			if len(url) > 0:
				url = url[0]["href"]
			else:
				url = ""
			# get title
			title = article.find_all(class_="title")
			if len(title) > 0:
				title = title[0].text
			else:
				title = ""
			# get date
			date = article.find_all(class_="date")
			if len(date) > 0:
				date = date[0].text.replace("detikNews", "")
			else:
				date = ""
			# get tags
			tags = get_tags(url) if url != "" else []

			result.append({"title": title, "url": url, "date": date, "tags": tags})
			json.dump(result, open(saveTo, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
			print(f" [{pagination}] {url}")
		pagination+=1
	return result


def main():
	saveTo = str(input(" [*] Save result to : "))
	if saveTo.split(".")[-1] != "json": saveTo+=".json"
	query = str(input(" [*] Keyword : "))
	list_news(query, saveTo)
	print(" Data was successfulyt saved to : "+saveTo)

if __name__ == '__main__':
	main()
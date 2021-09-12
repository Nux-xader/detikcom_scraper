import requests, json
from bs4 import BeautifulSoup



def scrap(query, pagination=1):
	url = "https://www.detik.com/search/searchall?query="+query
	if pagination != 1 or pagination != 0:
		url+="&sortby=time&page="+str(pagination)
	all_news = requests.get(url).text
	all_news = BeautifulSoup(all_news, 'html.parser')
	all_news = all_news.find_all("article")
	result = []
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
		result.append({"title": title, "url": url, "date": date})
	return result

def main():
	saveTo = str(input(" Save result to : "))
	if saveTo.split(".")[-1] != "json": saveTo+=".json"
	query = str(input(" Query : "))
	pagination = int(input(" Pagination (1, 2, 3, ...): "))
	data = scrap(query, pagination)
	with open(saveTo, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)
	print(" Data was successfulyt saved to : "+saveTo)

if __name__ == '__main__':
	main()
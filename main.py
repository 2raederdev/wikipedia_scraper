import requests
from bs4 import BeautifulSoup


def wantToContinue():
	confirm = input('Do you want to try it again? (y/n): ')

	if confirm[0].lower() == 'y':
		scrapeWikiArticle()
	else:
		return False


def scrapeWikiArticle():
	url = input('Please, enter the URL of a Wikipedia article: ')

	# Check for valid URL
	if not url.startswith('http') or 'wikipedia.org' not in url:
		print('Sorry, the URL might be wrong as there are no links to Wikipedia articles. Please remember that a valid URL should always start with \'http\' as well.')

		# If wrong URL, confirm if the user wants to continue
		if not wantToContinue():
			print('Bye!')
			return

		
	response = requests.get(url=url)

	soup = BeautifulSoup(response.content, 'html.parser')

	# Find the h1 (title of the article, the term you are looking for) by the ID tag.
	title = soup.find(id="firstHeading")

	print(f'The title of the article is \'{title.text}\'\n')

	# Now, let's get all the links within the content of the article. The article is inside a DIV with the ID "bodyContent".
	links = soup.find(id="bodyContent").find_all("a")
	internal_links = filter(lambda link: link['href'].find("/wiki/") == 0, links)

	if not internal_links:
		print('Sorry, but something went wrong.')

		if not wantToContinue():
			print('Bye!')
			return
	
	for internal_link in internal_links:
		if internal_link.string:
			print(internal_link.string)

	print('\nThis was the list of all the internal links founded in the Wikipedia article. Thank you!')


scrapeWikiArticle()
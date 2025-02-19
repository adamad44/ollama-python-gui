import requests
from bs4 import BeautifulSoup


url = 'https://ollama.com/search'

response = requests.get(url)

listOfLLMS = [] 


if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
   
    links = soup.find_all('a')
    for link in links:
        linkHREF = link.get('href')
        if "/library/" in linkHREF:
            LLMName = linkHREF.split("/library/")[1]
            listOfLLMS.append(LLMName)
        
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


for i in listOfLLMS:
    print(i)
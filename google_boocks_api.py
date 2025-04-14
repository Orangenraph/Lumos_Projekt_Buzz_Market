import requests
import json

'''
searches for specific book
https://www.googleapis.com/books/v1/volumes?q=Die+Verwandlung

searches for author
https://www.googleapis.com/books/v1/volumes?q=autor:Franz+Kafka

searches for thema
https://www.googleapis.com/books/v1/volumes?q=thema:finance
'''

"""
mail: xxxx
PW: xxxxx
key : 75u5apwOgBLGVJZyWhmF0wGUTuuoe51O
secret: qGeAcaesxaO7aJSj
"""
api_key = '75u5apwOgBLGVJZyWhmF0wGUTuuoe51O'


def main():
    '''....v3/lists/{date}/{list}.json'''
    api_key = '75u5apwOgBLGVJZyWhmF0wGUTuuoe51O'

    #url = f"https://api.nytimes.com/svc/books/v3/lists/2020-01-01/combined-print-and-e-book-fiction.json?api-key={api_key}"
    url = f"https://api.nytimes.com/svc/books/v3/lists/2020-01-01/combined-print-and-e-book-nonfiction.json?api-key={api_key}"#starts at 2012-01-01
    #url = f"https://api.nytimes.com/svc/books/v3/lists/names.json?api-key={api_key}"
    #url = f"https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date=2019-01-01&api-key={api_key}"

    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=2))

    # Beispiel: Liste der Top-Bücher
    print(data["results"]["bestsellers_date"]) # 2011-12-17
    for book in data['results']['books']:
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Rank: {book['rank']}")
        print(f"Weeks on list: {book['weeks_on_list']}")
        print(f"Amazon product url: {book['amazon_product_url']}")
        print("-" * 40)

if __name__ == "__main__":
    main()

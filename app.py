from flask import Flask, render_template, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_restaurant_data(city_name):
    search_query = f"top restaurants in {city_name}"
    google_search_url = f"https://www.google.com/search?q={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(google_search_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    # restaurant_names = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    restaurant_names = soup.find_all('div', class_='OSrXXb')

    ratings = soup.find_all('span', class_='yi40Hd.YrbPuc')
    reviews = soup.find_all('span', class_='RDApEe.YrbPuc')

    restaurant_data = []
    for i in range(min(len(restaurant_names), 10)):
        name = restaurant_names[i].get_text()
        rating = ratings[i].get_text() if i < len(ratings) else "N/A"
        review = reviews[i].get_text() if i < len(reviews) else "N/A"

        restaurant_data.append({
            'name': name,
            'rating': rating,
            'reviews': review
        })

    return restaurant_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        restaurants = get_restaurant_data(city)
        return render_template('results.html', restaurants=restaurants, city=city)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





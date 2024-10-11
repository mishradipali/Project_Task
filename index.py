import requests
import json

def fetch_restaurants(city):
    """
    Fetches the top 10 restaurants in the specified city using Google Places API.

    Args:
        city (str): The name of the city to search for restaurants.

    Returns:
        dict: A dictionary containing restaurant names as keys and their details as values.
    """
    # Your Google Places API key
    api_key = 'YOUR_API_KEY'  
    location = city.replace(' ', '+')
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+{location}&key={api_key}"
    
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return {}

    data = response.json()
    
    restaurants = {}
    for place in data.get('results', [])[:10]:  # Limit to top 10 results
        name = place['name']
        rating = place.get('rating', 'N/A')
        review_count = place.get('user_ratings_total', 'N/A')
        restaurants[name] = {
            'rating': rating,
            'reviews': review_count
        }
    
    return restaurants

def save_to_json(data, filename='restaurants.json'):
    """
    Saves the given data to a JSON file.

    Args:
        data (dict): The data to save.
        filename (str): The file name to save data to.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    """
    Main function to execute the script.
    """
    # Prompt the user for a city name
    city = input("Enter the name of a city: ")
    
    # Fetch restaurant data
    restaurant_data = fetch_restaurants(city)
    
    # Save the data to a JSON file
    if restaurant_data:  # Only save if data is available
        save_to_json(restaurant_data)
        print(f"Top 10 restaurants in {city} have been saved to 'restaurants.json'.")
    else:
        print("No restaurant data found.")

if __name__ == "__main__":
    main()

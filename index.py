import requests
from bs4 import BeautifulSoup
import json

def fetch_restaurants(city):
    """
    Fetches the top 10 restaurants in the specified city using Google search.

    Args:
        city (str): The name of the city to search for restaurants.

    Returns:
        dict: A dictionary containing restaurant names as keys and their details as values.
    """
    # Format the search URL for Google
    search_url = f"https://www.google.com/search?q=top+restaurants+in+{city.replace(' ', '+')}"
    
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    
    # Send a request to Google
    response = requests.get(search_url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return {}

    # Debugging line: Print the first 1000 characters of the response
    print("HTML Response Snippet:")
    print(response.text[:1000])  # Shows the beginning of the response

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize a dictionary to store restaurant data
    restaurants = {}

    # Attempt to extract restaurant information
    for index, restaurant in enumerate(soup.find_all('div', class_='BNeawe iBp4i AP7Wnd')):  # Update class names as needed
        if index >= 10:  # Limit to top 10 restaurants
            break
        name = restaurant.get_text()
        
        # Extract additional details like ratings and reviews (if available)
        details = restaurant.find_next_sibling('div', class_='BNeawe s3v9rd AP7Wnd')  # Update class names as needed
        if details:
            details_text = details.get_text().split(' · ')
            rating = details_text[0] if len(details_text) > 0 else "N/A"
            review_count = details_text[1] if len(details_text) > 1 else "N/A"
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
        filename (str): The name of the file to save data to.
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

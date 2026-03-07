import httpx
import urllib.parse
from bs4 import BeautifulSoup

def scrape_elite_hubs(query):
    print(f"Searching EliteHubs for: {query}")
    encoded = urllib.parse.quote(query)
    url = f"https://elitehubs.com/search?type=product&options%5Bprefix%5D=last&q={encoded}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    response = httpx.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}")
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Elitehubs is Shopify based, products are usually in grid items
    products = soup.select('.grid__item .card-wrapper')
    
    if not products:
        print("No products found.")
        return None
        
    first_product = products[0]
    
    # Try multiple common Shopify price selectors
    price_element = first_product.select_one('.price-item--sale')
    if not price_element:
        price_element = first_product.select_one('.price-item--regular')
        
    if price_element:
        # Extract the text and clean it up (e.g. "Rs. 18,500.00")
        raw_price = price_element.text.strip()
        print(f"Found Raw Price Text: {raw_price}")
        
        # Parse it into a float
        clean_price = "".join(c for c in raw_price if c.isdigit() or c == '.')
        try:
            return float(clean_price)
        except ValueError:
            pass
            
    print("Could not find price element in the first product card.")
    return None

if __name__ == "__main__":
    price = scrape_elite_hubs("Ryzen 5 7600X")
    print(f"Final Parsed Price: {price}")

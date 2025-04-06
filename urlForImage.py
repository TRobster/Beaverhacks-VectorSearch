import requests

def get_card_image_by_uuid(uuid):
    url = f"https://api.scryfall.com/cards/{uuid}"
    
    response = requests.get(url)
    if response.status_code == 200:
        card_data = response.json()
        if 'image_uris' in card_data:
            image_url = card_data['image_uris']['normal']
            return image_url
        else:
            return "Image not available for this card."
    else:
        return "Card not found."

# Example usage
uuid = "b7c19924-b4bf-56fc-aa73-f586e940bd42"
image_url = get_card_image_by_uuid(uuid)
if image_url:
    print(f"Image URL for card with UUID {uuid}: {image_url}")
else:
    print(f"Card with UUID {uuid} not found.")
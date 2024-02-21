import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_section_content', methods=['POST'])
def get_section_content():
    data = request.get_json()
    section_number = data.get('section_number')

    # Call the function to fetch content for the given section number
    section_content = fetch_section_content(section_number)

    return jsonify({'section_content': section_content})

def fetch_section_content(section_number):
    base_url = "https://lawrato.com/indian-kanoon/ipc/section-"
    link = f"{base_url}{section_number}"

    # Fetch the content of the linked page
    response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    linked_page_content = response.text

    # Parse the content of the linked page with BeautifulSoup
    linked_page_soup = BeautifulSoup(linked_page_content, 'html.parser')

    # Extract content within the <div> with class "answer-box"
    answer_box = linked_page_soup.find('div', class_='answer-box')
    if answer_box:
        return answer_box.text.strip()
    else:
        return f"No content found in the specified <div> on the linked page: {link}"

if __name__ == '__main__':
    # Use PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

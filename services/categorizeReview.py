import time
import os
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Configuring every dotenv keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
mongo_uri = os.getenv("MONGODB_URL")

# MongoDB setup
client = MongoClient(mongo_uri)
db = client['review_monitor']
reviews_collection = db['reviews']

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Function to scrape reviews from the Google Play page
def scrape_reviews():
    url = os.getenv("GAME_URL")
    driver.get(url)
    
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    user_reviews = [div.get_text(strip=True) for div in soup.find_all('div', class_='h3YV2d')]
    review_dates = [span.get_text(strip=True) for span in soup.find_all('span', class_='bp9Aid')]

    reviews = []
    for div_text, span_text in zip(user_reviews, review_dates):
        reviews.append({
            "review_text": div_text,
            "date": span_text
        })

    return reviews

# Function to classify a review using generative AI
def classify_review(review_text):
    prompt = f"""
    You are an expert linguist, who is good at classifying user reviews into Bugs/Complaints/Crashes/Praises/others.
    Help me classify user reviews into: Bugs/Complaints/Crashes/Praises/others.
    User review: {review_text}
    """
    response = model.generate_content(prompt)
    
   
    if response and response._result.candidates:
        return response._result.candidates[0].content.parts[0].text.strip()
    return "Unknown"


def main():
    reviews = scrape_reviews()
    categorized_reviews = []
    
    for review in reviews:
        category = classify_review(review["review_text"])
        review_data = {
            "text": review["review_text"],
            "category": category,
            "date": review["date"]
        }
        
        # Insert into MongoDB
        result = reviews_collection.insert_one(review_data)
        review_data["_id"] = str(result.inserted_id)
        categorized_reviews.append(review_data)

    
    driver.quit()

    
    print(json.dumps(categorized_reviews, indent=2))

if __name__ == "__main__":
    main()

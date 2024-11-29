import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import json
from datetime import datetime

date_string = sys.argv[1]

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
mongo_uri = os.getenv("MONGODB_URL")

client = MongoClient(mongo_uri)
db = client['fullDaySummary']
oneDayReviewCollection = db['daysummary']

def reviews_summary(reviews):
    prompt = """
    You are an expert linguist and analyist, who is good at making summary of important point.
    Help me to make short summary of reviews by extracting important data.
    User reviews = {reviews}
    """
    response = model.generate_content(prompt)
    return response
    
def aggregate_reviews():
    pipeline = [
        {"$match": {"date": date_string}},  
        {"$group": {"_id": None, "all_reviews": {"$push": "$text"}}}
    ]
    result = list(oneDayReviewCollection.aggregate(pipeline))
    if result:
        all_reviews_text = " ".join(result[0]["all_reviews"])
        return all_reviews_text
    else:
        return "No reviews found for this date."
    
    
def main():
    all_reviews = aggregate_reviews()
    reviews = reviews_summary(all_reviews)
    review_data = {
            "text": reviews,
            "date": datetime.now
        }
    result = oneDayReviewCollection.insert_one(review_data)
    print(json.dumps(result, indent=2))
    
    
if __name__ == "__main__":
    main()
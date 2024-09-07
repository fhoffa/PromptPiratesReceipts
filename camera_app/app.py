from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import base64
import boto3
import logging
from sqlalchemy import create_engine, text
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json
# import os
from geopy.geocoders import Nominatim

url = 'postgresql://'
# Create SQLAlchemy engine
engine = create_engine(url)

def geocode_address(address):
    geolocator = Nominatim(user_agent="GeoExpenses3")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def insert_expense(user_id, price, datetime, description, category, location, latitude, longitude):
    query = text("""
    INSERT INTO trip_expenses (user_id, price, datetime, description, category, location, latitude, longitude)
    VALUES (:user_id, :price, :datetime, :description, :category, :location, :latitude, :longitude)
    """)

    with engine.connect() as conn:
        conn.execute(query, {
            "user_id": user_id,
            "price": price,
            "datetime": datetime,
            "description": description,
            "category": category,
            "location": location,
            "latitude": latitude,
            "longitude": longitude
        })
        conn.commit()

def send_data_to_storage(user_id, price, datetime, description, category, location, latitude, longitude):
    try:
        insert_expense(
            user_id=user_id,  # "fat_guy",
            price=price,  # 10.99,
            datetime=datetime, # datetime.now(),
            description=description,  # "McDonalds",
            category=category, # "Food",
            location=location, # "609 Market St, San Francisco, CA 94105"
            latitude=latitude,
            longitude=longitude
        )
        print("Expense inserted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

app = Flask(__name__)

# Initialize Amazon Bedrock client
client = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id='ID', aws_secret_access_key='KEY')  # Make sure to replace with your correct region

prompt = 'Use english language for the results. Give me in a json format the datetime, price, description, location, and category (like food, transportation, etc.) of the receipt. The description should the a summary of the meal in a single string. The location should be an address. The category should be a string.'

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set logging level to INFO

    # Example log statements
    logger.info("Lambda function started")
    # logger.debug("Processing event data: %s", event)

    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image']

    # Remove the "data:image/png;base64," part from the string
    image_data = image_data.replace('data:image/png;base64,', '')

    try:
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(image_data)

        # Convert bytes to a PIL Image for potential preprocessing
        image = Image.open(BytesIO(image_bytes))

#        image_paths = []
#        directory = '../images'
#        for filename in os.listdir(directory):
#            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
#                image_paths.append(os.path.join(directory, filename))
#        for image_path in image_paths:
#            print(image_path)
#            image = Image.open(image_path)

        image = image.convert('RGB')

        # Optionally save the image for debugging
        # image.save("uploaded_image.jpg", "JPEG")

        # Convert image to base64 to send to Bedrock API if necessary
        buffered = BytesIO()
        image.save(buffered, format="jpeg")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        logger.info("Calling Claude")
        # Call to Claude model on Amazon Bedrock
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # Use your Claude model version
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                        {
                            "type": "image",
                            "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                        ]
                    }
                ]
            })
        )

        # Process the response from the Claude model
        result = response['body'].read().decode('utf-8')

        try:
            output =  json.loads(json.loads(result)["content"][0]["text"])
        except:
            return jsonify({'error': 'No text data found in response: '+json.loads(result)["content"][0]["text"]})

        latitude = None
        longitude = None
        try:
            latitude, longitude = geocode_address(output["location"])
        except Exception as e:
            print(f"Error fetch GPS coords for: '{output["location"]}' : {e}")
        send_data_to_storage("tiago", output["price"], output["datetime"], output["description"], output["category"], output["location"], latitude, longitude)

        return jsonify({'success': True, 'message': 'Image processed', 'response': result})

    except NoCredentialsError as e:
        print("AWS credentials not found or invalid.")
        return jsonify({'error': 'AWS credentials not found or invalid.'}), 500

    # except client.exceptions.ServiceError as e:
    #    print(f"Amazon Bedrock service error: {e}")
    #    return jsonify({'error': 'Amazon Bedrock service error.'}), 500

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

    logger.info("Lambda function finished")

if __name__ == '__main__':
    app.run(debug=True)

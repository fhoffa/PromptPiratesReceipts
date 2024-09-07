from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import base64
from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
import boto3

app = Flask(__name__)

# Initialize Amazon Bedrock client
client = boto3.client('bedrock-runtime', region_name='us-west-2')  # Make sure to replace with your correct region

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Image data not provided'}), 400
    
    image_data = data['image']
    prompt = 'Use english language for the results. Give me in a json format the date, cost, taxes, description, location (address), and category (like food, transportation, etc.) of the receipt.'

    # Remove the "data:image/png;base64," part from the string
    image_data = image_data.replace('data:image/png;base64,', '')
    
    try:
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to a PIL Image for potential preprocessing
        image = Image.open(BytesIO(image_bytes))
        
        # Optionally save the image for debugging
        image.save("uploaded_image.png", "PNG")
        
        # Convert image to base64 to send to Bedrock API if necessary
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Call to Claude model on Amazon Bedrock
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # Use your Claude model version
            contentType="application/json",
            accept="application/json",
            body={
                "prompt": prompt,
                "image": img_base64
            }
        )
        
        # Process the response from the Claude model
        result = response['body'].read().decode('utf-8')
        
        return jsonify({'success': True, 'message': 'Image processed', 'response': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

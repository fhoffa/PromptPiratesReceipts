from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    # Get the base64 encoded image string
    image_data = data['image']
    
    # Remove the "data:image/png;base64," part from the string
    image_data = image_data.replace('data:image/png;base64,', '')
    
    try:
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to a PIL Image
        image = Image.open(BytesIO(image_bytes))
        
        # Save the image as a file (or you could process it further)
        image.save("uploaded_image.png", "PNG")
        
        # Return success response
        return jsonify({'success': True, 'message': 'Image uploaded successfully!'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64, os, io
from PIL import Image

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Hello, world!"})

# post request, receive parameters id and name
@api_view(['POST'])
def test_api_post(request):
    id = request.data.get('id')
    name = request.data.get('name')
    return Response({"id": id, "name": name})

# a post request, which used to store the image file as a local file at the server side
@api_view(['POST'])
def store_image(request):
    success = False
    image_data = request.data.get('image')
    filename = request.data.get('filename')
    if image_data:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        data = image_data.split("base64,")[1]
        image = Image.open(BytesIO(base64.decodebytes(bytes(data, 'utf-8'))))
        image.save(f'temp/{filename}')
        success = True
    if success:
        return Response({"message": "Image stored successfully", "error": None})
    else:
        return Response({"message": None, "error": "Failed to store image"})


import streamlit as st
from PIL import Image
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from io import BytesIO

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

COG_KEY = '7ced5790185f491c8a751ba945e2a5a4'
COG_ENDPOINT = 'https://ress-compvis.cognitiveservices.azure.com/'

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(COG_ENDPOINT, CognitiveServicesCredentials(COG_KEY))

# The title
st.title("Search engine for images with Azure infra")

# Users can search image from here
search = st.text_input('Search your image here')

# Users can upload images from here
uploaded_file = st.file_uploader("Upload an image", type=['png','jpeg','jpg'], accept_multiple_files=False)

if uploaded_file is not None:
    if st.button("Click to upload"):
        image = Image.open(uploaded_file)


        st.image(image)


        print("Sending file to the blob")


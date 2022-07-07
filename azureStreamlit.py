import io
import uuid
import cv2
import streamlit as st
from PIL import Image
import os
from azure.identity import DefaultAzureCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import numpy as np

# UserName : toky : MOT DE PASSE SQL : Projet@Azure

# https://tokyazureproject.scm.azurewebsites.net:443/TokyAzureProject.git

#credential for blob
credential = DefaultAzureCredential()

# Retrieve the storage blob service URL, which is of the form
# https://stockagetoky.blob.core.windows.net/
storage_url = "https://stockagetoky.blob.core.windows.net"

CONTAINER_NAME = "container-azure-project"

# Cognitive key
COG_KEY = '7ced5790185f491c8a751ba945e2a5a4'
COG_ENDPOINT = 'https://ress-compvis.cognitiveservices.azure.com/'

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(COG_ENDPOINT, CognitiveServicesCredentials(COG_KEY))





##############################################################
# The title
st.title("Search engine for images with Azure infra")

# Users can search image from here
search = st.text_input('Search your image here')


# Users can upload images from here
uploaded_file = st.file_uploader("Upload an image", accept_multiple_files=False)




if uploaded_file is not None:
    if st.button("Click to upload"):
        with open(os.path.join("./image/", uploaded_file.name), "wb") as f :
            f.write(uploaded_file.getbuffer())

        st.success("Upload Successfull")
        # description = computervision_client.tag_image_in_stream("./image/" + str(uploaded_file.name) + ".png")
        with open("./image/" + str(uploaded_file.name),"rb") as image_stream:
            description = computervision_client.tag_image_in_stream(image_stream)

            # Deleting the file:
        # check if file exists or not
        if os.path.exists("./image/" + uploaded_file.name) is True :
            os.remove("image/" + uploaded_file.name)
        # file did not exists


        for tag in description.tags:
            st.write(tag.name)



        # check tags of the file from blob:
        # description = computervision_client.tag_image("https://stockagetoky.blob.core.windows.net/container-azure-project/myfile.png", language="fr")
        #
        # print(type(description))
        # for tag in description.tags:
        #     print(tag.name)

        # st.image(image)
        # st.caption(description)


        print("Sending file to the blob")

if st.button("Blob things"):
    # blob_client = BlobClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=stockagetoky;AccountKey=+rXyX74rnGr7avYqBCG2KaMWzALsV4augUb4yWUzdEj7UuRVVCxQzfcgAye7AVWjZE6y/RZJ9jjT+AStAsLbwQ==;EndpointSuffix=core.windows.net",
    #                                                 container_name="container-azure-project", blob_name="new-blob.txt")

    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=stockagetoky;AccountKey=+rXyX74rnGr7avYqBCG2KaMWzALsV4augUb4yWUzdEj7UuRVVCxQzfcgAye7AVWjZE6y/RZJ9jjT+AStAsLbwQ==;EndpointSuffix=core.windows.net")
    # Instantiate a new ContainerClient
    container_client = blob_service_client.get_container_client("container-azure-project")
    blob_list = container_client.list_blobs()
    for blob in blob_list :
        print("\t" + blob.name)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob="myfile.png")

    print("\nUploading to Azure Storage as blob:\n\t")

    # Upload the created file
    with open("./image/im1.png", "rb") as data :
        print(type(data))
        blob_client.upload_blob(data)


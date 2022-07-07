import streamlit as st
import os
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import BlobServiceClient

# UserName : toky : MOT DE PASSE SQL : Projet@Azure

# https://tokyazureproject.scm.azurewebsites.net:443/TokyAzureProject.git

# credential for blob
# credential = DefaultAzureCredential()

# Retrieve the storage blob service URL, which is of the form
# https://stockagetoky.blob.core.windows.net/
storage_url = "https://stockagetoky.blob.core.windows.net"
image_base_url = "https://stockagetoky.blob.core.windows.net/container-azure-project/"

CONTAINER_NAME = "container-azure-project"

# Cognitive key
COG_KEY = '7ced5790185f491c8a751ba945e2a5a4'
COG_ENDPOINT = 'https://ress-compvis.cognitiveservices.azure.com/'

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(COG_ENDPOINT, CognitiveServicesCredentials(COG_KEY))

# Settings for blob
blob_service_client = BlobServiceClient.from_connection_string(
    "DefaultEndpointsProtocol=https;AccountName=stockagetoky;AccountKey=+rXyX74rnGr7avYqBCG2KaMWzALsV4augUb4yWUzdEj7UuRVVCxQzfcgAye7AVWjZE6y/RZJ9jjT+AStAsLbwQ==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("container-azure-project")

##############################################################
# The title
st.title("Search engine for images with Azure infra")


# Users can search image from here
search = st.text_input('Search your image here')
res = blob_service_client.find_blobs_by_tags(f"\"metadata1\"={search}")
st.image(Image.open(res))

st.write("text you typed : " + search)



# Users can upload images from here
uploaded_file = st.file_uploader("Upload an image", accept_multiple_files=False)

if uploaded_file is not None :
    if st.button("Click to upload") :
        # for file in uploaded_file :
        # print(file)
        with open(os.path.join("./image/", uploaded_file.name), "wb") as f :
            f.write(uploaded_file.getbuffer())
        # description = computervision_client.tag_image_in_stream("./image/" + str(uploaded_file.name) + ".png")
        with open("./image/" + str(uploaded_file.name), "rb") as image_stream :
            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME,
                                                              blob=str(uploaded_file.name))
            # upload the image in a the blob
            res = blob_client.upload_blob(image_stream, overwrite=True)

            print("Image uploaded")

        with open("./image/" + str(uploaded_file.name), "rb") as image_stream :
            description = computervision_client.tag_image_in_stream(image_stream, language='fr')
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME,
                                                              blob=str(uploaded_file.name))
            blob_client.set_blob_metadata(metadata={'tag' : 'test metadata','tag2':'metada2'})
            print("metadata added")

    # Deleting the file:
    # check if file exists or not
    # if os.path.exists("./image/" + uploaded_file.name) is True :
    #     os.remove("image/" + uploaded_file.name)
    #
    # st.image(Image.open(uploaded_file))
    #
    # st.success("Upload Successfull")
    # print("the image url :" + image_base_url + str(uploaded_file.name))
    # for tag in description.tags:
    #     st.write(tag.name)

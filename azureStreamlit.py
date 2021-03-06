import pymysql.cursors
import streamlit as st
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.storage.blob import BlobServiceClient
from msrest.authentication import CognitiveServicesCredentials

# https://tokyazureproject.scm.azurewebsites.net:443/TokyAzureProject.git

# Retrieve the storage blob service URL, which is of the form
# https://stockagetoky.blob.core.windows.net/


storage_url = "https://stockagetoky.blob.core.windows.net"
image_base_url = "https://stockagetoky.blob.core.windows.net/container-azure-project/"

CONTAINER_NAME = "container-azure-project"

# Cognitive key
COG_KEY = <YourKey>
COG_ENDPOINT = <YourEndpoint>

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(COG_ENDPOINT, CognitiveServicesCredentials(COG_KEY))

# Settings for blob
blob_service_client = BlobServiceClient.from_connection_string(
    "DefaultEndpointsProtocol=https;AccountName=<yourAccount>;AccountKey=<YourAccountKey>;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("container-azure-project")

# Connection to mySQL server
cnx = pymysql.connect(user=<Username>, password=<YourUsername>, host=<HOST>,
                      port=3306, database=<DATABASE>)


##############################################################
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #70f1ff;">
  <img src="https://www.groupe-pomona.fr/sites/default/files/reseau/Logo%20PassionFroid.png" style='max-width:120px'/>
</nav>
""", unsafe_allow_html=True)  # navigation bar

# The title
st.title("Moteur de recherche PassionFroid")

# Users can search image from here
with cnx.cursor() as cursor :
    sql_image_display_query = """SELECT DISTINCT tags from images"""
    cursor.execute(sql_image_display_query)
    record = cursor.fetchall()
    record =  (" ",) + record

col1, col2 = st.columns(2)

with st.sidebar:
    st.title("Option de recherche")
    nb_images = st.slider("Number of images to show", 1,30)
    type_recherche = st.radio("Choisissez le type de recherche :", ["Recherche par tag", "Recherche Textuel"])



if type_recherche == "Recherche par tag":
    search = st.selectbox('Rechercher ici', [row[0] for row in record])
    if search is not None:
        st.write("Vous avez cherch?? : " + search)

else:
    text_search = st.text_input("Tapez la recherche")
    if text_search is not None:
        tokens = text_search.split(" ")
        print(tokens)
        all_response = []
    for token in tokens:
        sql_image_display_query = f"SELECT DISTINCT url FROM images WHERE tags='{token}'"
        with cnx.cursor() as cursor :
            cursor.execute(sql_image_display_query)
            rec = cursor.fetchall()
            all_response.append(rec)



# Users can upload images from here
uploaded_files = st.file_uploader("Charger une image ici",type=['jpg','jpeg','png'],help="Charger une image au format jpg,jpeg,png", accept_multiple_files=True)

if uploaded_files is not None :
    tags = []
    if st.button("Cliquer pour charger l'image") :
        for uploaded_file in uploaded_files: #Here begin the multiple images management
            with open(os.path.join("./image/", uploaded_file.name), "wb") as f :
                f.write(uploaded_file.getbuffer())
            with open("./image/" + str(uploaded_file.name), "rb") as image_stream :
                # Create a blob client using the local file name as the name for the blob
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME,
                                                                  blob=str(uploaded_file.name))
                # upload the image in a the blob
                res = blob_client.upload_blob(image_stream, overwrite=True)

            with open("./image/" + str(uploaded_file.name), "rb") as image_stream :
                description = computervision_client.tag_image_in_stream(image_stream, language='fr')
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME,
                                                                  blob=str(uploaded_file.name))
                for tag in description.tags :
                    tags.append(tag.name)
                    # blob_client.set_blob_metadata(metadata={'tag' : 'test metadata','tag2':'metada2'})
                    print("adding tag :" + tag.name)
                    sql_query = f"INSERT INTO images (url,tags) VALUES ('{image_base_url + uploaded_file.name}', '{tag.name}');"
                    print(sql_query)

                    with cnx.cursor() as cursor :
                        cursor.execute(sql_query)
                        cnx.commit()
                        print("tag uploaded")

                st.success("Chargement r??ussi")

            # Deleting the file:
            # check if file exists or not
            if os.path.exists("./image/" + uploaded_file.name) is True :
                os.remove("image/" + uploaded_file.name)

    # Uploaded images display
    st.image(uploaded_files, use_column_width=True)  # To display the uploaded images on the dashboard



if type_recherche == "Recherche par tag":
    counter = 1
    # Searched term images display
    if search is not None :
        with cnx.cursor() as cursor :
            sql_image_display_query = """SELECT DISTINCT url from images where tags = %s"""
            cursor.execute(sql_image_display_query, (search,))
            record = cursor.fetchall()
            for row in record :
                st.image(row[0])
                if counter == nb_images :
                    break
                else :
                    counter += 1
                # print(row[1])
else:

    counter = 1
    print(nb_images)
    for rec in all_response :
        for row in rec:
            st.image(row[0])
            if counter == nb_images:
                break
            else:
                counter+=1

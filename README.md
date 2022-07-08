# AzureProject

To run the project you have to has Streamlit :
**Run :**
*pip install streamlit*

and then run : 
*streamlit run azureStreamlit.py*

to build the container in azure
az acr build --registry TokyAppRegistry --resource-group gr-ia-poc --image tokyapp .
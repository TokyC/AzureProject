# AzureProject

Ce repo est le résultat de notre semaine thématique **Azure**. 
L'objectif du projet était de construire une application en utilisant **Azure** Comme cloud provider.

Commencer par installerles dépendance dans le requirements.txt:
- *pip install -r requirements.txt*

Pour run l'application, il faut se mettre à la racine du projet et lancer la commande suivante:
- *streamlit run azureStreamlit.py*

Sinon vous pouvez l'application dans un container Docker.

Pour build un container dans azure :
- *az acr build --registry <YourRegistry> --resource-group <Your res> --image tokyapp .* 

### Le lien du GIT pour le projet:
- https://github.com/TokyC/DevOpsProject.git

### Le lien du **trello** pour le projet : 
- https://trello.com/invite/b/emJnEMCn/401dcb9b815bb37fdbbfea8f9229d2ea/projet-azure-pomona-passionfroid


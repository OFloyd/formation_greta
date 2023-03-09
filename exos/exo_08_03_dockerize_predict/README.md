# Utilisation de Docker avec le TP sur les RNN pour la classification des commentaires IMDB 

Commande pour construire l'image :
docker build -t rnn_sentiment .

Commande pour créer un container de cette image : 
docker run -dp 5000:5000 --name server_rnn rnn_sentiment

Par la suite, on doit avoir accès à une page web à l'adresse localhost:5000, sur laquelle on écrit un commentaire dans le champ disponible, qui est classifié comme positif ou négatif.



Cependant, l'étape 'build' ne marche pas correctement. On obtient l'erreur : 
ValueError: Layer 'embedding' expected 1 variables, but received 0 variables during loading. Names of variables received: []

Cette erreur se déroule durant le chargement du modèle, mais celui-ci marche correctement quand il est lu par 

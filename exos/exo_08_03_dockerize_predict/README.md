# Utilisation de Docker avec le TP sur les RNN pour la classification des commentaires IMDB 

Commande pour construire l'image :
docker build -t rnn_sentiment .

Commande pour créer un container de cette image : 
docker run -pd 5000:5000 rnn_sentiment --name server_rnn

Par la suite, on doit avoir accès à une page web à l'adresse localhost:5000, sur laquelle on écrit un commentaire dans le champ disponible, qui est classifié comme positif ou négatif.
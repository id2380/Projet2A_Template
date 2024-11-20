# Bienvenue dans **Cinégram**

Vous êtes passionné(e) de cinéma ? Vous aimez partager vos découvertes sur les réseaux sociaux ? Alors **Cinégram** est fait pour vous !

Avec 181 millions d’entrées au cinéma en France en 2023 et 4,62 milliards d’utilisateurs actifs sur les réseaux sociaux en 2022, il est essentiel de rassembler ces deux univers. **Cinégram** est une plateforme numérique qui réunit les cinéphiles autour du septième art. Découvrez, échangez et partagez vos coups de cœur cinématographiques avec vos proches, tout en révélant le critique en vous.

Grâce à **Cinégram**, vous pouvez :
- Rechercher des films.
- Accéder à des fiches techniques complètes (casting, genre, synopsis, etc.).
- Lire les critiques et notes attribuées par la communauté.
- Partager vos avis avec vos amis cinéphiles (éclaireurs).
- Ajouter vos amis en tant qu'éclaireur.
- Trouver des films similaires.

---

## 🚀 **Démarrage de l'application**

### Étape 1 : Créer un fichier .env 
Avant de commencer à utiliser notre application, il vous faut un fichier .env. Il faut le créer à la racine
du projet et celui-ci doit avoir la forme suivante :

WEBSERVICE_HOST=https://api.themoviedb.org/3
WEBSERVICE_TOKEN=...
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_DATABASE=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_SCHEMA=...
JWT_SECRET=2b5e1b209b27a9b4e04ef8f3a5bcac6a5093d03e9b4925e2f07c5d3b2d7bfa9a

Remplissez les ... par vos informations. Pour le token, utilisez votre token pour l'API Tmdb. 

### Étape 2 : Initialiser la base de données
Lorsque vous exécutez la commande suivante :

`bash : pdm start`

La base de données se charge automatiquement avec des utilisateurs, des films et des avis pré-enregistrés. 

### Étape 2 : Accéder à l'application
Une fois le serveur démarré, ouvrez votre navigateur préféré et accédez à l'application via : (http://localhost:8000/docs)


## 🌟 **Utilisation des endpoints de Cinégram**
Tout les endpoints sont affichés avec leur description afin de vous guider lors de l'utilisation.


## 🎉 **Bon Visionnage et Partage sur Cinégram !** 🍿








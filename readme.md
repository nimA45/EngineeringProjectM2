# AccessTalent

AccessTalent est une application web de gestion des talents. Elle permet aux entreprises de trouver des candidats qualifiés pour leurs postes vacants. Les candidats se connectent et passent leurs tests techniques. Ils sont ensuite notés et corrigés par une intelligence artificielle. Toutes les données sont stockées dans une base de données.

## Installation

### Prérequis

Node.js (version 12 ou supérieure)

Python (version 3.7 ou supérieure)

Créer un fichier .env pour les variables d'environnements avec dedans votre clé API OpenAI et un mot de passe admin :
 
`OPENAI_API_KEY=`

`ADMIN_PASSWORD=123456`

### Backend

Clonez ce dépôt sur votre machine locale : git clone https://github.com/nimA45/Project

Accédez au dossier backend : `cd back`

Installez les dépendances : `pip install -r requirements.txt`

Lancez le serveur : `python main.py`

Le backend devrait être accessible sur http://localhost:5000.

### Frontend

Accédez au dossier frontend : `cd front`

Installez les dépendances : `npm install`

Lancez l'application : `npm run dev`

Le frontend devrait être accessible sur http://127.0.0.1:5173/.

## Release Notes

Version 1.0.0 (31/03/2023)

Fonctionnalités initiales : inscription, connexion, tests techniques, notation par une IA, stockage des données en base de données.

Backend en Python avec FastApi.

Frontend en Svelte avec Picocss.

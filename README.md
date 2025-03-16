# Employment Platform

Bienvenue dans **Employment Platform**, une application backend développée avec Django et Django REST Framework pour automatiser le processus de recrutement. Ce projet permet aux entreprises de publier des offres d’emploi, aux candidats de soumettre leurs CVs, et utilise l’intelligence artificielle pour comparer les CVs aux descriptions de poste, générer des questions d’entretien, et évaluer les réponses textuelles des candidats.

## Fonctionnalités
- **Gestion des utilisateurs** : Inscription, récupération et mise à jour des informations des utilisateurs.
- **Gestion des postes** : Création, listing, mise à jour et suppression des offres d’emploi.
- **Upload de CVs** : Téléversement de fichiers PDF (CVs) pour analyse.
- **Comparaison CV/Poste** : Utilisation de TF-IDF pour évaluer la compatibilité entre un CV et une description de poste.
- **Entretiens virtuels** : Génération de questions avec un modèle T5 et évaluation des réponses avec Sentence Transformers.

## Pré-requis
- Python 3.8+
- Django
- Django REST Framework
- SimpleJWT (authentification JWT)
- Bibliothèques IA : `scikit-learn`, `transformers`, `sentence-transformers`, `PyPDF2`
- Postman (pour tester les endpoints)

### Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/SamraniOuahid/employment-.git
   cd employment-
Créez un environnement virtuel et activez-le :
bash

Réduire

Envelopper

Copier
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate
Installez les dépendances :
bash

Réduire

Envelopper

Copier
pip install -r requirements.txt
Contenu recommandé de requirements.txt :
text

Réduire

Envelopper

Copier
django
djangorestframework
djangorestframework-simplejwt
PyPDF2
scikit-learn
transformers
sentence-transformers
torch
Configurez la base de données :
bash

Réduire

Envelopper

Copier
python manage.py makemigrations
python manage.py migrate
Lancez le serveur :
bash

Réduire

Envelopper

Copier
python manage.py runserver

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



## Routes de l’API

### Authentification
Les endpoints marqués **[Auth]** nécessitent un token JWT dans l’en-tête `Authorization: Bearer <token>` obtenu via `/api/token/`.

#### 1. `POST /api/register/` - Inscription
- **Description** : Crée un nouvel utilisateur.
- **Body** (JSON) :
  ```json
  {
      "username": "testuser",
      "email": "testuser@example.com",
      "password": "testpass123"
  }
Réponse :
json

Réduire

Envelopper

Copier
{
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
}
2. POST /api/token/ - Obtenir un token JWT
Description : Authentifie un utilisateur et retourne un token.
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "username": "testuser",
    "password": "testpass123"
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "refresh": "long_refresh_token",
    "access": "votre_access_token"
}
3. GET /api/current-user/ - Détails de l’utilisateur [Auth]
Description : Récupère les informations de l’utilisateur connecté.
Headers : Authorization: Bearer <token>
Réponse :
json

Réduire

Envelopper

Copier
{
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
}
4. PUT /api/update-user/ - Mise à jour de l’utilisateur [Auth]
Description : Met à jour les informations de l’utilisateur.
Headers : Authorization: Bearer <token>
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "email": "newemail@example.com"
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "id": 1,
    "username": "testuser",
    "email": "newemail@example.com"
}
Gestion des postes
5. POST /post/new/ - Créer un poste [Auth]
Description : Ajoute un nouveau poste d’emploi.
Headers : Authorization: Bearer <token>
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "title": "Développeur Python",
    "description": "Recherche un développeur Python expérimenté.",
    "final_date": "2025-04-01"
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "post": {
        "id": 1,
        "title": "Développeur Python",
        "description": "Recherche un développeur Python expérimenté.",
        "final_date": "2025-04-01",
        "uploaded_at": "2025-03-16T12:00:00Z",
        "user": 1,
        "accepted": false
    }
}
6. GET /post/getAll/ - Lister tous les posts
Description : Retourne tous les postes.
Réponse :
json

Réduire

Envelopper

Copier
{
    "posts": [
        {
            "id": 1,
            "title": "Développeur Python",
            "description": "Recherche un développeur Python expérimenté.",
            "final_date": "2025-04-01",
            "uploaded_at": "2025-03-16T12:00:00Z",
            "user": 1,
            "accepted": false
        }
    ]
}
7. GET /post/get/<id>/ - Récupérer un post
Description : Récupère un poste spécifique par ID.
Exemple : GET /post/get/1/
Réponse :
json

Réduire

Envelopper

Copier
{
    "post": {
        "id": 1,
        "title": "Développeur Python",
        "description": "Recherche un développeur Python expérimenté.",
        "final_date": "2025-04-01",
        "uploaded_at": "2025-03-16T12:00:00Z",
        "user": 1,
        "accepted": false
    }
}
8. PUT /post/update/<id>/ - Mettre à jour un post [Auth]
Description : Modifie un poste existant.
Exemple : PUT /post/update/1/
Headers : Authorization: Bearer <token>
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "title": "Développeur Python Senior",
    "description": "Recherche un développeur Python senior.",
    "final_date": "2025-05-01"
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "post": {
        "id": 1,
        "title": "Développeur Python Senior",
        "description": "Recherche un développeur Python senior.",
        "final_date": "2025-05-01",
        "uploaded_at": "2025-03-16T12:00:00Z",
        "user": 1,
        "accepted": false
    }
}
9. DELETE /post/delete/<id>/ - Supprimer un post [Auth]
Description : Supprime un poste.
Exemple : DELETE /post/delete/1/
Headers : Authorization: Bearer <token>
Réponse :
json

Réduire

Envelopper

Copier
{
    "message": "The post is deleted"
}
Gestion des CVs et entretiens
10. POST /post/upload/ - Uploader un PDF
Description : Ajoute un fichier PDF (par exemple, un CV).
Body (form-data) :
title: "Mon CV" (Text)
pdf_file: sélectionnez un fichier PDF (File)
Réponse :
json

Réduire

Envelopper

Copier
{
    "id": 1,
    "title": "Mon CV",
    "pdf_file": "pdfs/cv.pdf",
    "uploaded_at": "2025-03-16T12:00:00Z"
}
11. POST /post/compare-cv-with-post/ - Comparer un CV avec un poste
Description : Évalue la compatibilité d’un CV avec un poste.
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "cv_id": 1,
    "post_id": 1
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "message": "You are eligible for an interview.",
    "similarity_score": 85.23,
    "next_step": "interview"
}
12. POST /post/interview/ - Générer des questions
Description : Génère des questions d’entretien basées sur un poste.
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "post_id": 1
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "questions": [
        "What experience do you have with Python?",
        "How would you optimize a Python script?"
    ],
    "post_title": "Développeur Python"
}
13. POST /post/submit-interview/ - Soumettre des réponses [Auth]
Description : Enregistre les réponses textuelles d’un entretien.
Headers : Authorization: Bearer <token>
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "post_id": 1,
    "responses": [
        {
            "question": "What experience do you have with Python?",
            "answer": "I have 3 years of experience."
        }
    ]
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "message": "Text responses submitted successfully."
}
14. POST /post/evaluate-responses/ - Évaluer les réponses [Auth]
Description : Évalue les réponses par rapport à la description du poste.
Headers : Authorization: Bearer <token>
Body (JSON) :
json

Réduire

Envelopper

Copier
{
    "post_id": 1,
    "candidate_answers": [
        "I have 3 years of experience with Python.",
        "I optimize scripts using profiling tools."
    ]
}
Réponse :
json

Réduire

Envelopper

Copier
{
    "final_score": 78.45,
    "scores": [82.10, 74.80],
    "post_title": "Développeur Python",
    "message": "Text response evaluation completed."
}
text

Réduire

Envelopper

Copier

---

### Instructions pour l’ajouter à votre dépôt GitHub
1. **Accédez à votre dépôt** :
   - Allez sur `https://github.com/SamraniOuahid/employment-`.

2. **Créez ou mettez à jour `README.md`** :
   - Si `README.md` n’existe pas :
     - Cliquez sur `Create new file`.
     - Nommez-le `README.md`.
   - S’il existe déjà :
     - Cliquez sur `README.md`, puis sur l’icône de crayon (`Edit this file`).
   - Copiez-collez le contenu ci-dessus dans l’éditeur.

3. **Committez les changements** :
   - En bas de la page, entrez un message de commit comme "Ajout de la section Routes de l’API au README".
   - Cliquez sur `Commit new file` ou `Commit changes`.

4. **Vérifiez le rendu** :
   - Retournez à la page principale de votre dépôt (`https://github.com/SamraniOuahid/employment-`) pour voir le `README.md` mis à jour avec une mise en forme Markdown.

---

### Notes
- **Structure** : Cette version inclut uniquement la section "Routes de l’API" comme demandé, avec les sous-sections "Authentification", "Gestion des postes", et "Gestion des CVs et entretiens".
- **Markdown** : Les blocs de code sont entourés de ```json pour un affichage propre sur GitHub.
- **Ajout au dépôt existant** : Si votre `README.md` actuel contient d’autres sections (comme une introduction ou des instructions d’installation), vous pouvez coller ce contenu sous une section existante ou remplacer le fichier entier, selon vos préférences.

Si vous voulez que j’ajoute d’autres sections (par exemple, une introduction ou des instructions d’installation) pour compléter ce `README.md`, dites-le-moi ! Que pensez-vous de cette version ? Prêt à l’ajouter à votre dépôt ?

Voici le contenu formaté en `README.md` :

```markdown
# Employment Platform

Bienvenue dans **Employment Platform**, une application backend développée avec Django et Django REST Framework pour automatiser le processus de recrutement. Ce projet permet aux employeurs de publier des offres d’emploi, aux employés de postuler avec leurs CVs, et utilise l’intelligence artificielle pour comparer les CVs aux postes, générer des questions d’entretien, et évaluer les réponses textuelles.

## Fonctionnalités
- **Gestion des utilisateurs** : Inscription, authentification JWT, mise à jour des informations, suppression de compte (par l’utilisateur ou un admin), rôles (`admin`, `employee`, `employer`).
- **Gestion des postes** : Création, listing, mise à jour, suppression des offres d’emploi avec salaire, et signalement des postes incorrects.
- **Upload de CVs** : Téléversement de fichiers PDF (CVs) pour candidatures et analyse.
- **Candidatures** : Suivi des candidatures avec statut (`en_attente`, `accepte`, `refuse`), CV et entretien associés.
- **Comparaison CV/Poste** : Utilisation de TF-IDF pour évaluer la compatibilité entre un CV et une description de poste.
- **Entretiens virtuels** : Génération de questions avec T5 et évaluation des réponses avec Sentence Transformers.
- **Dashboards personnalisés** :
  - **Admin** : Statistiques globales et signalements.
  - **Employé** : Historique des entretiens et candidatures.
  - **Employeur** : Postes publiés et candidatures reçues.
- **Signalements** : Possibilité de signaler des postes avec des informations incorrectes (ex. : salaire erroné).

## Pré-requis
- Python 3.8+
- Django 5.1.2
- Django REST Framework 3.15.2
- SimpleJWT (authentification JWT)
- Bibliothèques IA : `scikit-learn`, `transformers`, `sentence-transformers`, `PyPDF2`
- Postman (pour tester les endpoints)

### Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/SamraniOuahid/employment-.git
   cd employment-
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

   Contenu de `requirements.txt` :
   ```text
   Django==5.1.2
   djangorestframework==3.15.2
   djangorestframework-simplejwt==5.3.1
   PyJWT==2.9.0
   PyPDF2==3.0.1
   sentence-transformers==3.4.1
   transformers==4.48.1
   scikit-learn==1.6.1
   numpy==2.0.2
   python-dateutil==2.9.0.post0
   pytz==2024.2
   requests==2.32.3
   torch
   ```

4. Configurez la base de données :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Créez un superutilisateur :
   ```bash
   python manage.py createsuperuser
   ```

6. Lancez le serveur :
   ```bash
   python manage.py runserver
   ```

## Routes de l’API

### Authentification
Les endpoints marqués **[Auth]** nécessitent un token JWT dans l’en-tête `Authorization: Bearer <token>` obtenu via `/api/token/`.

1. **POST /api/register/** - Inscription  
   Description : Crée un nouvel utilisateur.  
   Body (JSON) :
   ```json
   {
       "username": "testuser",
       "email": "testuser@example.com",
       "password": "testpass123",
       "role": "employee"
   }
   ```
   Réponse :
   ```json
   {
       "id": 1,
       "username": "testuser",
       "email": "testuser@example.com",
       "role": "employee"
   }
   ```

2. **POST /api/token/** - Obtenir un token JWT  
   Description : Authentifie un utilisateur et retourne un token.  
   Body (JSON) :
   ```json
   {
       "email": "testuser@example.com",
       "password": "testpass123"
   }
   ```
   Réponse :
   ```json
   {
       "refresh": "long_refresh_token",
       "access": "votre_access_token"
   }
   ```

3. **GET /api/current-user/** - Détails de l’utilisateur **[Auth]**  
   Description : Récupère les informations de l’utilisateur connecté.  
   Headers : `Authorization: Bearer <token>`  
   Réponse :
   ```json
   {
       "id": 1,
       "username": "testuser",
       "email": "testuser@example.com",
       "role": "employee"
   }
   ```

4. **PUT /api/update-user/** - Mise à jour de l’utilisateur **[Auth]**  
   Description : Met à jour les informations de l’utilisateur.  
   Headers : `Authorization: Bearer <token>`  
   Body (JSON) :
   ```json
   {
       "email": "newemail@example.com"
   }
   ```
   Réponse :
   ```json
   {
       "id": 1,
       "username": "testuser",
       "email": "newemail@example.com",
       "role": "employee"
   }
   ```

5. **DELETE /api/users/delete/** - Supprimer un utilisateur **[Auth]**  
   Description : Supprime un compte.  
   - **Utilisateur** : Supprime son propre compte (sans paramètre).  
     Headers : `Authorization: Bearer <token>`  
     Exemple : `curl -X DELETE http://localhost:8000/api/users/delete/ -H "Authorization: Bearer <token>"`  
     Réponse : `{"message": "Votre compte a été supprimé avec succès"}`  
   - **Admin** : Supprime un autre compte avec `user_id`.  
     Body (JSON) :
     ```json
     {
         "user_id": "2"
     }
     ```
     Exemple : `curl -X DELETE http://localhost:8000/api/users/delete/ -H "Authorization: Bearer <admin_token>" -d '{"user_id": "2"}'`  
     Réponse : `{"message": "Utilisateur test2@example.com supprimé par l'admin"}`

### Gestion des postes
6. **POST /post/new/** - Créer un poste **[Auth]**  
   Description : Ajoute un nouveau poste (employeur uniquement).  
   Headers : `Authorization: Bearer <token>`  
   Body (JSON) :
   ```json
   {
       "title": "Développeur Python",
       "description": "Recherche un développeur Python expérimenté.",
       "final_date": "2025-04-01",
       "salaire": 10000
   }
   ```
   Réponse :
   ```json
   {
       "post": {
           "id": 1,
           "title": "Développeur Python",
           "description": "Recherche un développeur Python expérimenté.",
           "final_date": "2025-04-01",
           "salaire": "10000.00",
           "uploaded_at": "2025-04-05T12:00:00Z",
           "user": 1,
           "accepted": false
       }
   }
   ```

7. **GET /post/getAll/** - Lister tous les posts  
   Description : Retourne tous les postes.  
   Réponse :
   ```json
   {
       "posts": [
           {
               "id": 1,
               "title": "Développeur Python",
               "description": "Recherche un développeur Python expérimenté.",
               "final_date": "2025-04-01",
               "salaire": "10000.00",
               "uploaded_at": "2025-04-05T12:00:00Z",
               "user": 1,
               "accepted": false
           }
       ]
   }
   ```

8. **GET /post/get/<id>/** - Récupérer un post  
   Description : Récupère un poste spécifique par ID.  
   Exemple : `GET /post/get/1/`  
   Réponse :
   ```json
   {
       "post": {
           "id": 1,
           "title": "Développeur Python",
           "description": "Recherche un développeur Python expérimenté.",
           "final_date": "2025-04-01",
           "salaire": "10000.00",
           "uploaded_at": "2025-04-05T12:00:00Z",
           "user": 1,
           "accepted": false
       }
   }
   ```

9. **PUT /post/update/<id>/** - Mettre à jour un post **[Auth]**  
   Description : Modifie un poste existant (employeur uniquement).  
   Exemple : `PUT /post/update/1/`  
   Headers : `Authorization: Bearer <token>`  
   Body (JSON) :
   ```json
   {
       "title": "Développeur Python Senior",
       "description": "Recherche un développeur Python senior.",
       "final_date": "2025-05-01",
       "salaire": 12000
   }
   ```
   Réponse :
   ```json
   {
       "post": {
           "id": 1,
           "title": "Développeur Python Senior",
           "description": "Recherche un développeur Python senior.",
           "final_date": "2025-05-01",
           "salaire": "12000.00",
           "uploaded_at": "2025-04-05T12:00:00Z",
           "user": 1,
           "accepted": false
       }
   }
   ```

10. **DELETE /post/delete/<id>/** - Supprimer un post **[Auth]**  
    Description : Supprime un poste (employeur uniquement).  
    Exemple : `DELETE /post/delete/1/`  
    Headers : `Authorization: Bearer <token>`  
    Réponse :
    ```json
    {
        "message": "The post is deleted"
    }
    ```

11. **POST /post/apply/** - Postuler à un poste **[Auth]**  
    Description : Soumet une candidature à un poste (employé uniquement).  
    Headers : `Authorization: Bearer <token>`  
    Body (JSON) :
    ```json
    {
        "post_id": "1",
        "cv_id": "1"
    }
    ```
    Réponse :
    ```json
    {
        "application": {
            "post_id": 1,
            "user_id": 2,
            "cv_id": 1,
            "status": "en_attente",
            "application_date": "2025-04-05T12:00:00Z"
        }
    }
    ```

12. **PATCH /post/update-application/** - Mettre à jour une candidature **[Auth]**  
    Description : Modifie le statut d’une candidature (employeur uniquement).  
    Headers : `Authorization: Bearer <token>`  
    Body (JSON) :
    ```json
    {
        "application_id": "1",
        "status": "accepte",
        "interview_id": "1"
    }
    ```
    Réponse :
    ```json
    {
        "application": {
            "id": 1,
            "post_id": 1,
            "user_id": 2,
            "cv_id": 1,
            "interview_id": 1,
            "status": "accepte"
        }
    }
    ```

13. **POST /post/report/** - Signaler un poste **[Auth]**  
    Description : Signale un poste avec des informations incorrectes.  
    Headers : `Authorization: Bearer <token>`  
    Body (JSON) :
    ```json
    {
        "post_id": "1",
        "description": "Salaire incorrect, annoncé 10000 mais offre 5000"
    }
    ```
    Réponse :
    ```json
    {
        "report": {
            "id": 1,
            "post_id": 1,
            "user_id": 2,
            "description": "Salaire incorrect, annoncé 10000 mais offre 5000",
            "reported_at": "2025-04-05T12:00:00Z"
        }
    }
    ```

### Gestion des CVs et entretiens
14. **POST /post/upload/** - Uploader un PDF **[Auth]**  
    Description : Ajoute un fichier PDF (ex. : CV).  
    Headers : `Authorization: Bearer <token>`  
    Body (form-data) :
    ```
    title: "Mon CV" (Text)
    pdf_file: sélectionnez un fichier PDF (File)
    ```
    Réponse :
    ```json
    {
        "id": 1,
        "title": "Mon CV",
        "pdf_file": "cvs/cv.pdf",
        "uploaded_at": "2025-04-05T12:00:00Z"
    }
    ```

15. **POST /post/compare-cv-with-post/** - Comparer un CV avec un poste  
    Description : Évalue la compatibilité d’un CV avec un poste.  
    Body (JSON) :
    ```json
    {
        "cv_id": 1,
        "post_id": 1
    }
    ```
    Réponse :
    ```json
    {
        "message": "You are eligible for an interview.",
        "similarity_score": 85.23,
        "next_step": "interview"
    }
    ```

16. **POST /post/interview/** - Générer des questions  
    Description : Génère des questions d’entretien basées sur un poste.  
    Body (JSON) :
    ```json
    {
        "post_id": 1
    }
    ```
    Réponse :
    ```json
    {
        "questions": [
            "What experience do you have with Python?",
            "How would you optimize a Python script?"
        ],
        "post_title": "Développeur Python"
    }
    ```

17. **POST /post/submit-interview/** - Soumettre des réponses **[Auth]**  
    Description : Enregistre les réponses textuelles d’un entretien.  
    Headers : `Authorization: Bearer <token>`  
    Body (JSON) :
    ```json
    {
        "post_id": 1,
        "responses": [
            {
                "question": "What experience do you have with Python?",
                "answer": "I have 3 years of experience."
            }
        ]
    }
    ```
    Réponse :
    ```json
    {
        "message": "Text responses submitted successfully."
    }
    ```

18. **POST /post/evaluate-responses/** - Évaluer les réponses **[Auth]**  
    Description : Évalue les réponses par rapport au poste.  
    Headers : `Authorization: Bearer <token>`  
    Body (JSON) :
    ```json
    {
        "post_id": 1,
        "candidate_answers": [
            "I have 3 years of experience with Python.",
            "I optimize scripts using profiling tools."
        ]
    }
    ```
    Réponse :
    ```json
    {
        "final_score": 78.45,
        "scores": [82.10, 74.80],
        "post_title": "Développeur Python",
        "message": "Text response evaluation completed."
    }
    ```

19. **GET /api/dashboard-stats/** - Statistiques du tableau de bord **[Auth]**  
    Description : Récupère des statistiques selon le rôle.  
    Headers : `Authorization: Bearer <token>`  
    Réponse :
    - **Admin** :
      ```json
      {
          "users": {"total": 10},
          "posts": {"total": 5, "average_salaire": 8000.00},
          "cvs": {"total": 15},
          "interview_responses": {"total": 20, "average_score": 85.50},
          "applications": {"total": 8, "pending": 5, "accepted": 2},
          "reports": {
              "total": 1,
              "details": [
                  {
                      "id": 1,
                      "post_title": "Développeur Senior",
                      "user_email": "employee@example.com",
                      "description": "Salaire incorrect",
                      "reported_at": "2025-04-05T12:00:00Z"
                  }
              ]
          }
      }
      ```
    - **Employé** :
      ```json
      {
          "interview_history": [
              {
                  "id": 1,
                  "post_title": "Développeur Senior",
                  "question": "Quelle est votre expérience ?",
                  "answer": "3 ans",
                  "score": 85.0,
                  "response_date": "2025-04-05T12:00:00Z"
              }
          ],
          "total_responses": 1,
          "average_score": 85.0,
          "applications": [
              {
                  "post_title": "Développeur Senior",
                  "cv_id": 1,
                  "interview_id": 1,
                  "status": "accepte",
                  "application_date": "2025-04-05T12:00:00Z"
              }
          ]
      }
      ```
    - **Employeur** :
      ```json
      {
          "my_posts": [
              {
                  "id": 1,
                  "title": "Développeur Senior",
                  "salaire": "10000.00",
                  "uploaded_at": "2025-04-05T12:00:00Z"
              }
          ],
          "total_posts": 1,
          "applications": [
              {
                  "id": 1,
                  "post_title": "Développeur Senior",
                  "applicant_email": "employee@example.com",
                  "cv_id": 1,
                  "interview_id": 1,
                  "application_date": "2025-04-05T12:00:00Z",
                  "status": "accepte"
              }
          ],
          "total_applications": 1,
          "pending_applications": 0
      }
      ```
```

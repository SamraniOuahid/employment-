

---

```markdown
# Employment Platform

Bienvenue dans **Employment Platform**, une application backend développée avec Django et Django REST Framework pour automatiser le processus de recrutement. Ce projet permet aux employeurs vérifiés de publier des offres d’emploi approuvées par un admin, aux employés de postuler avec leurs CVs, et utilise l’intelligence artificielle pour comparer les CVs aux postes, générer des questions d’entretien, et évaluer les réponses textuelles.

## Fonctionnalités
- **Gestion des utilisateurs** :
  - Inscription avec rôles (`admin`, `employee`, `employer`) et authentification JWT.
  - Mise à jour et suppression de compte (par l’utilisateur ou un admin).
  - Vérification des employeurs par un admin (`verified`) pour autoriser la création de postes.
- **Gestion des postes** :
  - Création par des employeurs vérifiés uniquement, avec approbation admin (`approved`) avant publication publique.
  - Listing, mise à jour, suppression et signalement des postes.
  - Informations sur l’entreprise (`company_name`, `company_address`, `company_website`) incluses.
- **Upload de CVs** : Téléversement de fichiers PDF pour candidatures et analyse.
- **Candidatures** :
  - Suivi avec statut (`en_attente`, `accepte`, `refuse`), CV et entretien associés.
  - Détails des entretiens (`question`, `answer`, `score`) inclus pour les employeurs.
- **Comparaison CV/Poste** : Évaluation de compatibilité via TF-IDF et similarité cosinus.
- **Entretiens virtuels** :
  - Génération de questions avec Google Flan-T5.
  - Évaluation des réponses avec Sentence Transformers (`all-MiniLM-L6-v2`).
- **Dashboards personnalisés** :
  - **Admin** : Statistiques globales, liste des utilisateurs, signalements.
  - **Employé** : Historique des entretiens et candidatures.
  - **Employeur** : Postes publiés et candidatures avec détails d’entretien.
- **Signalements** : Signalement des postes incorrects (ex. : salaire erroné).

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
Les endpoints marqués **[Auth]** nécessitent un token JWT dans l’en-tête `Authorization: Bearer <token>` obtenu via `/api/token/`. Les endpoints **[Auth, Admin]** sont réservés aux superutilisateurs (`is_superuser=True`).

1. **POST /api/register/** - Inscription
   - **Description** : Crée un utilisateur. Si `role='admin'`, `is_superuser=True`.
   - **Body** :
     ```json
     {
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "password": "pass1234",
         "role": "employer",
         "company_name": "Tech Corp"
     }
     ```
   - **Réponse** :
     ```json
     {
         "detail": "Your account has been registered successfully!"
     }
     ```

2. **POST /api/token/** - Obtenir un token JWT
   - **Body** :
     ```json
     {
         "email": "john@example.com",
         "password": "pass1234"
     }
     ```
   - **Réponse** :
     ```json
     {
         "refresh": "...",
         "access": "..."
     }
     ```

3. **GET /api/current-user/** - Détails de l’utilisateur **[Auth]**
   - **Réponse** :
     ```json
     {
         "id": 1,
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "role": "employer",
         "verified": false,
         "company_name": "Tech Corp"
     }
     ```

4. **PUT /api/update-user/** - Mise à jour de l’utilisateur **[Auth]**
   - **Body** :
     ```json
     {
         "first_name": "Jane",
         "company_name": "New Corp"
     }
     ```
   - **Réponse** : [Détails mis à jour]

5. **DELETE /api/users/delete/** - Supprimer un utilisateur **[Auth]**
   - **Utilisateur** : Supprime son propre compte (sans body).
     - **Réponse** : `{"message": "Votre compte a été supprimé avec succès"}`
   - **Admin** : Supprime un autre compte.
     - **Body** :
       ```json
       {
           "user_id": "2"
       }
       ```
     - **Réponse** : `{"message": "Utilisateur test@example.com supprimé par l'admin"}`

6. **POST /api/verify-user/<user_id>/** - Vérifier un employeur **[Auth, Admin]**
   - **Description** : Définit `verified=True` pour un employeur.
   - **Réponse** :
     ```json
     {
         "message": "L'utilisateur john@example.com a été vérifié avec succès",
         "user": {
             "id": 2,
             "first_name": "John",
             "last_name": "Doe",
             "email": "john@example.com",
             "role": "employer",
             "verified": true,
             "company_name": "Tech Corp"
         }
     }
     ```

### Gestion des postes
7. **POST /post/new/** - Créer un poste **[Auth]**
   - **Description** : Réservé aux employeurs avec `verified=True`.
   - **Body** :
     ```json
     {
         "title": "Développeur Python",
         "description": "Recherche un développeur Python."
     }
     ```
   - **Réponse** :
     ```json
     {
         "post": {
             "id": 1,
             "title": "Développeur Python",
             "description": "Recherche un développeur Python.",
             "final_date": null,
             "salaire": null,
             "uploaded_at": "2025-04-08T12:00:00Z",
             "accepted": false,
             "approved": false,
             "user": {
                 "id": 2,
                 "email": "john@example.com",
                 "role": "employer",
                 "company_name": "Tech Corp",
                 "company_address": null,
                 "company_website": null
             }
         }
     }
     ```
   - **Erreur** (non vérifié) :
     ```json
     {
         "error": "Votre compte doit être vérifié par un admin pour créer des postes"
     }
     ```

8. **GET /post/getAll/** - Lister les postes approuvés
   - **Description** : Retourne uniquement les postes avec `approved=True`.
   - **Réponse** :
     ```json
     {
         "posts": [
             {
                 "id": 1,
                 "title": "Développeur Python",
                 "description": "Recherche un développeur Python.",
                 "final_date": null,
                 "salaire": null,
                 "uploaded_at": "2025-04-08T12:00:00Z",
                 "accepted": false,
                 "approved": true,
                 "user": {
                     "id": 2,
                     "email": "john@example.com",
                     "role": "employer",
                     "company_name": "Tech Corp",
                     "company_address": "123 Tech St",
                     "company_website": "https://techcorp.com"
                 }
             }
         ]
     }
     ```

9. **GET /post/get/<id>/** - Récupérer un poste
   - **Exemple** : `GET /post/get/1/`
   - **Réponse** : [Détails du poste]

10. **PUT /post/update/<id>/** - Mettre à jour un poste **[Auth]**
    - **Body** :
      ```json
      {
          "title": "Développeur Python Senior"
      }
      ```
    - **Réponse** : [Poste mis à jour]

11. **DELETE /post/delete/<id>/** - Supprimer un poste **[Auth]**
    - **Réponse** :
      ```json
      {
          "message": "The post is deleted"
      }
      ```

12. **POST /post/approve-post/<id>/** - Approuver un poste **[Auth, Admin]**
    - **Description** : Définit `approved=True` pour un poste.
    - **Réponse** :
      ```json
      {
          "message": "Le poste 'Développeur Python' a été approuvé avec succès",
          "post": {
              "id": 1,
              "title": "Développeur Python",
              "approved": true,
              "user": {
                  "id": 2,
                  "email": "john@example.com",
                  "role": "employer",
                  "company_name": "Tech Corp"
              }
          }
      }
      ```

13. **POST /post/apply/** - Postuler à un poste **[Auth]**
    - **Body** :
      ```json
      {
          "post_id": "1",
          "cv_id": "1"
      }
      ```
    - **Réponse** :
      ```json
      {
          "application": {
              "post_id": 1,
              "user_id": 3,
              "cv_id": 1,
              "status": "en_attente"
          }
      }
      ```

14. **PATCH /post/update-application/** - Mettre à jour une candidature **[Auth]**
    - **Body** :
      ```json
      {
          "application_id": "1",
          "status": "accepte",
          "interview_id": "1"
      }
      ```
    - **Réponse** :
      ```json
      {
          "application": {
              "id": 1,
              "status": "accepte",
              "interview_id": 1
          }
      }
      ```

15. **POST /post/report/** - Signaler un poste **[Auth]**
    - **Body** :
      ```json
      {
          "post_id": "1",
          "description": "Salaire incorrect"
      }
      ```
    - **Réponse** :
      ```json
      {
          "report": {
              "id": 1,
              "post_id": 1,
              "description": "Salaire incorrect"
          }
      }
      ```

### Gestion des CVs et entretiens
16. **POST /post/upload/** - Uploader un CV **[Auth]**
    - **Body (form-data)** :
      ```
      title: "Mon CV"
      pdf_file: <fichier.pdf>
      ```
    - **Réponse** :
      ```json
      {
          "id": 1,
          "title": "Mon CV",
          "pdf_file": "cvs/cv.pdf"
      }
      ```

17. **POST /post/compare-cv-with-post/** - Comparer un CV avec un poste
    - **Body** :
      ```json
      {
          "cv_id": 1,
          "post_id": 1
      }
      ```
    - **Réponse** :
      ```json
      {
          "similarity_score": 85.23,
          "next_step": "interview"
      }
      ```

18. **POST /post/interview/** - Générer des questions
    - **Body** :
      ```json
      {
          "post_id": 1
      }
      ```
    - **Réponse** :
      ```json
      {
          "questions": [
              "What experience do you have with Python?"
          ]
      }
      ```

19. **POST /post/submit-interview/** - Soumettre des réponses **[Auth]**
    - **Body** :
      ```json
      {
          "post_id": 1,
          "responses": [
              {
                  "question": "What experience do you have with Python?",
                  "answer": "3 years"
              }
          ]
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Text responses submitted successfully."
      }
      ```

20. **POST /post/evaluate-responses/** - Évaluer les réponses **[Auth]**
    - **Body** :
      ```json
      {
          "post_id": 1,
          "candidate_answers": ["3 years"]
      }
      ```
    - **Réponse** :
      ```json
      {
          "final_score": 85.0,
          "scores": [85.0]
      }
      ```

21. **GET /api/interview-data/** - Données des entretiens **[Auth]**
    - **Réponse (Employeur)** :
      ```json
      {
          "total_interviews": 1,
          "interview_data": [
              {
                  "id": 1,
                  "post_title": "Développeur Python",
                  "user_email": "employee@example.com",
                  "question": "What experience do you have with Python?",
                  "answer": "3 years",
                  "score": 85.0
              }
          ]
      }
      ```

22. **GET /api/dashboard-stats/** - Statistiques du tableau de bord **[Auth]**
    - **Réponse (Employeur)** :
      ```json
      {
          "my_posts": [
              {
                  "id": 1,
                  "title": "Développeur Python",
                  "salaire": "10000.00",
                  "uploaded_at": "2025-04-08T12:00:00Z"
              }
          ],
          "total_posts": 1,
          "applications": [
              {
                  "id": 1,
                  "post_title": "Développeur Python",
                  "applicant_email": "employee@example.com",
                  "cv_id": 1,
                  "interview_id": 1,
                  "application_date": "2025-04-08T12:00:00Z",
                  "status": "accepte",
                  "test": {
                      "question": "What experience do you have with Python?",
                      "answer": "3 years",
                      "score": 85.0
                  }
              }
          ],
          "total_applications": 1,
          "pending_applications": 0
      }
      ```
    - **Réponse (Admin)** : Statistiques globales.
    - **Réponse (Employé)** : Historique des entretiens.

## Contribution
1. Forkez le projet.
2. Créez une branche (`git checkout -b feature/nouvelle-fonction`).
3. Commitez vos changements (`git commit -m "Ajout de nouvelle fonction"`).
4. Poussez vers la branche (`git push origin feature/nouvelle-fonction`).
5. Ouvrez une Pull Request.

## Licence
Ce projet est sous licence MIT.
```

---

### Changements par rapport à l’ancien `README.md`
1. **Fonctionnalités mises à jour** :
   - Ajout de la vérification des employeurs (`verified`) et de l’approbation des postes (`approved`).
   - Inclusion des champs `company_name`, `company_address`, `company_website` dans les postes.
   - Ajout du champ `test` (question, answer, score) dans les candidatures pour les employeurs.
2. **Endpoints actualisés** :
   - Ajout de `POST /api/verify-user/<user_id>/` et `POST /post/approve-post/<id>/`.
   - Mise à jour de `POST /post/new/` avec la restriction `verified=True`.
   - Mise à jour de `GET /post/getAll/` pour ne retourner que les postes approuvés.
   - Réponses enrichies avec les nouveaux champs dans `GET /post/getAll/` et `GET /api/dashboard-stats/`.
3. **Clarté** :
   - Descriptions plus précises des restrictions (ex. : "Réservé aux employeurs avec `verified=True`").
   - Exemples de réponses reflétant les modifications (ex. : `approved`, `test`).

Remplacez votre ancien `README.md` par ce nouveau contenu dans votre projet. Testez les endpoints documentés avec Postman pour vous assurer qu’ils correspondent à l’implémentation actuelle. Si vous voulez ajouter d’autres sections (ex. : exemples de configuration, notes spécifiques), dites-le-moi !

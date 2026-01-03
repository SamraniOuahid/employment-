<img width="1920" height="901" alt="image" src="https://github.com/user-attachments/assets/90cca1a9-cc73-4533-a412-e2a6c05a66fb" />


# Employment Platform

Bienvenue dans **Employment Platform**, une application backend développée avec Django et Django REST Framework pour automatiser le processus de recrutement. Ce projet permet aux employeurs vérifiés de publier des offres d’emploi approuvées par un admin, aux employés de postuler avec leurs CVs, et utilise l’intelligence artificielle pour comparer les CVs, générer des questions d’entretien, et évaluer les réponses. Le flux de candidature suit un ordre strict : Comparaison → Sauvegarde Interview → Génération Questions → Soumission Réponses → Évaluation.

## Fonctionnalités
- **Gestion des utilisateurs** : Inscription, mise à jour, suppression, vérification (admin).
- **Gestion des postes** : Création, listing, mise à jour, suppression, signalement.
- **Candidatures** : Flux ordonné avec IA pour comparaison CV/Poste et entretiens virtuels.
- **Dashboards** : Statistiques personnalisées par rôle (admin, employé, employeur), avec `application_id` pour les employés.
- **Tests** : Endpoints testables avec Apidog.

## Pré-requis
- Python 3.8+
- Django 5.1.2
- Django REST Framework 3.15.2
- SimpleJWT (authentification JWT)
- Bibliothèques IA : `scikit-learn`, `transformers`, `sentence-transformers`, `PyPDF2`
- Apidog (pour tester les endpoints)

### Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/SamraniOuahid/employment-.git
   cd employment-
   ```
2. Créez un environnement virtuel :
   ```bash
   python -m venv env
   source env/bin/activate  # Windows : env\Scripts\activate
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

## Tous les Endpoints de l’API

Les endpoints sont organisés par module (`account` et `post`). Chaque endpoint inclut une **explication**, une **méthode**, une **URL**, des **headers** (si nécessaire), un **body** (si applicable), et un **exemple de réponse**. Les endpoints marqués **[Auth]** nécessitent un token JWT dans `Authorization: Bearer <token>` (obtenu via `/api/token/` avec `email` et `password`). Les endpoints **[Auth, Admin]** sont réservés aux superutilisateurs.

---

### Module `account` - Gestion des Utilisateurs

1. **POST /api/register/** - Inscription
   - **Explication** : Crée un nouvel utilisateur avec un rôle (`employee`, `employer`, `admin`). L’email est l’identifiant principal. Si `role='admin'`, l’utilisateur devient superutilisateur.
   - **Headers** : `Content-Type: application/json`
   - **Body** :
     ```json
     {
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "password": "pass1234",
         "role": "employee"
     }
     ```
   - **Réponse** :
     ```json
     {
         "detail": "Votre compte a été enregistré avec succès !"
     }
     ```
   - **Erreur** (email déjà pris) :
     ```json
     {
         "detail": "Cet email est déjà utilisé !"
     }
     ```

2. **DELETE /api/users/delete/** - Supprimer un utilisateur **[Auth]**
   - **Explication** : Permet à un utilisateur de supprimer son compte ou à un admin de supprimer un autre utilisateur.
   - **Headers** : `Authorization: Bearer <token>`
   - **Body (admin uniquement)** :
     ```json
     {
         "user_id": "2"
     }
     ```
   - **Réponse (utilisateur)** :
     ```json
     {
         "message": "Votre compte a été supprimé avec succès"
     }
     ```
   - **Réponse (admin)** :
     ```json
     {
         "message": "Utilisateur test@example.com supprimé par l'admin"
     }
     ```

3. **GET /api/current-user/** - Détails de l’utilisateur connecté **[Auth]**
   - **Explication** : Retourne les informations de l’utilisateur authentifié, identifié par son email.
   - **Headers** : `Authorization: Bearer <token>`
   - **Réponse** :
     ```json
     {
         "id": 1,
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com",
         "role": "employee",
         "verified": false
     }
     ```

4. **PUT /api/update-user/** - Mettre à jour l’utilisateur **[Auth]**
   - **Explication** : Modifie les informations de l’utilisateur connecté (ex. : nom, mot de passe, infos entreprise pour employeurs).
   - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
   - **Body** :
     ```json
     {
         "first_name": "Jane",
         "password": "newpass123"
     }
     ```
   - **Réponse** :
     ```json
     {
         "id": 1,
         "first_name": "Jane",
         "last_name": "Doe",
         "email": "john@example.com",
         "role": "employee",
         "verified": false
     }
     ```

5. **GET /api/dashboard-stats/** - Statistiques du tableau de bord **[Auth]**
   - **Explication** : Fournit des statistiques selon le rôle (admin : globales, employé : personnelles avec `application_id`, employeur : ses postes).
   - **Headers** : `Authorization: Bearer <token>`
   - **Réponse (Employé)** :
     ```json
     {
         "interview_history": [
             {
                 "id": 1,
                 "post_title": "Développeur Python",
                 "question": "What experience do you have?",
                 "answer": "3 years",
                 "score": 90.20
             }
         ],
         "total_responses": 1,
         "average_score": 90.20,
         "applications": [
             {
                 "application_id": 1,
                 "post_title": "Développeur Python",
                 "status": "accepte"
             }
         ]
     }
     ```
   - **Réponse (Employeur)** :
     ```json
     {
         "my_posts": [{"id": 1, "title": "Développeur Python"}],
         "total_posts": 1,
         "applications": [
             {
                 "id": 1,
                 "post_title": "Développeur Python",
                 "applicant_email": "john@example.com",
                 "status": "accepte",
                 "test": {"question": "What experience?", "answer": "3 years", "score": 90.20}
             }
         ]
     }
     ```
   - **Réponse (Admin)** :
     ```json
     {
         "users": {"total": 10},
         "posts": {"total": 5},
         "applications": {"total": 20, "pending": 10}
     }
     ```

6. **POST /api/verify-user/<user_id>/** - Vérifier un employeur **[Auth, Admin]**
   - **Explication** : Définit `verified=True` pour un employeur, lui permettant de créer des postes.
   - **Headers** : `Authorization: Bearer <token>`
   - **URL Exemple** : `/api/verify-user/2/`
   - **Réponse** :
     ```json
     {
         "message": "L'utilisateur john@example.com a été vérifié avec succès",
         "user": {
             "id": 2,
             "email": "john@example.com",
             "role": "employer",
             "verified": true
         }
     }
     ```

---

### Module `post` - Gestion des Postes et Candidatures

7. **POST /post/new/** - Créer un poste **[Auth]**
   - **Explication** : Permet à un employeur vérifié de créer une offre d’emploi.
   - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
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
             "user": {"id": 2, "email": "employer@example.com"}
         }
     }
     ```

8. **GET /post/getAll/** - Lister tous les postes
   - **Explication** : Retourne tous les postes (filtrés par `approved=True` si implémenté).
   - **Réponse** :
     ```json
     {
         "posts": [
             {
                 "id": 1,
                 "title": "Développeur Python",
                 "description": "Recherche un développeur Python."
             }
         ]
     }
     ```

9. **GET /post/get/<pk>/** - Récupérer un poste par ID
   - **Explication** : Retourne les détails d’un poste spécifique.
   - **URL Exemple** : `/post/get/1/`
   - **Réponse** :
     ```json
     {
         "post": {
             "id": 1,
             "title": "Développeur Python",
             "description": "Recherche un développeur Python."
         }
     }
     ```

10. **PUT /post/update/<pk>/** - Mettre à jour un poste **[Auth]**
    - **Explication** : Modifie un poste créé par l’utilisateur connecté.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
    - **URL Exemple** : `/post/update/1/`
    - **Body** :
      ```json
      {
          "title": "Développeur Python Senior"
      }
      ```
    - **Réponse** :
      ```json
      {
          "post": {
              "id": 1,
              "title": "Développeur Python Senior"
          }
      }
      ```

11. **DELETE /post/delete/<pk>/** - Supprimer un poste **[Auth]**
    - **Explication** : Supprime un poste (créateur ou admin uniquement).
    - **Headers** : `Authorization: Bearer <token>`
    - **URL Exemple** : `/post/delete/1/`
    - **Réponse** :
      ```json
      {
          "message": "The post is deleted"
      }
      ```

12. **POST /post/upload/** - Uploader un CV **[Auth]**
    - **Explication** : Permet à un utilisateur de téléverser un CV en PDF.
    - **Headers** : `Authorization: Bearer <token>`
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
          "pdf_file": "pdfs/mon_cv.pdf"
      }
      ```

13. **POST /post/apply/** - Postuler à un poste **[Auth]**
    - **Explication** : Crée une candidature pour un poste avec un CV.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
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

14. **PATCH /post/update-application/** - Mettre à jour le statut d’une candidature **[Auth]**
    - **Explication** : Permet à l’employeur de modifier le statut d’une candidature.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
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
    - **Explication** : Permet de signaler un poste avec une description.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
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

16. **POST /post/compare-cv-with-post/** - Comparer un CV avec un poste **[Auth]**
    - **Explication** : Première étape du flux de candidature, évalue la compatibilité CV/Poste.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
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
          "message": "Votre CV correspond au poste. Prochaine étape : sauvegarde de l'interview.",
          "similarity_score": 75.20,
          "application_id": 1
      }
      ```

17. **POST /post/save-interview/** - Sauvegarder un interview **[Auth]**
    - **Explication** : Crée un entretien pour une candidature (nécessite `step='cv_compared'`). Requiert un utilisateur authentifié via JWT.
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
    - **Body** :
      ```json
      {
          "application_id": 1
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Interview sauvegardé. Cliquez pour commencer.",
          "interview_id": 1
      }
      ```
    - **Erreur** (non authentifié) :
      ```json
      {
          "detail": "Authentication credentials were not provided."
      }
      ```

18. **POST /post/interview/** - Générer des questions **[Auth]**
    - **Explication** : Génère des questions pour l’entretien (nécessite `step='interview_saved'`).
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
    - **Body** :
      ```json
      {
          "application_id": 1
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Questions générées. Soumettez vos réponses.",
          "questions": ["What experience do you have?"],
          "interview_id": 1
      }
      ```

19. **POST /post/submit-interview/** - Soumettre des réponses **[Auth]**
    - **Explication** : Enregistre les réponses de l’entretien (nécessite `step='questions_generated'`).
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
    - **Body** :
      ```json
      {
          "application_id": 1,
          "responses": ["3 years of experience"]
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Réponses soumises. Prochaine étape : évaluation."
      }
      ```

20. **POST /post/evaluate-responses/** - Évaluer les réponses **[Auth]**
    - **Explication** : Évalue les réponses et finalise la candidature (nécessite `step='answers_submitted'`).
    - **Headers** : `Authorization: Bearer <token>`, `Content-Type: application/json`
    - **Body** :
      ```json
      {
          "application_id": 1
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Évaluation terminée.",
          "final_score": 85.50,
          "scores": [85.50]
      }
      ```

21. **GET /post/interview-data/** - Données des entretiens **[Auth]**
    - **Explication** : Retourne les détails des entretiens selon le rôle (admin : tous, employé : personnels, employeur : ses postes).
    - **Headers** : `Authorization: Bearer <token>`
    - **Réponse (Employeur)** :
      ```json
      {
          "total_interviews": 1,
          "interview_data": [
              {
                  "id": 1,
                  "post_title": "Développeur Python",
                  "user_email": "john@example.com",
                  "question": "What experience?",
                  "answer": "3 years",
                  "score": 85.50
              }
          ]
      }
      ```

---

## Tester avec Apidog
1. **Configurer Apidog** :
   - Téléchargez Apidog (https://apidog.com/).
   - Créez une collection "Employment Platform".
   - Ajoutez une variable `TOKEN` dans l’environnement (obtenue via `/api/token/` avec `email` et `password`).
2. **Exemple de Requête** :
   - **Obtenir un Token** :
     - **Méthode** : `POST`
     - **URL** : `http://localhost:8000/api/token/`
     - **Headers** : `Content-Type: application/json`
     - **Body** :
       ```json
       {
           "email": "john@example.com",
           "password": "pass1234"
       }
       ```
     - **Réponse** : `{"refresh": "...", "access": "..."}`
   - **Comparer un CV avec un Poste** :
     - **Méthode** : `POST`
     - **URL** : `http://localhost:8000/post/compare-cv-with-post/`
     - **Headers** : `Authorization: Bearer {{TOKEN}}`, `Content-Type: application/json`
     - **Body** : `{"cv_id": 1, "post_id": 1}`
     - Testez et notez l’`application_id`.
3. **Flux Strict** : Suivez l’ordre des endpoints 16 à 20 avec l’`application_id` retourné.

## Contribution
1. Forkez le projet.
2. Créez une branche (`git checkout -b feature/nouvelle-fonction`).
3. Commitez vos changements (`git commit -m "Ajout de nouvelle fonction"`).
4. Poussez vers la branche (`git push origin feature/nouvelle-fonction`).
5. Ouvrez une Pull Request.

## Licence
Ce projet est sous licence MIT.


---

### Changements Apportés par Rapport à l’Ancien `README.md`

1. **Authentification avec Email** :
   - Suppression de `username` dans `/api/register/` et autres endpoints où il apparaissait (ex. : `/api/current-user/`, `/api/update-user/`).
   - Ajout d’une étape explicite pour obtenir un token avec `/api/token/` utilisant `email` et `password` dans la section "Tester avec Apidog".
   - Descriptions mises à jour pour refléter que l’email est l’identifiant principal.

2. **Ajout de `application_id` dans `/api/dashboard-stats/`** :
   - Dans la réponse pour le rôle `employee`, le champ `applications` inclut désormais `"application_id": 1` au lieu de simplement `"id": 1`, pour plus de clarté et cohérence avec le flux strict.

3. **Autres Ajustements** :
   - Suppression de références obsolètes à `username` dans les exemples de réponses (ex. : `/api/current-user/` ne retourne plus `username`).
   - Ajout d’une note sur l’erreur d’authentification pour `/post/save-interview/` pour rappeler l’importance du token.


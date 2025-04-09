



# Employment Platform

Bienvenue dans **Employment Platform**, une application backend développée avec Django et Django REST Framework pour automatiser le processus de recrutement. Ce projet permet aux employeurs vérifiés de publier des offres d’emploi approuvées par un admin, aux employés de postuler avec leurs CVs, et utilise l’intelligence artificielle pour comparer les CVs aux postes, générer des questions d’entretien, et évaluer les réponses textuelles. Les étapes du processus de candidature sont strictement ordonnées pour garantir une progression logique.

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
  - Étapes strictes : Comparaison CV/Poste → Sauvegarde Interview → Génération Questions → Soumission Réponses → Évaluation.
  - Détails des entretiens (`question`, `answer`, `score`) inclus pour les employeurs.
- **Comparaison CV/Poste** : Évaluation de compatibilité via TF-IDF et similarité cosinus (première étape obligatoire).
- **Entretiens virtuels** :
  - Génération de questions avec Google Flan-T5 (uniquement après sauvegarde de l’interview).
  - Soumission et évaluation des réponses avec Sentence Transformers (`all-MiniLM-L6-v2`) dans un ordre strict.
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
- Apidog (pour tester les endpoints)

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
         "role": "employee"
     }
     ```
   - **Réponse** :
     ```json
     {
         "detail": "Votre compte a été enregistré avec succès !"
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
         "role": "employee",
         "verified": false
     }
     ```

4. **PUT /api/update-user/** - Mise à jour de l’utilisateur **[Auth]**
   - **Body** :
     ```json
     {
         "first_name": "Jane"
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

6. **POST /api/verify-user/<user_id>/** - Vérifier un employeur **[Auth, Admin]**
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

8. **GET /post/getAll/** - Lister les postes approuvés
   - **Réponse** :
     ```json
     {
         "posts": [
             {
                 "id": 1,
                 "title": "Développeur Python",
                 "description": "Recherche un développeur Python.",
                 "approved": true
             }
         ]
     }
     ```

### Processus de Candidature (Ordre Strict)
Les endpoints suivants doivent être appelés dans cet ordre précis avec Apidog. Chaque étape nécessite la réussite de l’étape précédente, contrôlée par le champ `step` dans `PostApplication`.

9. **POST /post/compare-cv-with-post/** - Comparer un CV avec un poste **[Auth]**
   - **Description** : Première étape, crée une candidature si le score > 0.5.
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
   - **Erreur** (score < 0.5) :
     ```json
     {
         "message": "Désolé, votre CV ne correspond pas au poste.",
         "similarity_score": 45.30
     }
     ```

10. **POST /post/save-interview/** - Sauvegarder un interview **[Auth]**
    - **Description** : Crée un entretien lié à la candidature (nécessite `step='cv_compared'`).
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
    - **Erreur** :
      ```json
      {
          "error": "Vous devez d'abord passer la comparaison CV/Poste."
      }
      ```

11. **POST /post/interview/** - Générer des questions **[Auth]**
    - **Description** : Génère des questions (nécessite `step='interview_saved'`).
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
          "questions": [
              "What experience do you have with Python?",
              "How do you handle database optimization?"
          ],
          "interview_id": 1
      }
      ```
    - **Erreur** :
      ```json
      {
          "error": "L'interview doit être sauvegardé avant de commencer."
      }
      ```

12. **POST /post/submit-interview/** - Soumettre des réponses **[Auth]**
    - **Description** : Enregistre les réponses (nécessite `step='questions_generated'`).
    - **Body** :
      ```json
      {
          "application_id": 1,
          "responses": [
              "I have 3 years of experience with Python.",
              "I optimize databases using indexing."
          ]
      }
      ```
    - **Réponse** :
      ```json
      {
          "message": "Réponses soumises. Prochaine étape : évaluation."
      }
      ```
    - **Erreur** :
      ```json
      {
          "error": "Les questions doivent être générées avant de soumettre des réponses."
      }
      ```

13. **POST /post/evaluate-responses/** - Évaluer les réponses **[Auth]**
    - **Description** : Évalue les réponses et finalise (nécessite `step='answers_submitted'`).
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
          "scores": [90.20, 80.30]
      }
      ```
    - **Erreur** :
      ```json
      {
          "error": "Les réponses doivent être soumises avant l'évaluation."
      }
      ```

14. **GET /api/dashboard-stats/** - Statistiques du tableau de bord **[Auth]**
    - **Réponse (Employé)** :
      ```json
      {
          "interview_history": [
              {
                  "id": 1,
                  "post_title": "Développeur Python",
                  "question": "What experience do you have with Python?",
                  "answer": "3 years",
                  "score": 90.20
              }
          ],
          "applications": [
              {
                  "post_title": "Développeur Python",
                  "status": "accepte",
                  "application_date": "2025-04-09T12:00:00Z"
              }
          ]
      }
      ```

## Tester avec Apidog
1. **Configurer Apidog** :
   - Téléchargez Apidog (https://apidog.com/) ou utilisez la version web.
   - Créez une nouvelle collection nommée "Employment Flow".
   - Ajoutez un environnement avec la variable `TOKEN` (valeur obtenue via `/api/token/`).

2. **Exemple de Requête dans Apidog** :
   - **Nom** : "Compare CV with Post"
   - **Méthode** : `POST`
   - **URL** : `http://localhost:8000/post/compare-cv-with-post/`
   - **Headers** :
     ```
     Content-Type: application/json
     Authorization: Bearer {{TOKEN}}
     ```
   - **Body** :
     ```json
     {
         "cv_id": 1,
         "post_id": 1
     }
     ```
   - Sauvegardez et testez avec "Send".

3. **Flux Complet** :
   - Créez une requête pour chaque endpoint dans l’ordre : `/compare-cv-with-post/`, `/save-interview/`, `/interview/`, `/submit-interview/`, `/evaluate-responses/`.
   - Utilisez l'`application_id` retourné par la première étape dans les requêtes suivantes.
   - Vérifiez les réponses pour confirmer la progression.

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
1. **Mise à jour des Fonctionnalités** :
   - Ajout de l’ordre strict des étapes dans "Candidatures" avec référence au champ `step`.
   - Suppression des endpoints redondants ou non nécessaires (ex. : `/post/apply/`) pour se concentrer sur le nouveau flux.

2. **Endpoints Réorganisés** :
   - Ajout de `/post/save-interview/` comme nouvelle étape explicite.
   - Mise à jour des descriptions et exemples pour refléter l’ordre strict et les vérifications (ex. : "nécessite `step='cv_compared'`").
   - Réponses mises à jour avec `application_id` et messages spécifiques.

3. **Section Apidog** :
   - Ajout d’une section dédiée à l’utilisation d’Apidog pour tester le flux.
   - Instructions pour configurer les requêtes avec headers et body.

4. **Simplification** :
   - Suppression des endpoints non pertinents dans ce contexte (ex. : `/post/update-application/`) pour éviter la confusion.
   - Focus sur le flux principal demandé.

---

### Instructions
- Remplace ton ancien `README.md` par celui-ci dans ton projet.
- Teste chaque endpoint avec Apidog comme décrit dans la section "Tester avec Apidog" pour valider que le flux fonctionne comme prévu.
- Si tu veux ajouter des détails supplémentaires (ex. : captures d’écran d’Apidog, autres endpoints), fais-le-moi savoir !

Ce README est maintenant aligné avec ta demande d’un flux ordonné et testé via Apidog.

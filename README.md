# Projet de Création de CV avec Django

## Description
Ce projet est une application web développée avec Django permettant aux utilisateurs de créer, personnaliser et télécharger leurs CV au format PDF. Les CV sont sauvegardés dans une base de données pour une récupération et une modification ultérieures.

## Fonctionnalités
- **Création et personnalisation de CV** via un formulaire interactif.
- **Téléchargement en PDF** pour une utilisation facile.
- **Base de données des CV** permettant de sauvegarder les informations.
- **Interface simple et intuitive** pour une meilleure expérience utilisateur.

## Installation
### Prérequis
- Python (>= 3.8)
- Django (>= 4.0)
- Virtualenv (optionnel mais recommandé)

### Étapes d'installation
1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-repo.git
   cd nom-du-repo
   ```
2. **Créer un environnement virtuel et l'activer** (optionnel mais recommandé)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```
5. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```
6. **Accéder à l'application**
   Ouvrir [http://127.0.0.1:8000](http://127.0.0.1:8000) dans votre navigateur.

## Technologies utilisées
- **Backend** : Django
- **Frontend** : HTML, CSS
- **Base de données** : SQLite (par défaut, peut être remplacé par PostgreSQL/MySQL)
- **Génération PDF** : Bibliothèque `WeasyPrint`

## Contribution
Les contributions sont les bienvenues ! Pour toute modification, veuillez forker le projet et soumettre une pull request.

## Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier.

---
**Auteur** : [Sedera](https://github.com/votre-utilisateur)

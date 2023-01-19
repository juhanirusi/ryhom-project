# Project Architecture

The project architecture is meant to **(MOSTLY)** comply with the structure laid out in the *Two Scoops Of Django* book. According to the book, the reason to lay out the project this way is to make it look easier for developers and non-developers and even though I made this project myself, this structure makes it easier for other team members to work together in a same project.

```python
# STRUCTURE OF THE "ryhom-project" PROJECT

ryhom-project
config/ # --> The config root where we store the project-wide settings.
    settings/
    __init__.py
    .env # --> The .env file where you place your sensitive data like Django SECRET_KEY (YOU NEED TO CREATE IT YOURSELF!)
    asgi.py
    urls.py
    wsgi.py
docs/ # -> Project documentation for developers.
ryhom/
    accounts/ # --> App for managing and displaying user accounts.
    articles/ # --> App for managing and displaying articles and comments in them
    categories/ # --> App for managing and displaying categories used in articles and microposts
    core/ # --> App for placing any functionality or code that's too general in other apps
    media/ # --> Development only media file!
    microposts/ # --> App for managing and displaying microposts and comments in them
    static/ # --> Files for static media assets like CSS, JavaScript etc.
    tags/ # --> App for managing and displaying tags used in articles and microposts
    templates/ # --> Contains the site-wide Django templates.
manage.py
requirements.txt # --> A list of Python packages required by the project
```
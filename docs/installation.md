# How To Install `ryhom-project` Into Your Own Device?

In order to install and make `ryhom-project` work on your own device, you need to do the following:


1. Fork the repo and clone the project into your own local machine


2. Open the project and create a virtual environment, so that the Python packages we'll install will live inside the virtual environment

    - You create the virtual environment by opening the terminal of your IDE, and typing the `pip` command `python -m venv .venv` into the terminal and running it. This should create a `.venv` folder into your parent folder structure!


3. Make sure that the virtual environment has been activated correctly by closing the current terminal and opening it again...

    - Now, you should see the terminal show your project structure in a similar manner as this --> `(.venv) PS C:\Users\YourUsername\Folder\Folder\GitHub\ryhom-project>`. If it does, you have installed the virtual environment successfully


4. Next, install the packages the project needs to work properly by running the pip command `pip install -r requirements.txt` in your terminal window.

    - Now, the packages should be installed (including Django), but if you aren't sure, run the pip command `pip freeze` to see what packages are currently installed and compare that to the insides of the `requirements.txt` file.

    - You can also make sure that Django has been installed properly by passing the pip command `django-admin --version` into the terminal. This should show the currently installed Django version number.


5. After you've made sure that Django is properly installed, create a database with PostgreSQL, give the database a name and your desired password. Write them down, if you can't remember them.


6. Create an account at [MailTrap.io](https://mailtrap.io/home) and create a free email testing inbox that we're going to use for receiving emails.


7. Check out the `SMPT Settings` -> `SMPT` section at your newly created email testing inbox in [MailTrap.io](https://mailtrap.io/home) and take note of these values in the SMPT section:

- host
- username
- password


8. Next, paste the template below into your newly created `.env` file and fill the variables with your personal info...


```python
# Django
SECRET_KEY='' # Insert your desired Django project's specific 50 character secret key
DEBUG=True # LEAVE THIS AS IT IS
IS_ADMIN_ENABLED=True # LEAVE THIS AS IT IS

# PostgreSQL
DATABASE_NAME=''
DATABASE_USER=''
DATABASE_PASSWORD=''
DATABASE_HOST=''
DATABASE_PORT=

# Email Testing (Mailtrap.io)
EMAIL_PORT=
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
```


9. Next, after you've filled the `.env` file with the correct inputs, let's create the database so that we can run our program, by opening the IDE terminal and writing the command `python manage.py makemigrations` into the terminal and running it.

    - When you run it, the terminal should show you a big list of tables it'll create into your PostgreSQL database, if it doesn't, make sure that the PostgreSQL configurations in your `.env` file are correct!


10. Then, run the command `python manage.py migrate` in the terminal to create the tables into your database.


11. After creating the database, let's create a superuser (an admin) into our project, which we can use to control the Django admin UI. To create the superuser, run the command `python manage.py createsuperuser` and input your personal info that the IDE asks.


12. Lastly, we can run the command `python manage.py runserver` and if all goes well, the IDE should tell us that the development server was started at a "http://127.0.0.1:8000/"
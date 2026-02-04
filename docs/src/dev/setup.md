# Getting Started

## Prerequisites

You need [uv](https://docs.astral.sh/uv/getting-started/installation/),
the Python package/version/virtual environment manager.
If you don't already have it, recommend installing it using `pipx`:

```bash
pipx install uv
```


(`pipx` installs packages as tools in their own virtual environment, [link if you don't already have it.](https://pipx.pypa.io/latest/installation/))

## Installation

Clone the repo to your computer:

```bash
git clone git@github.com:Gaia-COB/gaia-cob-pmp
```

Then enter the directory, and copy the default environment file `.env.default`:

```bash
cd gaia-cob-pmp
cp .env.default .env
```

Initialise the virtual environment and install the development prerequisites into it.
Then set up the database and load the demo data:

```bash
uv venv
source .venv/bin/activate
make develop
make setup
```

You can now run the server with:

```bash
make server
```

Go to `http://localhost:8000`, and look around.

In order to sign in, you'll need to register the app with Google's OAuth. Follow the process in the [AllAuth docs](https://docs.allauth.org/en/latest/socialaccount/providers/google.html):

1. Create a new Google OAuth client.
2. Add the **client ID** and **secret** to your `.env` file.
3. Add `http://localhost` and `http://localhost:8000` to the OAuth client as authorised JavaScript origins and redirect URIs.
4. Restart the server.

Once you've signed in, you can register your account as a superuser:

```bash
djmanage makestaff your_email@gmail.com --superuser
```

(This is just a shortcut to `python manage.py` from the correct directory)

Now you have access to the admin interface, and can manually view and edit things.

## Deployment

Installing the package for deployment is also fairly straightforward, and just requires Docker.
Clone the code to the server, and copy the environment file.

```shell
cd /var/www/
git clone https://github.com/Gaia-COB/gaia-cob-pmp
cd gaia-cob-pmp
cp .env.default .env
```

Then:
* Add your OAuth client details to `.env`.
* [Create a `SECRET_KEY`](https://humberto.io/blog/tldr-generate-django-secret-key/), and add it to `.env`. 
* Make sure debug mode is off.

Then build and launch the server:

```shell
screen
sudo docker compose up
[ctrl-a, ctrl-d]
```

You can't run a deployment in debug mode! It will fail (if you *want* to, you can change the Dockerfile to allow it).
View the logs for a running deployment with `docker compose logs web` or `nginx` as appropriate.

Finally, install the fixtures as a one-off command: 

```
sudo docker exec -it gaia-cob-pmp-web /bin/bash
uv run manage.py loaddata app/fixtures/*.json
exit
```

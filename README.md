# Gaia Compact Object Binaries: Proposal Management Platform

Demo project for the Iommi web framework

[![Build Status](https://github.com/smangham/iommi-demo/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/smangham/iommi-demo/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/smangham/iommi-demo/branch/main/graph/badge.svg)](https://codecov.io/gh/smangham/iommi-demo)
[![License](https://img.shields.io/github/license/smangham/iommi-demo)](https://github.com/smangham/iommi-demo)

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

Then enter the directory, and copy the template environment file `.env.example`:

```bash
cd gaia-cob-pmp
cp .env.example .env
```

Initialise the virtual environment and install the development prerequisites into it.
Then set up the database and load the demo data:

```bash
uv venv
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
1. Add the **client ID** and **secret** to your `.env` file.
1. Add `http://localhost` and `http://localhost:8000` to the OAuth client as authorised JavaScript origins and redirect URIs.
1. Restart the server.

Once you've signed in, you can register your account as a superuser:

```bash
djmanage makestaff your_email@gmail.com --superuser
```

(This is just a shortcut to `python manage.py` from the correct directory)

Now you have access to the admin interface, and can manually view and edit things.

## Development

The template I've used has linting/code style fixing built in. Check out `Makefile`;
`make fix-py` will run the `ruff` code formatter over your code.
Run it before committing and fix/flag as ignored anything it can't fix itself.

## Introduction

This uses Iommi, a very powerful and flexible framework for building websites in Python.
[The documentation is here](https://docs.iommi.rocks/), but it can be a bit hard to get your head around.
[The cookbook pages](https://docs.iommi.rocks/cookbook.html) are a good thing to refer to.

Examples are good as well, so I'll just outline a few key concepts to understand the code:

### Two Ways of Doing Anything

There's basically two ways of doing anything - **procedural** and **declarative**.
Example - building a form to edit a specific instance of a model, **procedurally**:

```python
view = Form(
    auto__model=MyDjangoModel,
    instance=lambda params, **_: params.my_django_model
)
```

and **declaratively**, where the `class Meta` is basically just what you'd give as arguments:

```python
class MyForm(Form):
    class Meta:
        auto__model=MyDjangoModel
        instance=lambda params, **_: params.my_django_model
        
view = MyForm()
```

In this example, the stuff in `app.main_menu.py` is mostly **procedural**,
and there's an example of a more complicated view in `app.pages.py` (that gets included into `main_menu`).

### Refinables

Everything is built out of 'refinables'. For example, `Form` has some settings for automatically generating it from a model.
Example - Building a form to edit *only* the name and height of \`MyDjangoModel:

```python
Form(
    auto=dict{
        model=MyDjangoModel
        include=['name', 'height']
    }
)
```

But you can also skip providing the dict of options with just double underscores:

```python
Form(
    auto__model=MyDjangoModel,
    auto__include=['name', 'height']
)
```

Anything not specified will have its default value.

### Function Arguments

A lot of arguments can be provided as functions that evaluate at runtime.
Example - Building a form that's only editable if you're staff:

```python
Form(
    editable=lambda user, **_: user.is_staff
)
```

```python
class MyForm(Form):
    class Meta:
        editable=lambda user, **_: user.is_staff
```

If you need the functions to be more complicated, then in the **procedural** frame you can declare them elsewhere.
Example - Making a form editable only by Steve. Needs to make sure the user is signed in, so they *have* a name to check.

```python
def staff_and_steve(user) -> bool:
    if not user.is_authenticated:
        return False
    else if user.is_staff and user.first_name == 'Steve':
        return True 
    return False

view = Form(
    editable=lambda user, **_: staff_and_steve(user)
)
```

Or declaratively:

```python
class MyForm(Form):
    class Meta:
        @staticmethod
        def editable(user, **_) -> bool:
            if not user.is_authenticated:
                return False
            else if user.is_staff and user.first_name == 'Steve':
                return True 
            return False

view = MyForm()
```

### Function Argument Parameters

The functions are passed a set of parameters. The values available vary, but it's generally `request`,
`params` (which contains any view parameters), `user` (a shortcut to `request.user`) and any you've specified using
**path decoding** (where you register a model, and then paths containing it put it in the context).
See `app.apps.AppConfig` and `app.main_menu -> cats.items.detail`.

## Rules

The app has object-level permissions, applied using [django-rules](https://github.com/dfunckt/django-rules).
These are defined for each model in the model files, after the model itself.

They fit pretty well into Iommi's structure, so it's easy to check when setting up a URL or whatever
if you're allowed to view/edit/whatever the object.

## Overview

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).

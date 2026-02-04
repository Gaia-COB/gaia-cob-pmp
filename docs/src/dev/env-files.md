# Environment Files

The platform settings are configured in a `.env` file.
A default one is provided - `.env.defaults`, which needs copying to an `.env` in the same folder.
If you want to use the default value of a setting, you can delete the entry in your `.env` file, 
but this is only really possible for the `[aladin]` keys.

The file is split into sections, though these are not 'functional', just for convenience:

## [settings]

General, site-wide settings:

* `URL`: The URL it will be deployed at, if you're not running it locally (e.g. `gaia-cob.soton.ac.uk`).
  * **Optional:** You can omit it if running locally. 
* `SECRET_KEY`: The 'secret key' for any cryptographic operations [(see Django docs)](https://docs.djangoproject.com/en/6.0/topics/signing/).
  * **Optional:** You *can* omit it and it'll generate a new one each time it restarts.
* `DEBUG`: Whether to enable the Django debug mode, `true` or `false`. 
  * Must be *`false`* on web-accessible deployments. 

## [allauth]

Specific to the user account authentication library [django-allauth](https://docs.allauth.org/en/latest/).

You'll need to register the app with Google's OAuth. 
Follow the process in the [AllAuth docs](https://docs.allauth.org/en/latest/socialaccount/providers/google.html):

1. Create a new Google OAuth client.
2. Fill in `GOOGLE_OUATH2_CLIENT_ID` and `GOOGLE_OAUTH2_CLIENT_SECRET` as appropriate.
3. Add `http://localhost` and `http://localhost:8000` to the OAuth client as authorised JavaScript origins and redirect URIs
   (or whatever your deployment URL is, if you're not doing it locally).

## [aladin]

Settings related to the [Aladin Lite](https://aladin.cds.unistra.fr/) sky maps:

* `ALADIN_DEFAULT_FOV`: The default 'field of view' around a target object in degrees, defaults to `0.2`. 
* `ALADIN_DEFAULT_SURVEY`: The background survey image shown, defaults to `P/DSS2/color` [(options)](https://aladin.cds.unistra.fr/hips/list).

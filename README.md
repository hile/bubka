
Bubka REST API CLI
==================

This tool is intended for manually using django rest framework APIs with DRF static TOKEN or
JWT token authentication. Nothing fancy but slightly useful.

Command line client 'bubka' can be used to:

* get REST APIs listings and details for a resource
* create records with POST
* update records with PUT
* delete records with DELETE

Obviously the client libraries are designed to be used from code as well, the CLI is just
a small wrapper around bubka.session commands.

Environment variable for static DRF token
-----------------------------------------

To use the CLI with a DRF static authentication token, set environment variabble
DJANGO_REST_API_STATIC_TOKE.

```
export DJANGO_REST_API_STATIC_TOKEN=6def9e631880d1f59b226571ceb5efc69d8dc1f1
```

Environment variables for generic authorization header token
------------------------------------------------------------

To use the CLI with other authorization header tokens, set environment variable
REST_AUTH_STATIC_TOKEN. This will send the token as-is in Authorization header.

If your application requires a token name you can also set REST_AUTH_TOKEN_NAME
which will cause the header to be sent with named token.

Example:

```
REST_AUTH_TOKEN_NAME='Auth'
REST_AUTH_STATIC_TOKEN='NotReally'
```

This sends Authorization header with value 'Auth: NotReally'.

Using JWT authentication
------------------------

There is code to obtain and verify JWT token in bubka.session.jwt_token_auth. This
has not yet been integrated to the command line tool, but when done, you can store the
currently valid JWT token to environment variable REST_API_JWT_AUTHENTICATION_TOKEN to
used the token with the CLI command.

Example commands
----------------

Following commands show example usage for the command line tool.

```
bubka create --file data.json http://localhost:8000/api/endpoint
bubka update --file data.json http://localhost:8000/api/endpoint/12345
bubka get http://localhost:8000/api/endpoint
bubka get http://localhost:8000/api/endpoint/12345
bubka delete http://localhost:8000/api/endpoint/12345
```

You can post other data than JSON as well, see --help for all these commands, for example:

```
bubka create --help
```

Name of project
---------------

Named after obscure Finnish reference to long snooker cue rest that got it's nickname from
pole vaulter Sergei Bubka.

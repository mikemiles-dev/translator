# translator
Language Translation API

# Description
HTTP Langugage Translation API.  Currently uses redis to persist translations.

# Requirments

Python 3.7+ (https://www.python.org/downloads/)
Docker 18+ (https://docs.docker.com/engine/install/ubuntu/)

# Build Dev

Build pip dependencies dev

```
make build-dev
```

# Build Production

Build pip dependencies production

```
make build
```

# Running Development Mode

```
make run HOST=<host ip or 0.0.0.0>
```

# Running Production Deployment

<Todo>

# Routes

Translate a word (HTTP GET REQUEST):

```
/translate/<from langugage>/<to language>/<word to translate>
```

for example:
```
/translate/english/spanish/library/
```

yields:
```
{"translation": "bibliotheca"}
```

Add new translation (HTTP POST REQUEST):
```
/translate/<from langugage>/<to language>/<word to translate>/<translation>

```

Delete translation (HTTP DELETE REQUEST):
```
/translate/<from langugage>/<to language>/<word to translate>/

```

# Tests

To run unit tests:

```
make test
```

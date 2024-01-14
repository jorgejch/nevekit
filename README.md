# New Eve Kit

[![tests](https://github.com/jorgejch/nevekit/actions/workflows/python-test.yml/badge.svg)](https://github.com/jorgejch/nevekit/actions/workflows/python-test.yml) [![codecov](https://codecov.io/gh/jorgejch/nevekit/graph/badge.svg?token=8OFRYTH59M)](https://codecov.io/gh/jorgejch/nevekit) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/063df9d27de14dbbbe27fa984c57d77c)](https://app.codacy.com/gh/jorgejch/nevekit/dashboard?utm_source=gh\&utm_medium=referral\&utm_content=\&utm_campaign=Badge_grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=jorgejch_nevekit\&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=jorgejch_nevekit)

## Description

A new Eve Kit Python 3 library to work with CCP's ESI Swagger API, SDE, Image Server and Fuzzworks data.

## Project Status

The project is at it's inception phase. Great moment to throw in your 2cs.

Also, for the most part, do something like this in your head.

```bash
sed -i 's/offers/will offer/g' README.md
sed -i 's/can/would be/g' README.md
```

### Contributing

A great start is dropping a "hi!" in this new [Discussions](https://github.com/jorgejch/nevekit/discussions/2) thing.

## Features

* The kit offers a simple interface to access the CCP's image server.
* The kit offers a simple interface to access the Eve Online's ESI.
* The kit offers a simple interface to access the Eve Online's dedicated service Fuzzworks' most useful data.
* Uses the Bravado library to handle the ESI.
  * The ESI definition can be found at: <https://esi.evetech.net/_latest/swagger.json>.
* ESI Market data is fetched synchronously or in asynchronous batches.
* The kit encapsulates the SDE data and provides a simple interface to access it.
  * The SDE data is fetched from a SQLite database.
  * The SDE data ready to restore can be downloaded from: <https://www.fuzzwork.co.uk/dump/>.

## Installation

The kit can be installed from Pypi using pip:

```bash
pip install nevekit
```

## Usage

### Image Server

```python
from nevekit.image import ImageServer

# Create an image server instance.
# By default it uses the following image server base URL: https://images.evetech.net/.
image_server = ImageServer()

# Save character id's 2114008190 portrait at size 256 to a file.
#     - The image server returns a PNG image.
#     - It can provide everything described in https://developers.eveonline.com/blog/article/from-image-server-to-a-whole-new-image-service-1:
#         - Character portraits.
#         - Corporation logos.
#         - Alliance logos.
#         - Type icons.
#         - Type renders.
with open('portrait.png', 'wb') as f:
    f.write(image_server.get_character_portrait(2114008190, 256))
```

### SSO

```python
from nevekit.esi.sso import SSO

# Create an SSO instance.
# By default it uses the following SSO base URL: https://login.eveonline.com/.
# It executes the flow described in the example at https://github.com/esi/esi-docs/blob/master/examples/python/sso/esi_oauth_native.py to get an access token.
# TODO: Review the scopes.
# It uses the following scopes: esi-contracts.read_corporation_contracts.v1, esi-contracts.read_character_contracts.v1.
sso = SSO()

# Authenticate a character and get an access token.
# You'll be redirected to the Eve Online's SSO login page.
# After logging in, you'll be redirected to the callback URL.
# The callback URL must be registered in the Eve Online's SSO application.
# You don't need to keep the token returned, it's stored in the SSO instance.
access_token = sso.login('client_id', 'secret_key', 'callback_url')

# Get the authenticated character's id.
character_id = sso.get_character_id()
```

### ESI

#### Public ESI

```python
from nevekit.esi import ESI
from nevekit.sso import SSO

# Create an ESI instance w/o authentication.
# By default it uses the following ESI base URL: https://esi.evetech.net/.
esi = ESI()
```

#### Authenticated ESI

```python
from nevekit.esi import ESI
from nevekit.esi.sso import SSO

# Create an ESI instance with authentication.
# By default it uses the following ESI base URL: https://esi.evetech.net/.
# It uses the access token stored in the SSO instance.
sso = SSO()
sso.login('client_id', 'secret_key', 'callback_url')
esi = ESI(sso=sso)

# Get the authenticated character's standings.
# It uses the following ESI endpoint: /characters/{character_id}/standings/.
standings = esi.get_character_standings()
```

### SDE

```python
from nevekit.sde import SDE

# Create an SDE instance.
# By default it creates a SQLite database at ~/.nevekit/nevekit.db.
sde = SDE()

# Get the type with id 587.
type_obj = sde.get_type(587)
```

### Fuzzworks

```python
from nevekit.fuzzworks import Fuzzworks

# Create a Fuzzworks instance.
# By default it uses the following Fuzzworks base URL: https://www.fuzzwork.co.uk/.
fuzzworks = Fuzzworks()

# Get the SQLite db dump of the Eve Online's SDE.
# This uses the following Fuzzworks endpoint: /dump/sqlite-latest.sqlite.bz2.
fuzzworks.get_sde_dump(db_type='sqlite')
```

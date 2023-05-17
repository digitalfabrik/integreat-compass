# Integreat Compass

This is a Django 4 based web application, a project powered by [Tür an Tür – Digitalfabrik gGmbH](https://tuerantuer.de/digitalfabrik/). The main goal is to develop an application that gathers courses that job center employees can pass on in counseling sessions to refugees and newcomers.

## TL;DR

### Prerequisites

Following packages are required before installing the project (install them with your package manager):

* `npm` version 7 or later
* `nodejs` version 12 or later
* `python3` version 3.9 or later
* `python3-pip` (Debian-based distributions) / `python-pip` (Arch-based distributions)
* `python3-venv` (only on Debian-based distributions)
* Either `postgresql` **or** `docker` to run a local database server

### Installation

````
git clone git@github.com:digitalfabrik/integreat-compass.git
cd integreat-compass
./tools/install.sh
````

### Run development server

````
./tools/run.sh
````

* Go to your browser and open the URL `http://localhost:8082`
* By default, the following users exist:

| Email                                     | Group                  |
|-------------------------------------------|------------------------|
| root@integreat.compass                    | -                      |
| board_member@integreat.compass            | BOARD_MEMBER           |
| integration_specialist@integreat.compass  | INTEGRATION_SPECIALIST |
| offer_provider@integreat.compass          | OFFER_PROVIDER         |

All default users share the password `compass`.

## Project Architecture / Reference


- [Integreat compass](integreat_compasss): The main package of the integreat-compass with the following sub-packages:
  - coming soon
- [Tests](tests): This app contains all tests to verify integreat-compass works as intended


## License

This project is licensed under the Apache 2.0 License, see [LICENSE.txt](./LICENSE.txt)

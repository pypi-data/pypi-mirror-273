# alfetcher

A simple library to help you fetch data from AniList

## Description

Welcome to my first python project!
This library is aimed at people who might be interested in automatizing their anime library.

## Getting Started

### Dependencies

* Python(tested on the latest ver.)
* An AniList account
* An AniList developer app
* Javascript enabled during the set-up process (for sending the access token back to Python)

### Installing

* Clone this repo
```
git clone https://github.com/ProchyGaming/alfetcher /path/to/desired/folder
```
* Install it using pip
```
pip install alfetcher
```
* Install it using pip locally
```
cd /path/to/desired/folder
pip install .
```
* If you want to make modifications to the library install it in the edit mode:
```
cd /path/to/desired/folder
pip install -e .
```

### Using the library

* To import the library into your code use:
```
import alhelper
```
* When importing this library for the first time, you will be taken through the setup process

### Setting up the AniList developer app

* When the setup process starts, you will be automatically taken to required pages. This process is really simple.
* When asked for the Client ID, you will be taken to the account developer page.
* If not logged in, log in first.
* Then create a new client
* Choose whatever name you fancy, and for the redirect URL use http://localhost:8888/auth
* After you save the client, copy the ID and paste it into the terminal
* After entering the ID you will be taken to an auth page, where you need to allow the app to access your account.
* Afterwards you will be taken to a redirect page that is momentarily hosted using gevent. (If you have any worries, please see the token_getter.html source code.)
* After that the library is successfully set-up and ready for use.

## Help

If you encounter any issues, feel free to open a new issue. If you have any new ideas or fixes, please open a pull request, they are more than welcome!

## Version History
* [1.1.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.1.0)
    * [fix typo](https://github.com/prochy-exe/alfetcher/commit/dbf3d14e90c4cfeebcef51503a884efd1e1178b5)
    * [allow some functions to not require user token](https://github.com/prochy-exe/alfetcher/commit/f3e58106709d5b1626b65384977fe22a05c7d647)
    * [use local ip address instead of localhost](https://github.com/prochy-exe/alfetcher/commit/9d6500229980faf68b20fe4a559a8d2bc08fed1b)
    * [print list name when no anime found](https://github.com/prochy-exe/alfetcher/commit/efca221b8f78ac0848aaa7d8813b6b5c36e89c28)
    * [drop user list caching](https://github.com/prochy-exe/alfetcher/commit/954fe02ef643e228561a2c3e845e18b431947652)
    * [add function to update progress in users list](https://github.com/prochy-exe/alfetcher/commit/c040d8836efb44352dd2f1339305cb9c5296f97d)
    * [add function to convert from al to mal id](https://github.com/prochy-exe/alfetcher/commit/278805356c25dcabb4029b01e337c40f83b135ac)
    * [dates: Make sure they are not None](https://github.com/prochy-exe/alfetcher/commit/92db92773cea64ec7e8c8f12bcf4bc624c2400b2)
    * [Formatting changes](https://github.com/prochy-exe/alfetcher/commit/b4a96be729ab23cff87fe00c2e0deab7d6b742f7)
* [1.0.0](https://github.com/prochy-exe/alfetcher/releases/tag/v1.0.0)
    * [Initial Release](https://github.com/prochy-exe/alfetcher/commit/4b67b1d8719d183012446a065c5b6c941ec6518e)

## Acknowledgments

Huge thanks to AniList team for their great page and database:
* [AniList](https://anilist.co/home)
* [AniList GraphQL](https://anilist.co/graphiql)

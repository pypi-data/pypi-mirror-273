# malfetcher

A simple library to help you fetch data from MyAnimeList

## Description
This library is aimed at people who might be interested in automatizing their anime library.

## Getting Started

### Dependencies

* Python(tested on the latest ver.)
* A MyAnimeList account
* A MyAnimeList developer app

### Installing

* Clone this repo
```
git clone https://github.com/prochy-exe/malfetcher /path/to/desired/folder
```
* Install it using pip
```
pip install malfetcher
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
import malhelper
```
* When importing this library for the first time, you will be taken through the setup process

### Setting up the MyAnilist developer app

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
* [1.1](https://github.com/prochy-exe/malfetcher/releases/tag/v1.1.0)
    * [fix typo](https://github.com/prochy-exe/malfetcher/commit/ec8fa79befc1a4190667639920f3b6bd736340f1)
    * [allow some functions to not require user token](https://github.com/prochy-exe/malfetcher/commit/2a3b8c4229984caf7e383072eb5e06af0208c3e3)
    * [use local ip address instead of localhost](https://github.com/prochy-exe/malfetcher/commit/ccb7bfff7d136e9be0204509f18f1646185b5e2c)
    * [print list name when no anime found](https://github.com/prochy-exe/malfetcher/commit/7888e5d7d7100f8e9952210ddbed6705b5dc393b)
    * [drop user list caching](https://github.com/prochy-exe/malfetcher/commit/dd5933434945759bbab8a2fd06ce0511b1ff435e)
    * [allow the mal_to_al_id function to be imported easily](https://github.com/prochy-exe/malfetcher/commit/fbf23bfd384ac53d68dbbe7960d12efa29d88b11)
    * [add function to update progress in users list](https://github.com/prochy-exe/malfetcher/commit/e8fa1dd20054c68f81be4133a9414daa4aad8b29)
    * [regenerate token when expired](https://github.com/prochy-exe/malfetcher/commit/af326c5693fec00c8c90286d63d81782fb90932f)
    * [add state to requests](https://github.com/prochy-exe/malfetcher/commit/76a3e27031ef88d5ba84d7816802647ae55a9e84)
    * [rotate useragents in hopes to avoid captcha](https://github.com/prochy-exe/malfetcher/commit/15ef5a3e866b64cb287264d70946602aa50dea82)
    * [fetch unreleased info all the time](https://github.com/prochy-exe/malfetcher/commit/15d8723dab29a67f0b55f903f8195a47bced6253)
    * [make sure we have a day in the dates](https://github.com/prochy-exe/malfetcher/commit/6ceea01d96ec190b85e0d3950f84a861aa464a73)
    * [Formatting changes](https://github.com/prochy-exe/malfetcher/commit/d06303c44837bc75f788fb29e510dad645c9e801)
* [1.0](https://github.com/prochy-exe/malfetcher/releases/tag/v1.0.0)
    * [Initial Release](https://github.com/prochy-exe/malfetcher/commit/2d356310fbe00143c50ffe14596532a7cd30e8db)

## Acknowledgments
* [MyAnimeList](https://myanimelist.net)

# miniserver

A simple server in Python which adds some functionality I commonly need, mainly for security testing. 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

Miniserver 

- Minimal requirements, does not depend on Flask etc.
- Option to serve a custom index page, or display the content of the running directory
- Accepts POST requests, can be disabled if you wish
- Writes the content of POST requests to idividual timestamped files in the "data" folder
- Includes some helpful logging in the terminal
- Saves log messages to server.log, in the "log" folder.
- Binds to any port you have permission to use
- Uses only the python3 standard library

## Installation

Clone the repo, run the file, nice and easy :D

```bash
$ git clone https://github.com/duck-sec/Simple-Practice-Test-Question-App
$ cd Simple-Practice-Test-Question-App
$ python3 ./miniserver.py
```

## Usage

The content of post requests will be saved in the "Data" folder. Your server logs are in "Log"

```bash
usage: miniserver.py [-h] [-sf] [-dp] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -sf, --servefiles     Serve files in the directory miniserver runs in - Defaults to False
  -dp, --disablepost    Disable server accepting POST requests
  -p PORT, --port PORT  Port to listen on - Defaults to 8000 - False by default
```

```bash
$python miniserver.py -p 8080
[LOG] Starting the server on port 8080. Press Ctrl+C to stop.
127.0.0.1 - - [03/Nov/2023 13:03:11] "GET / HTTP/1.1" 200 -
[LOG] GET request received from 127.0.0.1 for /
127.0.0.1 - - [03/Nov/2023 13:03:11] "GET /favicon.ico HTTP/1.1" 404 -
[LOG] [ERROR] GET request received for /favicon.ico - 404 Not Found.
127.0.0.1 - - [03/Nov/2023 13:03:31] "GET /doesnotexist HTTP/1.1" 404 -
[LOG] [ERROR] GET request received for /doesnotexist - 404 Not Found.
127.0.0.1 - - [03/Nov/2023 13:03:48] "POST / HTTP/1.1" 200 -
[LOG] POST request received from 127.0.0.1 and saved to file: data/127.0.0.1_03-11-2023@13:03:48.txt
127.0.0.1 - - [03/Nov/2023 13:04:01] "GET / HTTP/1.1" 200 -
[LOG] GET request received from 127.0.0.1 for /
```



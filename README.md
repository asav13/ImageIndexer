#Image Indexer
Author: asabj88@gmail.com<br>
A miniproject that lets a user create and store an image indexer, and then browse through it via a web UI.

##Layers
This project consists of three layers:
- A python application that scans through a file system and generates an index of all images
- A AngularJS web UI application that allows a user to browse through the index
- A NodeJS web API which the two applications use to communicate through

### Image Indexer python application
The python script ImageIndexer.py walks through the file system, and gathers information 
about all images it finds. This information is then posted to an API by default, however 
there is an option to save it to a local .json file

Usage:
optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        the directory to search for images in, if not set, the
                        whole file system will be scanned
  -l LOCAL, --local LOCAL
                        an option to save the index locally, takes one parameter:
                        destination for file

### NodeJS web API 
A very simple NodeJS web API that handles communication between the two applications.
An API was used instead of for example a local file, so that the two applications could perhaps, 
if needed, communicate over the internet between different hosts. The API uses sqlite3 to store the data, 
and implements two RESTful methods: GET and POST to /api/images

### AngularJS WEB UI
An AngularJS web application fetches the image index from the API and displays it in a table.
It provides a search utility in the form of filters.

## Run the application - step-by-step guide
1. If you don't have either Python3 or NodeJS installed, make
sure to download them first:
	- https://www.python.org/downloads/
	- https://nodejs.org/en/download/

2. Go to ImageIndexer\back-end\API and run
```
node ImageIndexerApi.js
```
NB: You might have to run ```npm install``` first, even though
the dependancies are provided in the zip file.

This starts the API web server locally.

3. Go to ImageIndexer\back-end\indexer and run
```
py ImageIndexer.py
```
to scan the whole file system, or 
```
py ImageIndexer.py -s <path>
```
to scan a given location.

Now the image indexer should have been posted to the API.

4. Go to ImageIndexer\web-UI and run
```
py -m http.server 8080
```

NB: You might have to run ```npm install``` first, even though
the dependancies are provided

This will start the web UI application on localhost:8080

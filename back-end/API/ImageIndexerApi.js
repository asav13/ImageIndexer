/**
 * Author: Asa Bjork Valdimarsdottir - asabj88@gmail.com
 * Since:  Jun 8th 2016
 */
'use strict'

/* Dependencies */
const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

/* The app */
const app = express();
const port = 4000;
app.use(bodyParser.json());

/* Database variables, the database, set when the app starts listening
   for connections */
var db = null;
var properties = ['filename', 'path', 'format', 'width', 'height',
				'bytes', 'created', 'accessed' , 'modified'];

/**
 * Returns all images, as a list of JSON objects
 */
app.get('/images', (req, res) => {
	var images = [];
	res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8080');

	db.all("SELECT * from Images", function(err,rows){
		res.status(200).send(rows);
	});
});

/*
 * Adds images to the database
 */
app.post('/images', (req, res) => {
	var data = req.body;

	db.serialize(function() {
		db.run("CREATE TABLE IF NOT EXISTS Images " 
			+ "(filename TEXT, path TEXT, format TEXT, width TEXT, "
			+ "height TEXT, bytes TEXT, created TEXT, accessed TEXT, modified TEXT)");

		var statement = db.prepare("INSERT INTO Images VALUES (?,?,?,?,?,?,?,?,?)");
		for (var i = 0; i < data.length; i++) {
			var curr = data[i];
			
			for(var j = 0; j < properties.length; j++){
				if(!curr.hasOwnProperty(properties[j])){
					res.status(412).send("Image object is missing '" + properties[j] + "' field.");
					return;
				}
			}

			statement.run(curr['filename'], curr['path'], curr['format'], curr['width'], 
					curr['height'], curr['bytes'], curr['created'], curr['accessed'], curr['modified']);
		}
		statement.finalize();

		res.status(201).send(data);; // 200 OK 
	});
});

/**
 * Initializing database, binding to port and listening for requests
 */
app.listen(port, () => {
	db = new sqlite3.Database(':memory:');
	console.log('Server is listening on', port);
});
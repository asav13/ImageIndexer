/**
 * Author: Asa Bjork Valdimarsdottir - asabj88@gmail.com
 * Since:  Jun 7th 2016
**/
'use strict';

const API_URL = "http://localhost:4000/images";

angular.module("ImageIndexerProject").controller("ImageController",
function ImageController($scope, $http) {

	$scope.getDataFromAPI = function getDataFromAPI(){
		$scope.data = [];

		$http.get(API_URL).then(function success(response){

			var data 		= response.data;
			var imageList 	= [];

			for(var i = 0; i < data.length; i++) {

				var location = data[i]['path'].slice(0, data[i]['path'].length - data[i]['filename'].length);
				var kb 		 = (parseInt(data[i]['bytes']) / 1000).toString() + " KB";

				var curr = {
					'filename': data[i]['filename'],
					'path': 	data[i]['path'],
					'format': 	data[i]['format'],
					'size': 	kb,
					'location': location,
					'created': 	data[i]['created']
				};

				imageList.push(curr);
			}
			$scope.data = imageList;
			}, function error(response){
				console.log("ERROR: Error while fetching data.\n" +
							"-Please check if the server you are trying to connect to is running");
		});
	}
	$scope.getDataFromAPI();
})
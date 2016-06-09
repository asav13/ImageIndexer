/**
 * Author: Asa Bjork Valdimarsdottir - asabj88@gmail.com
 * Since:  Jun 7th 2016
**/

'use strict';

angular.module("ImageIndexerProject", ["ngRoute"])
.config(function ($routeProvider) {

	$routeProvider.when("/", {
		controller: 	"ImageController",
		templateUrl: 	"/src/images/index.html"
	});
})
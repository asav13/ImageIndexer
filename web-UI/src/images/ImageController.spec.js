/**
 * Author: Asa Bjork Valdimarsdottir - asabj88@gmail.com
 * Since:  Jun 8th 2016
**/

'use strict';

describe("ImageController unit tests, true behaviour.", function(){

	var imageController, scope;

	beforeEach(module("ImageIndexerProject"));

	/* Inject: Get access */
	beforeEach(inject(function($controller, $rootScope){

		scope = $rootScope.$new();

		imageController = $controller("ImageController", { 
			$scope: 		scope
		});
	}));

	it("imageController and scope should be defined before we start testing", function(){
		expect(imageController).toBeDefined();
		expect(scope).toBeDefined();
	});

	/* TEST for valid input */
	it("Once the app starts data should be fetched and set to scope.data", function(){
		expect(scope.data).toBeDefined();
	});

})
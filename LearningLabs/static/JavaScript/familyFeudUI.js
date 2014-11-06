function AppController($http,$scope) {
	
	$http({method: 'GET', url: '/loadFamilyFeudGameData'}).
	success(function(data, status, headers, config) {
     	$scope.question = data.question;
     	$scope.currentQuestion = data.currentQuestion;
     	$scope.answers = data.gameData;
     	$scope.quizId = data.quizId;
    }).
    error(function(data, status, headers, config) {
      // log error
      alert(data);
    });
  
	$scope.loadNextQuestion=function(){
		$http({method: 'GET', params:{'quizId':$scope.quizId, 'questionId':$scope.currentQuestion, 'isNext':1}, url: '/loadFamilyFeudGameData'}).
		success(function(data, status, headers, config) {
			if (data.question != undefined) {
	     	$scope.question = data.question;
	     	$scope.currentQuestion = data.currentQuestion;
	     	$scope.answers = data.gameData;
	     	$scope.quizId = data.quizId;
	     	} else {
	     		 alert(data);
	     	}
	    }).
	    error(function(data, status, headers, config) {
	      // log error
	      alert(data);
	    });
  
	
	};
	/*
	$scope.loadPreviousQuestion=function(){
		if($scope.currentQuestion>0){
			$scope.currentQuestion = $scope.currentQuestion - 1;
			$scope.question = questions[$scope.currentQuestion]; 
			$scope.answers = answers[$scope.currentQuestion];
		}
		else{
			
		}
	};*/
}



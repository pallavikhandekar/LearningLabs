function AppController($http,$scope) {
	
	$http({method: 'GET', url: '/loadFamilyFeudGameData'}).
	success(function(data, status, headers, config) {
		if(data.questions!=undefined){
			$scope.questions =  data.questions; //Global variables
			$scope.gameData =  data.gameData;//Global variables
			$scope.quizId = data.quizId;//Global variables
			
			//Load 1st page
			$scope.currentQuestion = 0; //counter for questions
     		$scope.question = $scope.questions[$scope.currentQuestion];
     		$scope.answers = $scope.gameData[$scope.currentQuestion];
     	}else{
     		 alert(data);
     	}
    }).
    error(function(data, status, headers, config) {
      // log error
      alert(data);
    });
  
	$scope.loadNextQuestion=function(){
  		if (($scope.currentQuestion + 1) <  $scope.questions.length){
  			$scope.currentQuestion = $scope.currentQuestion+1; //counter for questions
		    $scope.question = $scope.questions[$scope.currentQuestion];
     		$scope.answers = $scope.gameData[$scope.currentQuestion];
  		}else{
  			alert("End of Quiz");
  		}
  		
	};

	$scope.loadPreviousQuestion=function(){
		if($scope.currentQuestion>0){
			$scope.currentQuestion = $scope.currentQuestion - 1;
			$scope.question =  $scope.questions[$scope.currentQuestion]; 
			$scope.answers = $scope.gameData[$scope.currentQuestion];
		}
		else{
			
		}
	};
}



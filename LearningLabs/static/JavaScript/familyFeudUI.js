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
     			
	//hide all divs
	
	 $("#divQuizResults").hide();
	 $("#divWrongAnswer").hide();
	 $("#divActionButtons").hide();
     		 displayError("Application Error",data,"no-close error");
     		 errorDig.dialog( "open" );
     	}
    }).
    error(function(data, status, headers, config) {
    	
	//hide all divs
	
	 $("#divQuizResults").hide();
	 $("#divWrongAnswer").hide();
	 $("#divActionButtons").hide();
     displayError("Response Error",data,"no-close error");
     errorDig.dialog( "open" );
    });
  
	$scope.loadNextQuestion=function(){
  		if (($scope.currentQuestion + 1) <  $scope.questions.length){
  			$scope.currentQuestion = $scope.currentQuestion+1; //counter for questions
		    $scope.question = $scope.questions[$scope.currentQuestion];
     		$scope.answers = $scope.gameData[$scope.currentQuestion];
     		resetWrongOptions()
  		}else{
  			displayError("Message","End of Quiz","no-close teamScore");
  			errorDig.dialog( "open" );
  		}
  		
	};

	$scope.loadPreviousQuestion=function(){
		if($scope.currentQuestion>0){
			$scope.currentQuestion = $scope.currentQuestion - 1;
			$scope.question =  $scope.questions[$scope.currentQuestion]; 
			$scope.answers = $scope.gameData[$scope.currentQuestion];
			resetWrongOptions();
		}
		else{
			
		}
	};
	
	$scope.viewScores=function(){
	
	 $http({method: 'GET', url: '/loadFamilyFeudScores'}).
	 success(function(data, status, headers, config) {

	 	$("#teamAScores").text(data.gameScores.Team1Score);
	 	$("#teamBScores").text(data.gameScores.Team2Score);

	 	dialog = $("#dialog").dialog({
		autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
	    title: "Team Scores",
	    hide:"puff",
        buttons: [{
         		text:"Ok",
         		click: function() {
         		 dialog.dialog( "close" );
        		}
     	 }],
      	close: function() {
       	
      	},
      	dialogClass:"no-close teamScore"
        });
      
      	dialog.dialog( "open" );
	
	  }).
	  error(function(data, status, headers, config) {
	 	console.log(data);
	  })
	 
	};
	
	
	$scope.playSound = function(){
		chimeSound.play();
	};
	
	//Error Popup
	function displayError(title,data, cssClass){
	$("#lblResponse").text(data);
		 
      errorDig = $("#divError").dialog({
		autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
	    title: title,
        buttons: [{
         		text:"Ok",
         		click: function() {
         		 errorDig.dialog( "close" );
        		}
     	 }],
      	close: function() {
       	
      	},
      	dialogClass:cssClass
        });
     
      
	}
	
	function resetWrongOptions(){
		wrongCounter = 1;
		$(imgCross1).css({'visibility':"hidden"});
		$(imgCross2).css({'visibility':"hidden"});
		$(imgCross3).css({'visibility':"hidden"});
	}
}



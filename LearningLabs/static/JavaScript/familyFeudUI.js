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
	
	$scope.viewScores=function(){
	/*
			var width = 300; //popup width
			var height = 300;//popup height
			var left = (screen.width/2)-(width/2);
  			var top = (screen.height/2)-(height/2);
		
			newwindow=window.open("/displayScores",'name','left='+left+',top='+top+', height='+height+', width='+width);
			if (window.focus) {newwindow.focus()}
				return false;
	
		*/
		
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
      	dialogClass:"no-close ui-dialog-titlebar"
        });
      
      	dialog.dialog( "open" );
	
	};
}



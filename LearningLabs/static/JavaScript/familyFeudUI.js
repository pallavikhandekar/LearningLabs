function AppController($scope) {
	$scope.question = questions[0]; 
	$scope.answers = answers[0];
	$scope.currentQuestion = 0;
	$scope.loadNextQuestion=function(){
		if($scope.currentQuestion+1<questions.length){
		    $scope.currentQuestion = $scope.currentQuestion + 1;
			$scope.question = questions[$scope.currentQuestion]; 
			$scope.answers = answers[$scope.currentQuestion];
		}
		else{
			confirm("End of Quiz");
		}
	};
	
	$scope.loadPreviousQuestion=function(){
		if($scope.currentQuestion>0){
			$scope.currentQuestion = $scope.currentQuestion - 1;
			$scope.question = questions[$scope.currentQuestion]; 
			$scope.answers = answers[$scope.currentQuestion];
		}
		else{
			
		}
	};
}



var questions = [{ text: "Other than Java, what Programming Languages do you use?" },
{ text: "The main patterns in MVC are?" }];
var answers = [[
{ text: 'C', optionNumber:"1", percentage:'40'},
{ text: 'C++', optionNumber:"2", percentage:'30'},
{ text: 'JavaScript', optionNumber:"3",percentage:'14'},
{ text: 'Python', optionNumber:"4", percentage:'11'},
{ text: 'Objective-C', optionNumber:"5", percentage:'5'}], 
[
{ text: 'Observer, Composite & Strategy', optionNumber:"1", percentage:'75'},
{ text: 'Observer & Decorator', optionNumber:"2", percentage:'20'},
{ text: 'Observer, Strategy & Command', optionNumber:"3",percentage:'3'},
{ text: 'Observer, Strategy & Command', optionNumber:"4",percentage:'2'},
{ text: 'Observer', optionNumber:"5",percentage:'1'}
]
];
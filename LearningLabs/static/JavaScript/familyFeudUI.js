function AppController($scope) {
	$scope.question = question; 
	$scope.answers = answers;
}



var question = { text: "Other than Java, what Programming Languages do you use?" };
var answers = [
{ text: 'C', optionNumber:"1", percentage:'40'},
{ text: 'C++', optionNumber:"2", percentage:'30'},
{ text: 'JavaScript', optionNumber:"3",percentage:'14'},
{ text: 'Python', optionNumber:"4", percentage:'11'},
{ text: 'Objective-C', optionNumber:"5", percentage:'5'}];
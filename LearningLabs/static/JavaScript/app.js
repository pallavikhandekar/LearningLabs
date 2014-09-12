/**
 * Created by nimmicv on 9/11/14.
 */

(function() {
    var app = angular.module('application', []);

    app.controller('QuizMe',function(){
        this.quizQns = [
        {
            quizNo : 1,
            questions : ["Other than Java, what Programming Languages do you use?",
               "The main patterns in MVC are?"]
        },
         {
            quizNo : 2,
            questions : ["Main Concept of Object-Oriented Programming?",
                    "What is Cloud Computing?"
                ]
        }
    ];
        this.quizzes = [1,2,3];
    });

    app.controller('QuizController',function(){
    this.quiz={};

    this.addme = function(){

        this.quiz ={};
    };
    });

    app.controller('TabController',function(){
        this.tab=1;

        this.setTab = function(setTab){
            this.tab= setTab;
        };

        this.isSelected = function(checkTab)
        {
            return this.tab == checkTab;
        }
    });
})();

/**
 * Created by nimmicv on 9/12/14.
 */

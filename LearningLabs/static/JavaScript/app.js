/**
 * Created by nimmicv on 9/11/14.
 */

(function() {
    var app = angular.module('application', []);
    app.controller('QuizMe',function(){
        this.quizzes = [];
    });

    app.controller('QuizController',function(){
    this.quiz={};
    this.addme = function(){

        this.quiz ={};
    };
    });
})();

/**
 * Created by nimmicv on 9/12/14.
 */

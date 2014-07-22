/**
 * Created by nimmicv on 7/21/14.
 */
$(document).ready(function() {
    alert("Hi");
    setInterval( refresh, 5000 );

  });

$(":button").click(function(){
    setInterval('alert("Hello")', 5000);
 });

function teller(){
    alert("Hellonz");
}

function refresh() {
    $.ajax({
        type:"GET",
        url: 'countpolls',
        success: function(data) {
            document.getElementById("counter").value = "Counter :: " + data.count; //adding an extra #result div to wrap #table
        }


    });
}

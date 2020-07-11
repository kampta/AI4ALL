// ----- custom js ----- //

// hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();

// global
var data = [];

$(function() {

  // sanity check
  console.log( "ready!" );

  // image click
  $("#upload-form" ).submit(function(event) {

    event.preventDefault();
    console.log( "submitted!" );

    var fd = new FormData($("#upload-form")[0]);
    fd.append('api', 'demo');

    // empty/hide results
    $("#results").empty();
    $("#results-table").hide();
    $("#error").hide();
    $("#no-results").hide();

    // show searching text
    $("#searching").show();
    console.log("searching...")

    // ajax request
    $.ajax({
      type: "POST",
      url: "/predict",
      data : fd,
      contentType: false,
      cache: false,
      processData: false,
      
      // handle success
      success: function(result) {
        console.log(result.results);
        data = result.results

        $("#searching").hide();
        if (data.length>0) {
          // show table
          $("#results-table").show();
          // loop through results, append to dom
          for (i = 0; i < data.length; i++) {
            $("#results").append('<tr><td>'+data[i]['label']+'</td><td>'+data[i]['score']+'</td></tr>')
          };
        }
        else {
          $("#no-results").show();
        }
        $("#upload-form").trigger("reset");
      },

      // handle error
      error: function(error) {
        console.log(error);
        // append to dom
        $("#error").show()
      }
    });

  });

});
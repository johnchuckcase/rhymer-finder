$(document).ready(function() {

    $("#lyric-input").blur(function() {
        var lyric = ($(this).val());
        var words = lyric.split(' ');

        $("#block-space").html("");
        for (i = 0; i < words.length; i++){
            $("#block-space").append('<div class="word">' + words[i] + '</div>');
        };

        $(".word").hover(
          function(){
          $(this).addClass('hvr-pulse');
        },
        function(){
          $(this).removeClass('hvr-pulse');
        });

        $(".word").click(function() {
          var word_to_rhyme = $(this).text();
          console.log(word_to_rhyme);
          //make ajax call with word
          //    $.ajax(word).success(function {
          //clear old words if the exist and display new rhyming words
          //    $('#rhymes-space').empty();
          // });

          URLString = '/rhyme?word_to_rhyme=' + word_to_rhyme + '&words=' + String(words)
          console.log(URLString);
          $.ajax({
          	type: 'GET',
          	url: URLString
          })
          .success( function(response) {
          	// empty the place where you are displaying rhyming words
          	// split up list of rhyming words and display them
            rhymes = response['Rhymes'];
            sims = response['Cos-sim'];

            $("#rhymes-space").html("");
            for (i = 0; i < rhymes.length; i++){
              // console.log(rhymes[i] + '  ' + sims[i]);
              // console.log(sims[i]);

                $("#rhymes-space").append('<div class="rhyme">' + rhymes[i] + '  ' + sims[i] + '</div>');
            };


          });

        });
    });

});

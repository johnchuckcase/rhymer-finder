$(document).ready(function() {
    $("#lyric-input").blur(function() {
        var lyric = ($(this).val());
        var words = lyric.split(' ');


        for (i = 0; i < words.length; i++){
            $("#block-space").append('<div class="word">' + words[i] + '</div>');
        };

        $(".word").click(function() {
          var word_to_rhyme = $(this).text();
          console.log(word_to_rhyme);
          //make ajax call with word
          //    $.ajax(word).success(function {
          //clear old words if the exist and display new rhyming words
          //    $('#rhymes-space').empty();
          // });

          $.ajax({
          	type: 'GET',
          	url: '/rhyme',
            data: {word_to_rhyme: word_to_rhyme}
          })
          .success( function(response) {
          	// empty the place where you are displaying rhyming words
          	// split up list of rhyming words and display them
            console.log(response);
          })

        });
    });

});

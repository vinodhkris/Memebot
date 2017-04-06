(function($){

    $(document).ready(function(){
        $('#search').bind('submit', function() {
            terms = $('#terms').val();
            actors = $('#actors').val();
            default_path = $('#defaultpath').val();
            URL = "http://localhost:5000/main/api/v1.0/memes?text="+terms+"&actor="+ actors;

            $('#results').empty();
            $('<p></p>').text('Searching for '+terms+' and ' + actors).appendTo('#results');

            $.ajax({
                url: URL,
                success: function(data) {
                    if (data) {
                        $('#results').empty();
                        result = jQuery.parseJSON( data );
                        for (var i = 0; i < result.length; i++){
                            var obj = result[i];
                            $('<ol>').appendTo('#results');
                            if (default_path != "") {
                                $("#results").append('<li><a href="'+default_path+"/"+obj['image_name']+'"><span class="tab">'+obj['image_name']+'</span></a></li>');
                            } else {
                                $('<li></li>').text('Image:'+obj['image_name']).appendTo('#results');
                            }
                            $('<li></li>').text('Actors:'+obj['actor']).appendTo('#results');
                            $('<li></li>').text('Description:'+obj['description']).appendTo('#results');
                            $('</ol>').appendTo('#results'); 
                        }
                    } else {
                        $('#results').empty();
                    }
                }
            });

            return false;
        })
    });

})(jQuery);
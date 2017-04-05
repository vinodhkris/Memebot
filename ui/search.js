(function($){

    $(document).ready(function(){
        $('#search').bind('submit', function() {
            terms = $('#terms').val();
            actors = $('#actors').val();
            etsyURL = "http://localhost:5000/main/api/v1.0/memes?text="+terms+"&actor="+ actors;

            $('#results').empty();
            $('<p></p>').text('Searching for '+terms+' and ' + actors).appendTo('#results');

            $.ajax({
                url: etsyURL,
                success: function(data) {
                    if (data) {
                        //console.log(data);
                        $('#results').empty();
                        result = jQuery.parseJSON( data );
                        for (var i = 0; i < result.length; i++){
                            var obj = result[i];
                            for (var key in obj){
                                if (key == "description") {
                                    $('<p></p>').text('description:'+obj[key]).appendTo('#results');
                                }
                            }
                        }
                        
                                //$('<p></p>').text('description:'+item.description).appendTo('#etsy-images');
                            
                    } else {
                        $('#results').empty();
                    }
                }
            });

            return false;
        })
    });

})(jQuery);
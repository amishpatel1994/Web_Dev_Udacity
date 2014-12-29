
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var adr = streetStr + ', ' + cityStr;

    $greeting.text('So, you want to live at ' + adr + '?');

    var adrUrl = 'https://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + adr + '';
    $body.append('<img class="bgimg" src="' + adrUrl + '">');
    // YOUR CODE GOES HERE!
    $('body').css('background-image','url(adrUrl)');


    var nyTimesAPI = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + cityStr + '&sort=newest&api-key=787c6af8de66e0331e2dfdc0bfa5f07b:3:70596932';
    var articles;
    var jqxhr = $.getJSON(nyTimesAPI, function(data) {
        $nytElem.text('New York Times Article About ' + cityStr);
        articles = data.response.docs;
        for (var i = 0; i < articles.length; i++){
            var article = articles[i];
            $nytElem.append('<li class="article">' +
                '<a href="'+article.web_url+'">' +
                article.headline.main + '</a>' +
                '<p>' + article.snippet + '</p>' +
                '</li>');
        }
    })
    .done(function() {  
    console.log( "second success" );
    })
    .fail(function() {
        $nytElem.text('New York Times Articles could not be loaded');
    })
    .always(function() {
      console.log( "complete" );
    });

    return false;
};

$('#form-container').submit(loadData);

 
// loadData();

javascript:(function(){
    var postURL = 'http://127.0.0.1:5000/post?type=keyword&';

    var productsContainer = document.querySelector('#s-results-list-atf');
    var productsList = productsContainer.getElementsByTagName('li');
    var asins = {logDate: new Date().toISOString()};
    for (var i=0; i<productsList.length; i++) {
        asins[i] = productsList[i].attributes['data-asin'].value;
    }

    var getParams = Object.keys(asins).map(function(k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(asins[k]);
    }).join('&');

    var amazonGetParams = window.location.search,
        postLink = postURL + getParams + amazonGetParams;
    window.open(postLink);
    for (var i=0; i<productsList.length; i++) {
        window.open('https://www.amazon.de/dp/' + productsList[i].attributes['data-asin'].value);
    }
}());

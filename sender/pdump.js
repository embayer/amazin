javascript:(function(){
    var data = {};
    data.title = document.querySelector('#productTitle').innerText;
    data.brand = document.querySelector('#brand').innerText;
    data.salesPrice = document.querySelector('#priceblock_saleprice').innerText;

    var url = Object.keys(data).map(function(k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]);
    }).join('&');

    var link = document.URL,
        postLink = 'http://127.0.0.1:5000/post?link=' + encodeURIComponent(link) + '&' + url;
    window.open(postLink);
}());
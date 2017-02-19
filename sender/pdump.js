javascript:(function(){
    function extractASIN(url) {
        var asinRegex = /\/([A-Z0-9]{10})/,
            match = asinRegex.exec(url);
        return match[1];
    }

    var data = {};
    data.url = document.URL;
    data.asin = extractASIN(data.url);
    data.title = document.querySelector('#productTitle').innerText;
    data.brand = document.querySelector('#brand').innerText;
    data.brandURL = document.querySelector('#brand').href;
    data.seller = document.querySelector('#merchant-info > a:nth-child(1)').innerText;
    data.sellerURL = document.querySelector('#merchant-info > a:nth-child(1)').href;
    data.shipping = document.querySelector('#SSOFpopoverLink').innerText;
    data.shippingURL = document.querySelector('#SSOFpopoverLink').href;
    data.salesPrice = document.querySelector('#priceblock_saleprice').innerText;
    data.stars = document.querySelector('#acrPopover > span.a-declarative > a > i.a-icon.a-icon-star.a-star-5 > span').innerText;
    data.reviewCount = document.querySelector('#acrCustomerReviewText').innerText;
    data.salesRank = document.querySelector('#SalesRank').innerText;

    var bulletContainer = document.querySelector('#feature-bullets'),
        bulletList = bulletContainer.getElementsByTagName('ul'),
        bulletItems = bulletList[0].getElementsByTagName('li');
    for (var i=0; i<bulletItems.length; i++) {
        eval('data.bullet_' +  + i + ' = ' + bulletItems[i].innerText);
    }

    var getParams = Object.keys(data).map(function(k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]);
    }).join('&');

    var postLink = 'http://127.0.0.1:5000/post?type=product&' + getParams;
    window.open(postLink);
}());
/**
javascript:(function(){function extractASIN(url) {var asinRegex = /\/([A-Z0-9]{10})/, match = asinRegex.exec(url); return match[1];} var data = {}; data.url = document.URL; data.asin = extractASIN(data.url); data.title = document.querySelector('#productTitle').innerText; data.brand = document.querySelector('#brand').innerText; data.brandURL = document.querySelector('#brand').href; data.seller = document.querySelector('#merchant-info > a:nth-child(1)').innerText; data.sellerURL = document.querySelector('#merchant-info > a:nth-child(1)').href; data.shipping = document.querySelector('#SSOFpopoverLink').innerText; data.shippingURL = document.querySelector('#SSOFpopoverLink').href; data.salesPrice = document.querySelector('#priceblock_saleprice').innerText; data.stars = document.querySelector('#acrPopover > span.a-declarative > a > i.a-icon.a-icon-star.a-star-5 > span').innerText; data.reviewCount = document.querySelector('#acrCustomerReviewText').innerText; data.salesRank = document.querySelector('#SalesRank').innerText; var bulletContainer = document.querySelector('#feature-bullets'), bulletList = bulletContainer.getElementsByTagName('ul'), bulletItems = bulletList.getElementsByTagName('li'); for (var i=0; i<bulletItems.length; i++) {eval('data.bullet_' +  + i + ' = ' + bulletItems[i].innerText);} var getParams = Object.keys(data).map(function(k) {return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]);}).join('&'); var postLink = 'http://127.0.0.1:5000/post?type=product&' + getParams; window.open(postLink);}());
**/

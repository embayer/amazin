javascript:(function(){
    var postURL = 'http://127.0.0.1:5000/post?type=product&';
    function innerTextOrNull () {}
    function asinFromURL(url) {
        var asinRegex = /\/([A-Z0-9]{10})/,
            match = asinRegex.exec(url);
        return match[1];
    }

    var product = {};
    product.url = document.URL;
    product.asin = product._id = asinFromURL(product.url);
    product.pricehistory = 'https://dyn.keepa.com/pricehistory.png?domain=de&asin=' + product.asin;
    product.title = document.querySelector('#productTitle').innerText;
    product.brand = document.querySelector('#brand').innerText;
    product.brandURL = document.querySelector('#brand').href;
    product.reviewCount = document.querySelector('#acrCustomerReviewText').innerText;
    product.salesRank = document.querySelector('#SalesRank').innerText;
    product.price = document.querySelector('span[id^=priceblock_]').innerText;
    product.priceCategory = document.querySelector('span[id^=priceblock_]').id;

    var stars = document.querySelector('#acrPopover').title;
    if (!stars) {
        product.stars = document.querySelector('#acrPopover').title;
    }

    var seller = document.querySelector('#merchant-info > a');
    if (seller) {
        product.seller = seller.innerText;
        product.sellerURL = seller.href;

        var shipping = document.querySelector('#SSOFpopoverLink');
        if (shipping) {
            product.sellerType = 'fba';
            product.shipping = document.querySelector('#SSOFpopoverLink').innerText;
            product.shippingURL = document.querySelector('#SSOFpopoverLink').href;
        } else {
            product.sellerType = 'marketplace';
            product.shipping = 'amazon';
            product.shippingURL = 'https://www.amazon.de/';
        }
    } else {
        product.sellerType = 'amazon';
        product.seller = 'amazon';
        product.sellerURL = 'https://www.amazon.de/';
        product.shipping = 'amazon';
        product.shippingURL = 'https://www.amazon.de/';
    }

    var bulletContainer = document.querySelector('#feature-bullets'),
        bulletList = bulletContainer.getElementsByTagName('ul'),
        bulletItems = bulletList[0].getElementsByTagName('li');
    for (var i=0; i<bulletItems.length; i++) {

        console.log('product.bullet_' + i + ' = ' + '"' + bulletItems[i].innerText.trim() + '"');
        eval('product.bullet_' + i + ' = ' + '"' + bulletItems[i].innerText.trim() + '"');
    }

    var getParams = Object.keys(product).map(function(k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(product[k]);
    }).join('&');

    var amazonGetParams = window.location.search,
        postLink = postURL + getParams + amazonGetParams;
    window.open(postLink);
}());

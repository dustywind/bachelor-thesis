
var express = require('express');
var http = require('http');
var router = express.Router();

function getOptions(){
    var options = {
        host: 'localhost',
        port: '8080',
        //path: '/product/get/' + req.params.product_id
    };
    return options;
}

function appendMeta(user_name, product){
    product.image_path = '/images/' + product.image_name;
    product.product_url = '/implicit/' + user_name + '/product/' + product.document_id;
    return product;
}

function getRenderObject(user_name, product_id){
    function overviewUrl(){
        return '/implicit/' + user_name + '/overview';
    }
    function userUrl(){
        return '/implicit/' + user_name;
    }
    function preferenceUrl(){
        return '/implicit/' + user_name + '/setpreference/' + product_id;
    }
    function productUrl(){
        return '/implicit/' + user_name + '/product/' + product_id;
    }
    function userUrl(){
        return '/implicit/' + user_name;
    }
    var meta = {
        implicit: true,
        header: true,
        user_name: user_name,
        product_id: product_id,
        overview_url: overviewUrl(),
        product_url: productUrl(),
        user_url: userUrl(),
        preference_url: preferenceUrl()
    };
    return meta;
}





/* GET home page */
router.get('/', function(req, res, next){
    res.render('index', {title: 'Implicit'});
});


/* GET overview */
router.get('/:user_name/overview', function(req, res, next){
    var options = getOptions();
    options.path =  '/product/get/' + req.params.product_id;

    var user_name = req.params.user_name;
    var product_id = req.params.product_id;
    var overview_count = 50;
    var recommendation_count = 5;


    function randomProducts(){
        randomProductsApiCall(overview_count, function(product_list){
            random_product_list = product_list;
            sendIfReady();
        });
    }

    function recommendations(){
        recommendationApiCall(user_name, recommendation_count, function(product_list){
            recommendet_product_list = product_list;
            sendIfReady();
        });
    }

    random_product_list = null;
    recommendet_product_list = null;

    randomProducts();
    recommendations();

    function sendIfReady(){
        if(random_product_list && recommendet_product_list){

            for(var index in random_product_list){
                appendMeta(user_name, random_product_list[index]);

            }

            for(var index in recommendet_product_list){
                appendMeta(user_name, recommendet_product_list[index]);
            }

            var renderObj = getRenderObject(user_name, product_id);
            renderObj.title = 'Implicit';
            renderObj.recommendations = recommendet_product_list;
            renderObj.random = random_product_list;
            res.render('overview', renderObj);
        }
    }
});



/* GET product */
router.get('/:user_name/product/:product_id', function(req, res){
    var user_name = req.params.user_name;
    var product_id = req.params.product_id
    productApiCall(product_id, function(chunk){
        var product = JSON.parse(chunk).result;
        product.image_path = '/images/' + product.image_name;
        var renderObj = getRenderObject(user_name, product_id);

        renderObj.product = product;
        res.render('product', renderObj);
    });
});


/* GET setPreference */
router.get('/:user_name/setpreference/:product_id', function(req, res){

    var user_name = req.params.user_name;
    var product_id = req.params.product_id;
    preferenceApiCall(user_name, product_id);
    res.send('OK');
});

/* GET user info */
router.get('/:user_name', function(req, res){
    var user_name = req.params.user_name;

    var user_vector = null;
    var user_preference = null;

    uservectorApiCall(user_name, function(chunk){
        user_vector = JSON.parse(chunk).result;
        sendIfReady();
    });

    userpreferenceApiCall(user_name, function(chunk){
        user_preference = JSON.parse(chunk).result;
        for(var index in user_preference){
            appendMeta(user_name, user_preference[index]);
        }
        sendIfReady();
    });

    function sendIfReady(){
        if(user_vector && user_preference){
            var renderObj = getRenderObject(user_name, null);
            renderObj.user_vector = user_vector;
            renderObj.user_preference = user_preference;

            res.render('user', renderObj);
        }
    }
});



function productApiCall(product_id, callback){
    var options = getOptions();
    options.path =  '/product/get/' + product_id;

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', callback);
    }).end();
}

function uservectorApiCall(user_name, callback){
    var options = getOptions();
    options.path = '/vector/user/' + user_name;

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', callback);
    }).end();
}


function userpreferenceApiCall(user_name, callback){
    var options = getOptions();
    options.path = '/user/relevant/' + user_name;

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', callback);
    }).end();
}



function preferenceApiCall(user_name, product_id){
    var options = getOptions();
    options.path = '/user/setpreference/' + user_name + '/' + product_id;
    http.request(options, function(res){}).end();
}

function randomProductsApiCall(count, callback){
    var options = getOptions();
    options.path = '/product/random/' + count;
    http.request(options, function(res){

        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            var result = JSON.parse(data);
            var products = result.result;
            callback(products);
        });

    }).end();
}

function recommendationApiCall(user_name, count, callback){
    var options = getOptions();
    options.path = '/recommendations/' + user_name + '/' + count;
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            var result = JSON.parse(data);
            var products = result.result;
            callback(products);
        });
    }).end();
}






/* last line: */
module.exports = router;

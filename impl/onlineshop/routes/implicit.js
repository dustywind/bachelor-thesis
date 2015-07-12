
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


/* GET home page */
router.get('/', function(req, res, next){
    res.render('index', {title: 'Implicit'});
});


/* GET overview */
router.get('/:user_name/overview', function(req, res, next){
    var options = getOptions();
    options.path =  '/product/get/' + req.params.product_id;

    var user_name = req.params.user_name;
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
                appendImagePath(random_product_list[index]);

            }

            for(var index in recommendet_product_list){
                appendImagePath(recommendet_product_list[index]);
            }

            res.render('overview', {
                title: 'Implicit',
                recommendations: recommendet_product_list,
                random: random_product_list,
                implicit: true
            });
        }
    }
});



/* GET product */
router.get('/:user_name/product/:product_id', function(req, res){

    productApiCall(req.params.product_id, function(chunk){
        var product = JSON.parse(chunk).result;
        product.image_path = '/images/' + product.image_name;
        res.render('product', {
            'product': product,
            'implicit': true,
            'preference_callback': '/implicit/' + req.params.user_name + '/setpreference/' + product.document_id
        });
    });
});


/* GET setPreference */
router.get('/:user_name/setpreference/:product_id', function(req, res){

    var user_name = req.params.user_name;
    var product_id = req.params.product_id;
    preferenceApiCall(user_name, product_id);
    res.send('OK');
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



function appendImagePath(product){
    product.image_path = '/images/' + product.image_name;
    return product;
}



/* last line: */
module.exports = router;

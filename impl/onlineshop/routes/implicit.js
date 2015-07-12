
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


    function randomProducts(){
    }

    function recommendations(){
    }

    apiCalls = [];


    res.render('overview', {title: 'Implicit'});
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




/* last line: */
module.exports = router;

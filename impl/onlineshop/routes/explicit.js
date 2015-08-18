
var express = require('express');
var router = express.Router();
var recommender = require('./recommenderapi');

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
    product.product_url = '/explicit/' + user_name + '/product/' + product.document_id;
    return product;
}

function getRenderObject(user_name, product_id){
    var baseUrl = '/explicit/';
    function overviewUrl(){
        return baseUrl + user_name + '/overview';
    }
    function userUrl(){
        return baseUrl + user_name;
    }
    function preferenceUrl(){
        return baseUrl + user_name + '/setpreference/' + product_id;
    }
    function noPreferenceUrl(){
        return baseUrl + user_name + '/setnopreference/' + product_id;
    }
    function productUrl(){
        return baseUrl + user_name + '/product/' + product_id;
    }
    function userUrl(){
        return baseUrl + user_name;
    }
    var meta = {
        implicit: false,
        header: true,
        user_name: user_name,
        product_id: product_id,
        overview_url: overviewUrl(),
        product_url: productUrl(),
        user_url: userUrl(),
        preference_url: preferenceUrl(),
        no_preference_url: noPreferenceUrl()
    };
    return meta;
}



/* GET home page */
router.get('/', function(req, res, next){
    res.render('index', {title: 'Explicit'});
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
        recommender.getRandomProducts(overview_count, function(product_list){
            random_product_list = product_list;
            sendIfReady();
        });
    }

    function recommendations(){
        recommender.getRecommendations(user_name, recommendation_count, function(product_list){
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
    recommender.getProduct(product_id, function(product){
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
    recommender.setPreference(user_name, product_id);
    res.send('OK');
});

/* GET setPreference */
router.get('/:user_name/setnopreference/:product_id', function(req, res){

    var user_name = req.params.user_name;
    var product_id = req.params.product_id;
    recommender.setNoPreference(user_name, product_id);
    res.send('OK');
});

/* GET user info */
router.get('/:user_name', function(req, res){
    var user_name = req.params.user_name;

    var user_vector = null;
    var user_preference = null;

    recommender.getUserVector(user_name, function(userVector){
        user_vector = userVector
        sendIfReady();
    });

    recommender.getUserPreference(user_name, function(userPreference){
        user_preference = userPreference;
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




/* last line: */
module.exports = router;

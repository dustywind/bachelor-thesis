
var http = require('http');

function getOptions(){
    var options = {
        host: 'localhost',
        port: '8080',
        //path: '/product/get/' + req.params.product_id
    };
    return options;
}


exports.getProduct = function(product_id, callback){
    var options = getOptions();
    options.path =  '/product/get/' + product_id;

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            var product = JSON.parse(result).result;
            callback(product);
        });
    }).end();
}

exports.getUserVector = function(user_name, callback){
    var options = getOptions();
    options.path = '/vector/user/' + user_name;

    var result = '';

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data
        });
        res.on('end', function(data){
            var userVector = JSON.parse(result).result;
            callback(userVector);
        });
    }).end();
}


exports.getUserPreference = function(user_name, callback){
    var options = getOptions();
    options.path = '/user/relevant/' + user_name;

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data
        });
        res.on('end', function(data){
            var userPreference = JSON.parse(result).result;
            callback(userPreference);
        });
    }).end();
}



exports.setPreference = function(user_name, product_id){
    var options = getOptions();
    options.path = '/user/setpreference/' + user_name + '/' + product_id;
    http.request(options, function(res){}).end();
}

exports.getRandomProducts = function(count, callback){

    var options = getOptions();
    options.path = '/product/random/' + count;

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            var products = JSON.parse(result).result;
            callback(products);
        });
    }).end();
}

exports.getRecommendations = function(user_name, count, callback){

    var options = getOptions();
    options.path = '/recommendations/' + user_name + '/' + count;

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            var recommendations = JSON.parse(result).result;
            callback(recommendations);
        });
    }).end();
}



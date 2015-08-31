
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
};

exports.removeProduct = function(product_id, callback){
    var options = getOptions();
    options.path = '/product/remove/' + product_id;
    options.method = 'DELETE';

    var result = '';
    http.delete(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            callback(r);
        });
    }).end();
};

exports.removeUser = function(user_name, callback){
    var options = getOptions();
    options.path = '/user/remove/' + user_name;
    options.method = 'DELETE';

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', console.log);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            callback(r);
        });
    }).end();
};

exports.createUserIfNotExists = function(username, success, error){
    var options = getOptions();
    options.path = '/user/createifnotexist/' + username;

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', error);
        res.on('data', function(data){
            result += data;  
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            success(r);
        });
    }).end();
};



exports.availableUsers = function(success, error){
    var options = getOptions();
    options.path = '/user/all';

    var result = '';
    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', error);
        res.on('data', function(data){
            result += data;  
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            success(r);
        });
    }).end();
};



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
};


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
};


exports.setPreference = function(user_name, product_id, success, error){
    var options = getOptions();

    options.path = '/user/setpreference/' + user_name + '/' + product_id;

    result = '';

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', error);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            success(r);
        });
    }).end();
};

exports.setNoPreference = function(user_name, product_id, success, error){
    var options = getOptions();
    options.path = '/user/setnopreference/' + user_name + '/' + product_id;

    result = '';

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', error);
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            success(r);
        }) 
    }).end();
};


exports.updateUser = function(user_name, success, error){
    var options = getOptions();

    var defaultWeights = false;
    var weights = '';

    if(!defaultWeights){
        var alpha = 60;
        var beta = 90;
        var gamma = 10;

        weights = '/' + alpha + '/' + beta + '/' + gamma;
    }

    options.path = '/user/update/' + user_name + weights;

    result = '';

    http.request(options, function(res){
        res.setEncoding('utf8');
        res.on('error', error); 
        res.on('data', function(data){
            result += data;
        });
        res.on('end', function(data){
            r = JSON.parse(result).result;
            success(r); 
        });
    }).end();
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
};

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
};



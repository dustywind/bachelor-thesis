var express = require('express');
var router = express.Router();
var recommender = require('./recommenderapi');

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

function getFeedbackPossibilities(){
    return ['implicit', 'explicit', 'implicittimed']
}



/* GET home page */
router.get('/', function(req, res, next){

    var userList = null;

    /*
    recommender.availableUsers(function(user_list){
        userList = user_list
        sendIfReady();
    }, function(x){});

    function sendIfReady(){
        if(isReady()){
            send();
        }
    };

    function isReady(){
        ready = true;
        ready = ready && (userList !== null);
        return ready;
    };
    */

    send();

    function send(){
        res.render('index', {
            title: 'recommender.io.js',
            userlist: userList,
            feedback: getFeedbackPossibilities()
        });
    };
});


router.post('/login', function(req, res, next){
    var username = req.body.username;
    var feedback = req.body.feedback;

    if(feedbackIsValid(feedback)){
        recommender.createUserIfNotExists(username, 
            function success(data){
                redirectTo(username, feedback, res);
            },
            function error(data){
                res.send(500);
            }
        );
    }
});

function feedbackIsValid(feedback){
    var possFeedback = getFeedbackPossibilities();
    for(var index in possFeedback){
        if(feedback === possFeedback[index]){
            return true;
        }
    }
    return false;
}

function redirectTo(username, feedback, res){
    url = '/' + feedback + '/' + username + '/overview';
    res.redirect(url);
}


/* last line: */
module.exports = router;

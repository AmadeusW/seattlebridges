var OAuth2 = require('oauth').OAuth2;
var https = require('https');

var twitterConsumerKey = process.env.twitterBridgeKey;
var twitterConsumerSecret = process.env.twitterBridgeSecret;
console.log("key: ", twitterConsumerKey);
console.log("secret: ", twitterConsumerSecret);
var oauth2 = new OAuth2(
    twitterConsumerKey,
    twitterConsumerSecret, 
    'https://api.twitter.com/', 
    null,
    'oauth2/token', 
    null);
oauth2.getOAuthAccessToken(
    '',
    {'grant_type':'client_credentials'},
    function (e, accessToken, refreshToken, results){
        console.log('access: ',accessToken);
        
        var options = {
            hostname: 'api.twitter.com',
            path: '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=10',
            headers: {
                Authorization: 'Bearer ' + accessToken
            }
          };
        https.get(options, function(result){
            var buffer = '';
            result.setEncoding('utf8');
            result.on('data', function (data) {
                buffer += data;
            });
            result.on('end', function () {
                var tweets = JSON.parse(buffer);
                console.log("Processing...");
                processTweets(tweets);
            });
        }).on("error", function(e){
            console.log("Error: ", e.message);
        });
    }
);

var requestTweets = function(lastId) {
    
}

var processTweets = function(tweets) {
    console.log(tweets);
    tweets.forEach(tweet => {
        console.log("id: ", tweet.id)
        console.log("text", tweet.text)
        console.log("time ", tweet.created_at)
    });
}
var fetchData = function(accessToken) {
    var options = {
      hostname: 'api.twitter.com',
      path: '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=10',
      headers: {
          Authorization: 'Bearer ' + accessToken
      }
    };
    https.get(options, function(result){
        var buffer = '';
        result.setEncoding('utf8');
        result.on('data', function (data) {
            buffer += data;
        });
        result.on('end', function () {
            var tweets = JSON.parse(buffer);

            console.log(tweets); // the tweets!
});
    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });
}
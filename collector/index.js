var OAuth2 = require('oauth').OAuth2;
var https = require('https');
var fs = require('fs');

var twitterConsumerKey = process.env.twitterBridgeKey;
var twitterConsumerSecret = process.env.twitterBridgeSecret;
var AccessToken;
var LastId;
var requestCount = 1000;

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
        AccessToken = accessToken;
        requestTweets();
    }
);

var requestTweets = function(lastId) {
    var path = '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=50'
    if (lastId != undefined) {
        path = '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=50&max_id='+lastId
    }
    console.log("Requesting", path)
    var options = {
        hostname: 'api.twitter.com',
        path: path,
        headers: {
            Authorization: 'Bearer ' + AccessToken
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

var processTweets = function(tweets) {
    //console.log(tweets);
    tweets.forEach(tweet => {
        if (tweet.id == undefined) throw 'Invalid data'
        //console.log("id: ", tweet.id)
        LastId = tweet.id
        //console.log("text", tweet.text)
        //console.log("time ", tweet.created_at)
        // subtract 8 hours
        var utcCreated = new Date(tweet.created_at)
        var localTime = new Date(utcCreated.getTime() - utcCreated.getTimezoneOffset() * 60000)
        //console.log("local time", localTime)
        var nameLength = tweet.text.indexOf(" has ");
        var name = tweet.text.substring(0, nameLength);
        var timeIndex = tweet.text.indexOf(" to traffic - ");
        var tweetedTime = tweet.text.substring(timeIndex + 14);
        var opened = tweet.text.substring(nameLength + 5, timeIndex);
        var closedBool = opened == "closed";
        //console.log(name, opened, opened == "reopened", tweetedTime)
        console.log(name, opened, "at", localTime);
        var data = tweet.id + "," + name + "," + closedBool + "," + localTime.toISOString() + "," + tweetedTime + "\n"
        fs.appendFile("tweets.csv", data, function (err) {
            if (err) throw err;
            console.log(data);
        });
    });
    if (requestCount-- > 0) {
        console.log("Requesting more. LastId", LastId)
        requestTweets(LastId);
    }
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
            processTweets(tweets);
});
    }).on("error", function(e){
      console.log("Got error: " + e.message);
    });
}
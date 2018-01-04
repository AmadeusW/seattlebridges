// USage: for all tweets until specific ID,
// node .\index.js 940726622650490900 
// for all tweets starting with specific ID, see commented out invocation to requestTweets

var OAuth2 = require('oauth').OAuth2;
var https = require('https');
var fs = require('fs');

var twitterConsumerKey = process.env.twitterBridgeKey;
var twitterConsumerSecret = process.env.twitterBridgeSecret;
var AccessToken;
var LastId;
var SinceId;
var idFromParameter;

console.log(process.argv);
if (process.argv.length == 3)
    idFromParameter = process.argv[2];

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

        requestTweets(); // use this line to request all tweets since now
        //requestTweets(941044213935890400); // use this line to request tweets older than this ID
    }
);

var requestTweets = function(id) {
    var path = '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=50'
    if (id != undefined) {
        // Use the line below for tweets older than id
        path = '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=50&max_id='+id
        // Use the line below for tweets newer than id, but this is all messed up so don't. Just keeping it for API reference.
        //path = '/1.1/statuses/user_timeline.json?screen_name=SDOTbridges&count=50&since_id='+id
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
            processTweets(tweets);
        });
    }).on("error", function(e){
        console.error("Error: ", e.message);
    });
}

var processTweets = function(tweets) {
    for(var i = 0; i < tweets.length; i++) {
        var tweet = tweets[i];
        if (tweet.id == undefined) throw 'Invalid data'
        if (tweet.id > SinceId || SinceId == undefined)
            SinceId = tweet.id
        if (tweet.id < LastId || LastId == undefined)
            LastId = tweet.id

        // subtract 8 hours
        var utcCreated = new Date(tweet.created_at)
        var localTime = new Date(utcCreated.getTime() - utcCreated.getTimezoneOffset() * 60000)
        var nameLength = tweet.text.indexOf(" has ");
        var name = tweet.text.substring(0, nameLength);
        var timeIndex = tweet.text.indexOf(" to traffic - ");
        var tweetedTime = tweet.text.substring(timeIndex + 14);
        var opened = tweet.text.substring(nameLength + 5, timeIndex);
        var closedBool = opened == "closed";
        var data = tweet.id + "," + name + "," + closedBool + "," + localTime.toISOString() + "," + tweetedTime + "\n"

        //console.log(data); // Diagnostics
        if (tweet.id <= idFromParameter)
        {
            console.log("STOP! Reached ", idFromParameter, " in tweet #", tweet.id)
            setTimeout(function() {
                console.log('Waiting...');
            }, 1000);
            return;
        }

        fs.appendFileSync("tweets.csv", data);
    }

    console.log("Requesting more. Id", LastId)
    requestTweets(LastId);
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
      console.error("Got error: " + e.message);
    });
}
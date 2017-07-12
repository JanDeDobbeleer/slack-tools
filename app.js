/*jshint esversion: 6*/

var util = require('util');
var express = require('express');
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var Slack = require('slack-node');

var urlencodedParser = bodyParser.urlencoded({ extended: false });
var app = express();
var spinning = false;

// settings
app.use(bodyParser.json()); // for parsing application/json
var port = process.env.PORT || 3000;
var options = {
    pythonPath: '/usr/bin/python3'
};

// respond with "hello world" when a GET request is made to the homepage
app.get('/', function(req, res) {
    res.send('hello world');
});

// Send a notification to the correct person/group
app.post('/slash-command', urlencodedParser, function(req, res) {
    // check if we are received a request from slack
    if (req.body.token !== process.env.S_TOKEN) {
        res.status(403).end();
        return;
    }
    handleCommand(res, req);
});

function handleCommand(response, request) {
    switch (request.body.text) {
        case 'stievie free':
            response.status(200).end(`Hey ${request.body.user_name}, please hold while I create you a new Stievie Free user!`);
            runPythonCommand(request, 'commands/stievie_free.py');
            break;
        case 'stievie premium':
            response.status(200).end(`Hey ${request.body.user_name}, please hold while I create you a new Stievie Premium user!`);
            runPythonCommand(request, 'commands/stievie_premium.py');
            break;
        case 'stievie premium mandate':
            response.status(200).end(`Hey ${request.body.user_name}, please hold while I create you a new Stievie Premium user with a mandate!`);
            runPythonCommand(request, 'commands/stievie_premium_mandate.py');
            break;
        case 'make me a sandwich':
            response.status(200).end(`Fuck you ${request.body.user_name}, make your own goddamn sandwich.`);
            break;
        default:
            let options = ['stievie free', 'stievie premium', 'stievie premium mandate'];
            response.status(200).end(`I'm sorry ${request.body.user_name}, I didn't quite get that. Please try again. The options are:\n ${options.join('\n')}`);
    }
}

function runPythonCommand(req, script) {
    slack = new Slack();
    slack.setWebhook(req.body.response_url);
    PythonShell.run(script, options, function(err, results) {
        // script finished
        var text = 'Something went wrong, please try again';
        if (!err) {
            text = results.join('\n');
        }
        slack.webhook({
            channel: req.body.channel_id,
            text: text
        }, function(err, response) {
            console.log(response);
        });
    });
}

app.listen(port, function() {
    console.log('Example app listening on port 3000!');
});
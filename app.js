/*jshint esversion: 6*/

var util = require('util');
var express = require('express');
var bodyParser = require('body-parser');
var PythonShell = require('python-shell');
var Slack = require('slack-node');
var fs = require('fs');

var urlencodedParser = bodyParser.urlencoded({ extended: false });
var app = express();

// settings
app.use(bodyParser.json()); // for parsing application/json
var port = process.env.PORT || 3000;
var options = {
    pythonPath: '/usr/bin/python3'
};

// load command settings
const commands = JSON.parse(fs.readFileSync('./settings.json', 'utf8'));

// respond with "hello world" when a GET request is made to the homepage
app.get('/', function(req, res) {
    res.send('hello world from Slack tools!');
});

// Send a notification to the correct person/group
app.post('/slash-command', urlencodedParser, function(req, res) {
    // check if we are received a request from slack
    if (req.body.token !== process.env.S_TOKEN) {
        res.status(403).end();
        return;
    }
    //check for Gigya queries first, only for authorized users
    if (handleQueries(req, res) || handleCommand(req, res)){
        return;
    }
    printOptions(req, res);
});

function printOptions(request, response) {
    let options = commands.map(command => `${command.key}: ${command.help}`);
    response.status(200).end(`I'm sorry ${request.body.user_name}, I didn't quite get that. Please try again. The options are:\n ${options.join('\n')}`);
}

function handleCommand(request, response) {
    hasCommand = false;
    available_commands = commands.filter(command => command.type === 'COMMAND');
    available_commands.forEach(function(command) {
        if (request.body.text === command.key) {
            response.status(200).end(`Hang on ${request.body.user_name}, I'll grab a coffee and get to work.`);
            runPythonCommand(request, command.script);
            hasCommand = true;
        }
    });
    return hasCommand;
}

function handleQueries(request, response) {
    var users = process.env.GIGYA_USERS.split(' ');
    if (users.indexOf(request.body.user_name) <= -1) {
        response.status(200).end(`I'm sorry ${request.body.user_name}, I'm afraid this is above your pay grade.`);
        return false;
    }
    hasQuery = false;
    available_commands = commands.filter(command => command.type === 'QUERY');
    available_commands.forEach(function(command) {
        if (request.body.text.startsWith(command.key)) {
            response.status(200).end(`Hang on ${request.body.user_name}, slapping Gigya monkeys to do the work.`);
            let query = request.body.text.replace(`${command.key} `, '');
            runPythonCommand(request, command.script, [query]);
            hasQuery = true;
        }
    });
    return hasQuery;
}

function runPythonCommand(req, script, args) {
    slack = new Slack();
    slack.setWebhook(req.body.response_url);
    if (args) {
        options.args = args;
    }
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
            if (err) { console.log(response); }
        });
    });
}

app.listen(port, function() {
    console.log('Example app listening on port 3000!');
});
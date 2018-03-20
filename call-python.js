#!/usr/bin/env node

var glob = require("glob");

var PythonShell = require('python-shell');

const args = process.argv; // insert magnitude as in filename, for ex. 17.0

var mag = args[2];

var fitlist=glob.sync("/home/indy/desktop/sim/r-g-50/NTT"+mag+"_*.fits");

var outjson=[];                

let requests = fitlist.map((item) => {
    return new Promise((resolve) => {
        
        let data = { filename:item,
                     x_true: 26.66, // in the star file!
                     y_true: 27.77, // in the star file!
                     x: 23,
                     y: 23,
                     box: 45,
                     mag: parseFloat(mag)
                   };
        
//        var pyshell = new PythonShell('./gaussian2dfit-davide.py', {pythonPath : '/usr/bin/python3'});
        var pyshell = new PythonShell('./marginalfit.py', {pythonPath : '/usr/bin/python3'});
//        var pyshell = new PythonShell('./centroidfit.py', {pythonPath : '/usr/bin/python3'});
//        var pyshell = new PythonShell('./cubicfit.py', {pythonPath : '/usr/bin/python3'});
        
        pyshell
            .send(JSON.stringify(data), {mode:'json'})
            .on('message', function (message) {
                outjson.push(JSON.parse(message));
            });

        pyshell
            .end(function(err){
                if (err){
            console.log('error:');
                    throw err;
                }
                resolve(); /// callback function when finished
            });

    });
    
});

Promise.all(requests).then(function(){
    console.log(JSON.stringify(outjson,null,2));
        
});


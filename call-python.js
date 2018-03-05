var glob = require("glob");

var PythonShell = require('python-shell');

var fitlist=glob.sync("/home/indy/desktop/sim/v-vega/NTT15*.fits");

var outjson=[];                

let requests = fitlist.map((item) => {
    return new Promise((resolve) => {
        
        let data = { filename:item,  x:48, y:47, box:30 };

        var pyshell = new PythonShell('./gaussian2dfit-davide.py', {pythonPath : '/usr/bin/python3'});
        
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


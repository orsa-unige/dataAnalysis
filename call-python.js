var glob = require("glob");

var PythonShell = require('python-shell');
var pyshell = new PythonShell('./gaussian2dfit-davide.py', {pythonPath : '/usr/bin/python3'});


// options is optional
var fitlist=glob.sync("/home/indy/desktop/sim/v-vega/NTT15*1.fits");

var outjson=[];

fitlist.forEach(function(item, index){
    var data = { filename:item,  x:48, y:47, box:30 };
//    var data = { filename:"/home/indy/desktop/sim/v-vega/NTT15_11.fits",  x:48, y:47, box:30 };
    
    pyshell.send(JSON.stringify(data), {mode:'json'});//the problem function

    pyshell.on('message', function (message) {
        outjson.push(message);
       
    });
    
 });

// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err){
        console.log('error:');
        throw err;
    };
    
    console.log(outjson);

});

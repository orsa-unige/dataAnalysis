var PythonShell = require('python-shell');
var pyshell = new PythonShell('./gaussian2dfit-davide.py', {pythonPath : '/usr/bin/python3'});

const data = { filename:"/home/indy/desktop/sim/v-vega/NTT16_5.fits",  x:53, y:46, box:30 };

pyshell.send(JSON.stringify(data), {mode:'json'},{});//the problem function

pyshell.on('message', function (message) {
    console.log("asd")
    console.log(message)
    
});

// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err){
    console.log('error:');
        throw err;
    };
});

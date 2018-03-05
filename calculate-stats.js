
var glob = require("glob");

var jslist=glob.sync("./ntt-*.json");

var outputjson = [];

// let requests = jslist.map((item) => {
//     return new Promise((resolve) => {


jslist.forEach(function(item, index){

        var injson = require(item);

    outputjson.push ({
        filename:item,
        x_mean_arr : injson.map(o => o.output.x_mean_0),
        y_mean_arr : injson.map(o => o.output.y_mean_0),            
        x_stddev_arr : injson.map(o => o.output.x_stddev_0),
        y_stddev_arr : injson.map(o => o.output.y_stddev_0)
    });

//        resolve();
        
        // var pyshell = new PythonShell('./gaussian2dfit-davide.py', {pythonPath : '/usr/bin/python3'});
        
        // pyshell
        //     .send(JSON.stringify(data), {mode:'json'})
        //     .on('message', function (message) {
        //         outjson.push(JSON.parse(message));
        //     });

        // pyshell
        //     .end(function(err){
        //         if (err){
        //     console.log('error:');
        //             throw err;
        //         }
        //         resolve(); /// callback function when finished
        //     });

    });
    
// });

// Promise.all(requests).then(function(){
//     console.log(JSON.stringify(outputjson,null,2));
        
// });


     console.log(JSON.stringify(outputjson));


var glob = require("glob");

var jslist=glob.sync("./ntt-*.json");

var outputjson = [];

jslist.forEach(function(item, index){

        var injson = require(item);

    outputjson.push ({
        mag:injson[0].mag,
        snr:injson[0].snr,
        pscale:injson[0].pscale,
        x_mean_arr : injson.map(o => o.output.x_mean_0),
        y_mean_arr : injson.map(o => o.output.y_mean_0),            
        err_vector : injson.map(o => Math.sqrt( (o.output.x_mean_0 - o.x_true)**2 + (o.output.y_mean_0 - o.y_true)**2) ),      
//        x_stddev_arr : injson.map(o => o.output.x_stddev_0),
//        y_stddev_arr : injson.map(o => o.output.y_stddev_0)
    });

});

console.log(JSON.stringify(outputjson));

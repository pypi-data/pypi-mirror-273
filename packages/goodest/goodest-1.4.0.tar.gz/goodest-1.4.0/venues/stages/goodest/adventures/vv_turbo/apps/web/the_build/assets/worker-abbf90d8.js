(function(){"use strict";console.log("web worker");function e(){console.log("web worker work")}self.onmessage=function(o){if(o.data,o.data.move==="start"){let s=e();self.postMessage(s)}}})();

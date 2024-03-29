/*
self.onmessage = function(event) {
    if (event.data === 'start') {
        setInterval(() => {
            self.postMessage('tick');
        }, 2000);
    }
};
*/

self.onmessage = function(event) {
    if (event.data === 'start') {
        function tick() {
            self.postMessage('tick');
            setTimeout(tick, 200);
        }
        tick(); // Start the recursive timer
    }
};


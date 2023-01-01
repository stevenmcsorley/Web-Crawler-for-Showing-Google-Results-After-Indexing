const http = require('http');
const fs = require('fs');
const url = require('url');

const server = http.createServer((req, res) => {
  // Parse the request URL
  const parsedUrl = url.parse(req.url);

  // Use a switch statement to determine which file to serve
  switch (parsedUrl.pathname) {
    case '/':
      // Set the response type
      res.setHeader('Content-Type', 'text/html');

      // Read the HTML file and send it as the response
      fs.readFile('index.html', (err, data) => {
        res.end(data);
      });
      break;
    case '/data.json':
      // Set the response type
      res.setHeader('Content-Type', 'application/json');

      // Read the JSON file and send it as the response
      fs.readFile('data.json', (err, data) => {
        res.end(data);
      });
      break;
    default:
      // Set the response status and type
      res.statusCode = 404;
      res.setHeader('Content-Type', 'text/plain');

      // Send a "not found" message as the response
      res.end('404 Not Found');
      break;
  }
});

server.listen(3000);

console.log('Server listening on port 3000');

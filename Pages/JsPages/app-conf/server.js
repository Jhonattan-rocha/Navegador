const http = require('http');
const express = require('express');
const path = require('path');

const app = express();

app.use(express.urlencoded({extended: true}));
app.use(express.static("./build"));

app.get("/config/", (req, res) => {
    res.sendFile(path.resolve("./", "build", "index.html"));
});

const server = http.createServer(app);

server.listen(3000, 'localhost', () => {
    console.log("Servidor de subpastas rodando na porta 3000 em localhost");
});
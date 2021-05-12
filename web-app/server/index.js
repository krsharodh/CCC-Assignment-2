const app = require('./app');

const PORT = process.env.PORT || 9000;

const baseURL = "http://127.0.0.1:5000/";

app.listen(PORT, () => {
    console.log(`App listening on port ${PORT}!`);
});

app.get("/sample", (req, res) => {

    // craft IEX API URL
    const url = `${baseURL}sample`;

    // make request to IEX API and forward response
    request(url).pipe(res);
});
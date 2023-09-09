const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const mysql = require("mysql");

const app = express();
const port = 8080;
const hostIP = "0.0.0.0";

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

const db = mysql.createConnection({
  host: "",
  user: "",
  password: "",
  database: "",
});

// Connect to the database
db.connect((err) => {
  if (err) throw err;
  console.log("Connected to the database");
});

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.get("/contact", (req, res) => {
  res.sendFile(__dirname + "/contact.html");
});

app.post("/submit", (req, res) => {
  const { name, email, message } = req.body;
  console.log(name);
  const sql = "INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)";
  db.query(sql, [name, email, message], (err, result) => {
    if (err) throw err;
    console.log("Data inserted into the database");
    res.sendFile(__dirname + "/success.html");
  });
});

app.listen(port, hostIP, () => {
  console.log(`Server is running on port ${port}`);
});

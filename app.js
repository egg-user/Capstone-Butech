const express = require('express');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const dotenv = require('dotenv');
const nodemailer = require('nodemailer');
const crypto = require('crypto');
const multer = require('multer');
const { error } = require('console');
const Usercontrollers = require('./controller')
const UsersModel = require ('./models')
const db = require('./database')
const upload = require('./middleware/multer')
const verifyToken = require('./middleware/token')

const app = express();
app.use(express.json());



//upload file
app.post('/upload', upload.single('photo'), (req, res) => {
    res.json({
        message: 'Upload berhasil'
    })
})

//middleware upload
app.use((err, req, res, next) => {
    res.json({
        message: err.message
    })
    next()
})


// GET ALL USERS
app.get('/users', Usercontrollers.getAllUsers);

//REGISTER USER
app.post('/users', Usercontrollers.registerUsers);

//LOGIN USER
app.post('/users/login', Usercontrollers.loginUsers);

//DELETE USER
app.delete('/users/:userId', Usercontrollers.deleteUsers);

//FORGOT PASSWORD
app.post('/users/forgot-password', Usercontrollers.forgotPasswordUsers);

//RESET PASSWORD
app.post('/users/reset-password/:token', Usercontrollers.resetPasswordUsers);

//UPDATE USER
app.put('/users/edit/:userId', Usercontrollers.updateUser);





app.listen(3000, () => {
    console.log('Server started on port 3000');
});
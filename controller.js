const mysql = require('mysql');
const dotenv = require('dotenv');
const express = require('express');
const bcrypt = require('bcrypt');
const crypto = require('crypto');
const UsersModel = require('./models')
const db = require('./database')
const jwt = require('jsonwebtoken');
// const secretKey = process.env.MY_KEY; 
dotenv.config();

// dotenv.config({ path: './.env' });



const getAllUsers = (req, res) => {
    db.query('SELECT * FROM akun', (error, result) => {
        if (error) {
            console.log(error);
            res.status(500).send('Internal Server Error');
        } else {
            res.json(result);
        }
    });
}

const registerUsers = async (req, res) => {
    try {
        const existingUser = await UsersModel.getUserByEmail(req.body.email);

        if (existingUser) {
            res.status(400).send('Email is already registered');
        } else {
            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(req.body.password, salt);

            const newUser = {
                first_name : req.body.first_name,
                last_name: req.body.last_name,
                email: req.body.email,
                password: hashedPassword,
                
            };

            db.query('INSERT INTO akun SET ?', newUser, (error, result) => {
                if (error) {
                    console.log(error);
                    res.status(500).send('Internal Server Error');
                } else {
                    console.log(result);
                    res.status(201).send('User Created');
                }
            });
        }
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}



const loginUsers = async (req, res) => {
    const email = req.body.email;
    db.query('SELECT * FROM akun WHERE email = ?', email, async (error, results) => {
        if (error) {
            console.log(error);
            res.status(500).send('Internal Server Error');
        } else if (results.length > 0) {
            const user = results[0];
            try {
                const token = jwt.sign({ email: email }, process.env.SECRET_KEY, { expiresIn: '1h' });
                if (await bcrypt.compare(req.body.password, user.password)) {
                    res.json({
                        message: 'Login berhasil',
                        token: token,
                    });
                } else {
                    res.send('gagal');
                }
            } catch (error) {
                console.log(error);
                res.status(500).send('Internal Server Error');
            }
        } else {
            res.status(400).send('User not found');
        }
    });
}

const deleteUsers = (req, res) => {
    const userId = req.params.userId;

    db.query('DELETE FROM akun WHERE id = ?', userId, (error, result) => {
        if (error) {
            console.log(error);
            res.status(500).send('Internal Server Error');
        } else if (result.affectedRows > 0) {
            res.send(`User with ID ${userId} deleted successfully`);
        } else {
            res.status(404).send(`User with ID ${userId} not found`);
        }
    });
}

const forgotPasswordUsers = async (req, res) => {
    const email = req.body.email;

    try {
        const user = await UsersModel.getUserByEmail(email);

        if (!user) {
            return res.status(404).send('User not found');
        }

        // Gtoken digenerate
        const token = crypto.randomBytes(20).toString('hex');

        // update token ke database
        db.query('UPDATE akun SET reset_token = ? WHERE id = ?', [token, user.id], (error, result) => {
            if (error) {
                console.log(error);
                return res.status(500).send('Internal Server Error');
            }

            // sending lokal dengan token
            console.log('Reset Token:', token);
            res.status(200).json({
                message: 'Reset password berhasil',
                token: token 
            });
        });
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}

const resetPasswordUsers = async (req, res) => {
    const token = req.params.token;
    const newPassword = req.body.newPassword;

    try {
        const user = await UsersModel.getUserByResetToken(token);

        if (!user) {
            return res.status(400).send('Invalid or expired token');
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(newPassword, salt);

        db.query('UPDATE akun SET password = ?, reset_token = NULL WHERE id = ?', [hashedPassword, user.id], (error, result) => {
            if (error) {
                console.log(error);
                res.status(500).send('Internal Server Error');
            } else {
                res.send('Password reset successfully');
            }
        });
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
}



const updateUser = async (req, res) => {
    const userId = req.params.userId;
    const newFirstName = req.body.new_first_name;
    const newLastName = req.body.new_last_name;
    const newPassword = req.body.new_password;
    const newEmail = req.body.new_email;

    if (!newFirstName && !newLastName && !newPassword && !newEmail) {
        return res.status(400).send('Silahkan isi bagian yang kosong');
    }

    const updateFields = {};
    if (newFirstName) {
        updateFields.first_name = newFirstName;
    }
    if (newLastName) {
        updateFields.last_name = newLastName;
    }
    if (newPassword) {
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(req.body.new_password, salt);
        updateFields.password = hashedPassword;
    }
    if (newEmail) {
        const existingUser = await UsersModel.getUserByEmail(newEmail);
        if (existingUser) {
            res.status(400).send('Email is already registered');
            return;
        } else {
            updateFields.email = newEmail;
        }
    }

    db.query('UPDATE akun SET ? WHERE id = ?', [updateFields, userId], (error, result) => {
        if (error) {
            console.log(error);
            res.status(500).send('Internal Server Error');
        } else {
            if (result.affectedRows > 0) {
                res.send('User updated successfully');
            } else {
                res.status(404).send('User not found');
            }
        }
    });
}


module.exports = {
    getAllUsers,
    registerUsers,
    loginUsers,
    deleteUsers,
    forgotPasswordUsers,
    resetPasswordUsers,
    updateUser,
}
const express = require('express');
const router = express.Router();
const { getResponse } = require('../controllers/chatbotController');

router.post('/', getResponse);

module.exports = router;

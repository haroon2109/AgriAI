const express = require('express');
const router = express.Router();
const { proxyPredictYield, proxyDiseaseAlert } = require('../controllers/mlController');

router.post('/yield', proxyPredictYield);
router.post('/disease', proxyDiseaseAlert);

module.exports = router;

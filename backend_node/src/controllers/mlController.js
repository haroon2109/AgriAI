const axios = require('axios');
require('dotenv').config();

exports.proxyPredictYield = async (req, res) => {
  try {
    const response = await axios.post(`${process.env.FASTAPI_URL}/predict_yield`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error('FastAPI error:', err.message);
    res.status(500).json({ msg: 'Error connecting to ML service' });
  }
};

exports.proxyDiseaseAlert = async (req, res) => {
  try {
    const response = await axios.post(`${process.env.FASTAPI_URL}/disease_alert`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error('FastAPI error:', err.message);
    res.status(500).json({ msg: 'Error connecting to ML service' });
  }
};

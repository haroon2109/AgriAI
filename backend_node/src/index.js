const express = require('express');
const cors = require('cors');
const { connectDB, sequelize } = require('./config/db');
require('dotenv').config();

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Routes
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/products', require('./routes/productRoutes'));
app.use('/api/ml', require('./routes/mlRoutes'));
app.use('/api/chatbot', require('./routes/chatbotRoutes'));

const PORT = process.env.PORT || 5000;

const startServer = async () => {
  await connectDB();
  // Sync database models
  await sequelize.sync({ force: false }); 
  app.listen(PORT, () => console.log(`Backend server running on port ${PORT}`));
};

startServer();

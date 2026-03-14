const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: false,
  dialectOptions: {
    ssl: {
      require: true,
      rejectUnauthorized: false,
    },
  },
});

const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('PostgreSQL Connected...');
  } catch (err) {
    console.error('Unable to connect to the database:', err.message);
    // Continue for now even if it fails locally (mocking might be needed if no DB exists)
  }
};

module.exports = { sequelize, connectDB };

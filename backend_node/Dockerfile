FROM node:18-slim

WORKDIR /app

# Install production dependencies
COPY package*.json ./
RUN npm install --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Start server
CMD ["node", "src/index.js"]

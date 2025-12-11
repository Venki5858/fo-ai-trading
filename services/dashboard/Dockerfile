FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install -g serve
COPY src/ ./src
CMD ["serve", "-s", "src", "-l", "3000"]

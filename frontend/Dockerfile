FROM node:24-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install -g npm@latest && npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
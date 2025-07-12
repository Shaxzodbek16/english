FROM node:24 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM node:24

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app /app

RUN chmod +x ./run.sh

EXPOSE 3000

CMD ["./run.sh"]
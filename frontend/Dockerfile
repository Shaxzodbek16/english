FROM node:24

WORKDIR /app

COPY . .

RUN npm install

RUN chmod +x ./run.sh

EXPOSE 3000

CMD ["./run.sh"]
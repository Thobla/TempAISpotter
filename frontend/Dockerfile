FROM node:22.19
WORKDIR /app
EXPOSE 5173

COPY package*.json ./

RUN npm install

COPY . .


CMD ["npm", "run", "dev", "--", "--host"]

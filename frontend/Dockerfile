FROM node:16-alpine as builder

WORKDIR /app
ADD package.json .
ADD package-lock.json .

RUN npm i

ADD . .
RUN npm run build

FROM bitnami/nginx:1.23.0-debian-11-r5

EXPOSE 8080

COPY ./default.conf /opt/bitnami/nginx/conf/bitnami/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
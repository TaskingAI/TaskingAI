# Start with a Node.js 18.18 image as the build environment
FROM node:18.18 as build-stage

# Set the working directory in the Docker container
WORKDIR /app

# Copy package.json and package-lock.json (if available) to the working directory
COPY package*.json ./

# Install dependencies defined in package.json
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem
COPY . .

# Build the application for production
RUN npm run build

# Start with a lightweight version of Nginx on Alpine Linux
FROM nginx:alpine

# Copy the build artifacts from the previous stage to the Nginx server directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Create a custom Nginx configuration file to handle React Router
RUN echo $'server {\n\
    listen       80;\n\
    server_name  localhost;\n\
    location / {\n\
        root   /usr/share/nginx/html;\n\
        index  index.html index.htm;\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
    error_page   500 502 503 504  /50x.html;\n\
    location = /50x.html {\n\
        root   /usr/share/nginx/html;\n\
    }\n\
}' > /etc/nginx/conf.d/default.conf

# Expose port 80 to the Docker host, so it can be mapped to the Docker container
EXPOSE 80

# Start Nginx when the container is launched and keep it running
CMD ["nginx", "-g", "daemon off;"]

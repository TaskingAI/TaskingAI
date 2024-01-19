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

# Expose port 80 to the Docker host, so it can be mapped to the Docker container
EXPOSE 80

# Start Nginx when the container is launched and keep it running
CMD ["nginx", "-g", "daemon off;"]

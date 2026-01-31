# Stage 1: Build the Flutter web application
# Use a generic Ubuntu image instead of a pre-built Flutter image
FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y --fix-missing curl
RUN apt-get update && apt-get install -y --fix-missing git
RUN apt-get update && apt-get install -y --fix-missing unzip
RUN apt-get update && apt-get install -y --fix-missing xz-utils
RUN apt-get update && apt-get install -y --fix-missing zip
RUN apt-get update && apt-get install -y --fix-missing libglu1-mesa
# && rm -rf /var/lib/apt/lists/*

# Install Flutter SDK manually
RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter -b stable

# Add Flutter to PATH
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy dependency definitions first to leverage Docker cache
COPY pubspec.yaml pubspec.lock ./

# Install project dependencies
RUN flutter pub get

# Copy the rest of the application source code
COPY . .


# Def ARGs for environment variables
ARG BACKEND_URL

# Build the application for web
# 1. Enable web support in the container's Flutter config
RUN flutter config --enable-web
# 2. Re-initialize the project for the web platform to generate the 'web/' directory
RUN flutter create . --platforms web
# 3. Clean and build the release version
RUN flutter clean && flutter build web --release --dart-define=BACKEND_URL=$BACKEND_URL

# Stage 2: Serve the application using Nginx
# Use a lightweight Nginx image
FROM nginx:alpine AS runner

# Copy the built artifacts from the builder stage to the Nginx html directory
COPY --from=builder /app/build/web /usr/share/nginx/html
COPY config/nginx.conf /etc/nginx/
# Expose port 80 for the web server
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

# Use Microsoft's dev container base for optimal VS Code integration
FROM mcr.microsoft.com/devcontainers/python:3.12

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies and tools
RUN apt-get update && apt-get install -y \
    tree \
    htop \
    curl \
    git \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x (includes npm and npx)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install --upgrade pip uv

# Configure git for container usage
RUN git config --global --add safe.directory /workspace

# Set working directory
WORKDIR /workspace

# Default shell
CMD ["bash"]

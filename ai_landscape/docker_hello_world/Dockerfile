# Base image: Start with a Python image with GPU support
FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Set environment variables for Python and CUDA
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as the default Python
RUN ln -s /usr/bin/python3.9 /usr/bin/python

# Install Python libraries
RUN pip install --upgrade pip setuptools wheel

# Install Hugging Face and diffusers
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install diffusers transformers accelerate

# Add additional tools (optional)
RUN pip install numpy matplotlib pillow

# Clone a specific Hugging Face diffusion model (if needed)
RUN git clone https://github.com/huggingface/diffusers.git /app/diffusers

# Set the working directory
WORKDIR /app

# Copy your Python script or entry point
COPY run_diffusion.py /app/run_diffusion.py

# Set the default command
CMD ["python", "run_diffusion.py"]

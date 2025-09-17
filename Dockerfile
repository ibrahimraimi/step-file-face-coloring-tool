# syntax=docker/dockerfile:1.7
# Lightweight base image with micromamba for fast conda env creation
FROM mambaorg/micromamba:latest AS base

# Ensure non-interactive builds
ARG DEBIAN_FRONTEND=noninteractive
# Let `RUN micromamba ...` auto-activate env in subsequent RUN steps
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Create a dedicated working directory
WORKDIR /app

# --- Layer 1: Copy only environment files to leverage caching ---
# Copy environment.yml (conda deps) and requirements.txt (pip deps)
COPY environment.yml /tmp/environment.yml
COPY requirements.txt /tmp/requirements.txt

# --- Layer 2: Create conda environment (cached when environment.yml unchanged) ---
# Create a single environment named `step-env` using environment.yml
RUN micromamba create -y -n step-env -f /tmp/environment.yml \
    && micromamba clean --all --yes

# --- Layer 3: Install pip packages into the same environment (cached on requirements changes) ---
RUN micromamba run -n step-env python -m pip install --upgrade pip \
    && micromamba run -n step-env pip install --no-cache-dir -r /tmp/requirements.txt

# --- Layer 4: Copy project sources (invalidates only when source files change) ---
COPY . /app

# Optional: ensure run scripts are executable if present
RUN set -eux; \
    if [ -f /app/run.sh ]; then chmod +x /app/run.sh; fi; \
    if [ -f /app/setup.sh ]; then chmod +x /app/setup.sh; fi

# Clean up any build caches to keep the image small
RUN micromamba clean --all --yes \
    && rm -rf /root/.cache /opt/conda/pkgs

# Default command uses micromamba to run inside the `step-env` environment
# This makes it easy to override at runtime: `docker run <img> python other.py`
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "micromamba", "run", "-n", "step-env", "--"]
CMD ["python", "main.py"]

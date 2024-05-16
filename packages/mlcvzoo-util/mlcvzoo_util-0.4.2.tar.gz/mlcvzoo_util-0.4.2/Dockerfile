FROM nexus.apps.sele.iml.fraunhofer.de/sele/ml-toolbox/cicd/mlcvzoo-ci-image:latest

# Define paths. Let all path definitions always end with a '/'!

# Path to all code we will place in this container image
ENV BUILD_ENV_DIR="/build-env/"
# Path to the actual project
ENV PROJECT_DIR="${BUILD_ENV_DIR}MLCVZoo/mlcvzoo-util/"
# Create those locations
RUN mkdir -p "$PROJECT_DIR" "${PROJECT_DIR}requirements_locked"

WORKDIR "$PROJECT_DIR"

COPY requirements_locked ./requirements_locked


ENV VIRTUAL_ENV="${BUILD_ENV_DIR}venv"
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV REQUIREMENTS_FILE="${PROJECT_DIR}requirements_locked/requirements-lock-uv-py310-all.txt"
RUN python3 -m venv "$VIRTUAL_ENV" \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install uv \
    && python3 -m uv pip sync "$REQUIREMENTS_FILE"

# Cleanup uv cache
RUN uv cache clean

# We don't deliver unit tests so even without --no-root we would need to set the PYTHONPATH here
ENV PYTHONPATH="$PYTHONPATH:$PROJECT_DIR"

# ====================================================================
# Label the image
LABEL org.opencontainers.image.authors="Maximilian Otten <maximilian.otten@iml.fraunhofer.de>, Christian Hoppe <christian.hoppe@iml.fraunhofer.de" \
      org.opencontainers.image.vendor="Fraunhofer IML" \
      org.opencontainers.image.title="MLCVZoo Util - GPU-enabled gitlab-runner container" \
      org.opencontainers.image.description="Container image for GPU enabled integration testing and continuous delivery for MLCVZoo-Util"

#!/bin/sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 POETRY_ARGS"
  return 1
fi

# Install yolox afterwards as it fails in poetry due to pep517, and others fail without it:
poetry "$@"

# Workaround for torch bug: https://github.com/pytorch/pytorch/pull/99980
export TORCH_DIR=$(poetry run python3 -c "import torch;import os;print(os.path.dirname(torch.__file__))")
sed -i "s/except (FileNotFoundError, PermissionError)/except (FileNotFoundError, PermissionError, NotADirectoryError)/" "$TORCH_DIR/utils/hipify/cuda_to_hip_mappings.py"


# Reinstall mmcv with legacy setup afterwards as the variant installed with poetry fails to run
if python -c "import mmcv" &> /dev/null; then
  poetry run python -m pip uninstall -y mmcv
  # Ensure setuptools and wheel
  poetry run python -m pip install setuptools wheel
  # TODO: Check if MMCV_WITH_OPS is still necessary with mmcv >= 2.0
  MMCV_WITH_OPS=1 poetry run python -m pip install \
    --no-cache \
    --no-cache-dir \
    --no-binary :all: \
    --no-deps \
    --no-build-isolation \
    --no-use-pep517 \
    mmcv=="$(poetry show mmcv | grep version | awk '{print $3}')"
fi

# Install YOLOX - due to bugs it is not a direct dependency of mlcvzoo-yolox anymore
if python -c "import mlcvzoo_yolox" &> /dev/null; then
  # Ensure setuptools and wheel
  poetry run python -m pip install setuptools wheel
  poetry run pip install \
    --no-cache \
    --no-cache-dir \
    --no-deps \
    --no-build-isolation \
    --no-use-pep517 \
    "git+https://github.com/Megvii-BaseDetection/YOLOX.git@419778480ab6ec0590e5d3831b3afb3b46ab2aa3"
fi

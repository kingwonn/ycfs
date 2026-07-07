#!/usr/bin/env bash
# build.sh — 一条命令无头构建(F1 验收:可复现构建)
set -euo pipefail
cd "$(dirname "$0")"

cmake -B build -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_TOOLCHAIN_FILE=cmake/arm-none-eabi.cmake >/dev/null
cmake --build build --parallel

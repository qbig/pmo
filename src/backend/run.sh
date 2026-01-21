#!/bin/bash
# Simple startup script for PMO backend

cd "$(dirname "$0")"
python -m src.backend.main

#!/bin/bash
# Streamlit startup script with proper configuration

# Clear cache
streamlit cache clear

# Run with proper flags
streamlit run app.py ^
    --client.showErrorDetails=true ^
    --logger.level=info ^
    --server.enableCORS=true ^
    --telemetry.enabled=false ^
    --client.toolbarMode=minimal


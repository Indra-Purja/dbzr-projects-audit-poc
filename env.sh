#!/bin/sh
export SERVICE_NAME=dbzr-projects-audit
export REGION_NAME=babylon-office
export ENV_NAME=local
export SERVICE_PORT=8000
export TRACING_ENABLED=true
export TRACING_SAMPLE_RATE=1
export "TRACING_STATIC_TAGS=env=local;user=$(whoami)"
export TRACING_COLLECTOR_URL=https://dev-jaeger.ops.babylontech.co.uk:9411/
export METRICS_ENABLED=true
export DEBUG=true
export SWAGGER_UI=true


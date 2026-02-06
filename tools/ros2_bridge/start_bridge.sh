#!/bin/bash

set -eu

DOCKER_COMPOSE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${DOCKER_COMPOSE_DIR}"

usage() {
    echo "Usage: $0 KACHAKA_IP_ADRESS [KACHAKA_NAME] [KACHAKA_STATE] [USE_MAP] [Option]"
    echo "  KACHAKA_NAME:  kachaka"
    echo "  KACHAKA_STATE: yes/no"
    echo "  USE_MAP:       yes/no"
    echo "  -d             daemonize"
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

if [[ $# -lt 2 ]]; then
    NAMESPACE="kachaka"
    FRAME_PREFIX=''
else
    NAMESPACE=$2
    FRAME_PREFIX=$2"/"
fi

if [[ $# -lt 3 ]]; then
    KACHAKA_STATE="yes"
else
    KACHAKA_STATE=$3
fi

if [[ $# -lt 4 ]]; then
    USE_MAP="True"
else
    if [[ $4 == "yes" ]]; then
        USE_MAP="True"
    else
        USE_MAP="False"
    fi
fi

if [[ "${KACHAKA_STATE}" == "yes" ]]; then
    LAUNCHER_CMD="bridge"
else
    LAUNCHER_CMD="bridge_no_state"
fi

USER_ID="$(id -u)"
GROUP_ID="$(id -g)"
GRPC_PORT=26400

export USER_ID
export GROUP_ID

KACHAKA_IP=$1

if command -v docker-compose; then
    API_GRPC_BRIDGE_SERVER_URI="${KACHAKA_IP}:${GRPC_PORT}" NAMESPACE="${NAMESPACE}" FRAME_PREFIX="${FRAME_PREFIX}" LAUNCHER_CMD="${LAUNCHER_CMD}" USE_MAP="${USE_MAP}" docker-compose up "${@:5}" ros2_bridge
else
    API_GRPC_BRIDGE_SERVER_URI="${KACHAKA_IP}:${GRPC_PORT}" NAMESPACE="${NAMESPACE}" FRAME_PREFIX="${FRAME_PREFIX}" LAUNCHER_CMD="${LAUNCHER_CMD}" USE_MAP="${USE_MAP}" docker compose up "${@:5}" ros2_bridge
fi

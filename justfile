set windows-shell := ["powershell", "-NoProfile", "-Command"]
set dotenv-load := true

COMMON_URL := 'https://raw.githubusercontent.com/esclient/tools/refs/heads/main/python/common.just'

PROTO_TAG := 'v0.0.17'
PROTO_NAME := 'comment.proto'
TMP_DIR := '.proto'
OUT_DIR := 'src/commentservice/grpc'
SERVICE_NAME := 'comment'

# dbmate via Docker
DBMATE_IMAGE := 'ghcr.io/amacneil/dbmate:2'
DBMATE_RUN := if os() == 'windows' {
  'docker run --rm -e DATABASE_URL=$env:DATABASE_URL -v ${PWD}:/work -w /work ' + DBMATE_IMAGE
} else {
  'docker run --rm -e DATABASE_URL=$DATABASE_URL -v $(pwd):/work -w /work ' + DBMATE_IMAGE
}

MKDIR_DOTJUST := if os() == 'windows' {
  'New-Item -ItemType Directory -Force -Path ".just" | Out-Null'
} else {
  'mkdir -p .just'
}

FETCH_CMD := if os() == 'windows' {
  'Invoke-WebRequest -Uri ' + COMMON_URL + ' -OutFile .just/common.just'
} else {
  'curl -fsSL ' + COMMON_URL + ' -o .just/common.just'
}

import? '.just/common.just'

default:
    @just --list

fetch-common:
    {{ MKDIR_DOTJUST }}
    {{ FETCH_CMD }}

# --- Migrations (dbmate) ---

# Pull dbmate image (optional)
dbmate-pull:
    docker pull {{ DBMATE_IMAGE }}

# Create a new migration: just migrate-new "add_users"
migrate-new name:
    {{ DBMATE_RUN }} new {{ name }}

# Apply all migrations
migrate-up:
    {{ DBMATE_RUN }} up

# Roll back the most recent migration
migrate-down:
    {{ DBMATE_RUN }} down

# Show migration status
migrate-status:
    {{ DBMATE_RUN }} status

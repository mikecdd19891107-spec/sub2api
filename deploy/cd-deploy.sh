#!/usr/bin/env bash
# Idempotent CD deploy for /srv/agentbyte on jp-app-01.
# Syncs origin/main, rebuilds from local Dockerfile via compose CD override, health-checks.
set -euo pipefail

REPO_DIR="${REPO_DIR:-/srv/agentbyte}"
DEPLOY_DIR="${DEPLOY_DIR:-$REPO_DIR/deploy}"
BRANCH="${BRANCH:-main}"
REMOTE="${REMOTE:-origin}"
COMPOSE_BASE="docker-compose.local.yml"
COMPOSE_CD="docker-compose.cd.yml"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8080/health}"
SKIP_BUILD="${SKIP_BUILD:-0}"
SKIP_GIT="${SKIP_GIT:-0}"
MAX_WAIT="${MAX_WAIT:-180}"

log() { printf '[cd-deploy] %s\n' "$*"; }
die() { printf '[cd-deploy] ERROR: %s\n' "$*" >&2; exit 1; }

if docker info >/dev/null 2>&1; then
  DOCKER=(docker)
elif sudo -n docker info >/dev/null 2>&1; then
  DOCKER=(sudo docker)
else
  die "cannot talk to docker daemon (add user to docker group or configure sudo)"
fi

command -v curl >/dev/null || die "curl not found"
[ -d "$REPO_DIR/.git" ] || die "not a git repo: $REPO_DIR"
[ -f "$DEPLOY_DIR/$COMPOSE_BASE" ] || die "missing $DEPLOY_DIR/$COMPOSE_BASE"
[ -f "$DEPLOY_DIR/.env" ] || die "missing $DEPLOY_DIR/.env (refusing to start without secrets)"

cd "$REPO_DIR"

if [ "$SKIP_GIT" != "1" ]; then
  log "fetch $REMOTE"
  git fetch --prune "$REMOTE"
  log "reset --hard $REMOTE/$BRANCH"
  git reset --hard "$REMOTE/$BRANCH"
  # Keep runtime data + secrets + local drafts
  git clean -fd \
    -e 'deploy/data' \
    -e 'deploy/postgres_data' \
    -e 'deploy/redis_data' \
    -e 'deploy/.env' \
    -e 'deploy/*.draft' \
    || true
  log "now at $(git rev-parse --short HEAD) $(git log -1 --pretty=%s)"
else
  log "SKIP_GIT=1 — using working tree as-is at $(git rev-parse --short HEAD)"
fi

cd "$DEPLOY_DIR"

compose() {
  "${DOCKER[@]}" compose -f "$COMPOSE_BASE" -f "$COMPOSE_CD" "$@"
}
compose_base() {
  "${DOCKER[@]}" compose -f "$COMPOSE_BASE" "$@"
}

if [ "$SKIP_BUILD" = "1" ]; then
  log "SKIP_BUILD=1 — restarting without rebuild"
  if "${DOCKER[@]}" image inspect agentbyte:cd >/dev/null 2>&1; then
    compose up -d --remove-orphans
  else
    log "agentbyte:cd not built yet; using base compose (Hub image ghcr.io/mikecdd19891107-spec/agentbyte)"
    compose_base up -d --remove-orphans
  fi
else
  [ -f "$COMPOSE_CD" ] || die "missing $COMPOSE_CD — commit/push docker-compose.cd.yml first"
  log "build + up from local Dockerfile (tag agentbyte:cd)"
  compose build agentbyte
  compose up -d --remove-orphans
fi

log "waiting for health: $HEALTH_URL"
ok=0
code=""
for i in $(seq 1 "$MAX_WAIT"); do
  code=$(curl -sS -o /tmp/agentbyte-health.body -w '%{http_code}' "$HEALTH_URL" || true)
  if [ "$code" = "200" ]; then
    ok=1
    break
  fi
  sleep 1
done
[ "$ok" = "1" ] || die "health check failed after ${MAX_WAIT}s (last HTTP ${code:-none})"
log "health OK: $(cat /tmp/agentbyte-health.body 2>/dev/null || true)"
log "containers:"
"${DOCKER[@]}" ps --filter name=agentbyte --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

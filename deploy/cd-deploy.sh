#!/usr/bin/env bash
# Idempotent CD deploy for /srv/sub2api on jp-app-01.
# Syncs origin/main, rebuilds from local Dockerfile via compose CD override, health-checks.
set -euo pipefail

REPO_DIR="${REPO_DIR:-/srv/sub2api}"
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
  [ -z "$(git status --porcelain --untracked-files=no)" ] || die "tracked files have local changes"
  git fetch "$REMOTE" "$BRANCH"
  git merge --ff-only FETCH_HEAD
  log "now at $(git rev-parse --short HEAD) $(git log -1 --pretty=%s)"
else
  log "SKIP_GIT=1 — using working tree as-is at $(git rev-parse --short HEAD)"
fi

export DEPLOY_COMMIT
DEPLOY_COMMIT=$(git rev-parse HEAD)
[ -z "${EXPECTED_COMMIT:-}" ] || [ "$DEPLOY_COMMIT" = "$EXPECTED_COMMIT" ] || die "checkout does not match expected commit"
export DEPLOY_VERSION
DEPLOY_VERSION=$(tr -d '\r\n' < backend/cmd/server/VERSION)
[ -n "$DEPLOY_VERSION" ] || die "empty version"

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
    compose up -d --no-deps agentbyte
  else
    log "agentbyte:cd not built yet; using base compose (Hub image ghcr.io/mikecdd19891107-spec/agentbyte)"
    compose_base up -d --no-deps agentbyte
  fi
else
  [ -f "$COMPOSE_CD" ] || die "missing $COMPOSE_CD — commit/push docker-compose.cd.yml first"
  log "build from local Dockerfile (tag agentbyte:cd)"
  compose build agentbyte
  # Preserve the live database before starting a version that may run migrations.
  BACKUP_DIR="${BACKUP_DIR:-$REPO_DIR/backups}"
  umask 077
  mkdir -p "$BACKUP_DIR"
  backup="$BACKUP_DIR/agentbyte-$(date -u +%Y%m%dT%H%M%SZ)-${DEPLOY_COMMIT:0:12}.dump"
  log "backing up PostgreSQL to $backup"
  "${DOCKER[@]}" exec agentbyte-postgres sh -c 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$backup"
  [ -s "$backup" ] || die "database backup is empty"
  "${DOCKER[@]}" exec -i agentbyte-postgres pg_restore --list < "$backup" > /dev/null || die "database backup is invalid"
  log "starting application with existing database and Redis"
  compose up -d --no-deps agentbyte
fi

log "waiting for health: $HEALTH_URL"
ok=0
code=""
for i in $(seq 1 "$MAX_WAIT"); do
  code=$(curl --noproxy '*' -sS -o /dev/null -w '%{http_code}' "$HEALTH_URL" || true)
  if [ "$code" = "200" ]; then
    ok=1
    break
  fi
  sleep 1
done
[ "$ok" = "1" ] || die "health check failed after ${MAX_WAIT}s (last HTTP ${code:-none})"
log "health OK"
if [ "$SKIP_BUILD" != "1" ]; then
  version=$("${DOCKER[@]}" exec agentbyte /app/agentbyte -version 2>&1)
  [[ "$version" == *"commit: $DEPLOY_COMMIT"* ]] || die "running application does not report expected commit"
  log "running version verified: $DEPLOY_VERSION ($DEPLOY_COMMIT)"
fi
log "containers:"
"${DOCKER[@]}" ps --filter name=agentbyte --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

#!/usr/bin/env bash
# 从原项目 Wei-Shaw/sub2api 挑选提交合并到 AgentByte。
#
# 原理：对上游提交改动的每个文件，把改动前后两个版本都套用
# tools/rebrand/rebrand.py 的同一套改名规则（并 gofmt），再与当前文件三方合并。
# 改名和 import 排序不会再造成冲突，只有你自己改过的代码才可能需要手动处理。
#
# 用法：
#   tools/sync-upstream.sh --list              列出上次同步之后上游的新提交
#   tools/sync-upstream.sh <commit> [...]      应用一个或多个上游提交
#   tools/sync-upstream.sh <from>..<to>        应用一段提交
#
# 依赖：git、python3；处理 Go 文件时会用到 gofmt（装了 Go 就有）。
# 上游改了 plugin.proto 时，*.pb.go 会被跳过，需要在 backend/pkg/pluginapi/v1 下重新生成：
#   protoc --go_out=. --go_opt=paths=source_relative \
#          --go-grpc_out=. --go-grpc_opt=paths=source_relative plugin.proto
set -euo pipefail
exec python3 "$(dirname "$0")/rebrand/sync_upstream.py" "$@"

#!/usr/bin/env python3
"""AgentByte rebrand rules (sub2api -> AgentByte).

The same rules are used for the one-off rename of this repository and by
tools/sync-upstream.sh to rewrite upstream (Wei-Shaw/sub2api) patches before
applying them, so upstream fixes keep applying cleanly after the rename.

Usage:
  rebrand.py --apply            rewrite tracked files in place + rename paths
  rebrand.py --check            list remaining occurrences outside the allowlist
  rebrand.py --stdin            rewrite a patch / text read from stdin to stdout
"""
import fnmatch
import os
import re
import subprocess
import sys

NEW_MODULE = 'github.com/mikecdd19891107-spec/agentbyte'
NEW_REPO = 'mikecdd19891107-spec/agentbyte'
NEW_IMAGE = 'ghcr.io/mikecdd19891107-spec/agentbyte'

# Files that are never rewritten.
SKIP_FILES = {
    'LICENSE',
    'CLA.md',  # upstream contributor agreement naming the upstream owner; not ours to rename
    'NOTICE.md',
    'tools/rebrand/rebrand.py',
    'tools/rebrand/pbdesc.py',
    'tools/rebrand/sync_upstream.py',
    'tools/sync-upstream.sh',
}
SKIP_PREFIXES = ('backend/internal/web/dist/', 'frontend/dist/', 'frontend/node_modules/')

# Text kept verbatim everywhere: third-party projects and external services
# whose real names contain "sub2api".
GLOBAL_KEEP = [
    r'touwaeriol/sub2apipay', r'Sub2ApiPay', r'sub2apipay',
    r'ckken/sub2api-mobile', r'sub2api-mobile',
    r'tls\.sub2api\.org',
    r'Wei-Shaw/model-price-repo',  # external pricing data source
    r'\[sub2api\]\(https://github\.com/Wei-Shaw/sub2api\)',  # attribution link in README
    r'upstream sub2api', r'其他 sub2api', r'other sub2api',
]

# Per-file text kept verbatim: describes or talks to *other* sub2api servers
# (upstream relays), so renaming would break interoperability or meaning.
FILE_KEEP = {
    # Probe of upstream sub2api relays: protocol path/object must stay.
    'backend/internal/service/upstream_billing_probe*.go': [
        r'/v1/sub2api/billing', r'sub2api\.key_billing',
        r'[Ss]ub2[Aa][Pp][Ii](?![-/A-Za-z])',  # prose about upstream sub2api relays
    ],
    'frontend/src/components/account/UpstreamBillingRateCell.vue': [r'sub2api'],
    'frontend/src/components/account/BulkEditAccountModal.vue': [r'sub2api(?: 上游|/billing)', r'/v1/sub2api/billing'],
    'frontend/src/components/account/EditAccountModal.vue': [r'sub2api 上游'],
    'frontend/src/components/account/*UpstreamRequestIdHeaderField*': [r"label: 'sub2api'", r"'sub2api'", r'sub2apiNote'],
    'frontend/src/i18n/locales/*/admin/accounts.ts': [r'sub2apiNote'],
    # Legacy import formats from other sub2api deployments.
    'backend/internal/handler/admin/account_data.go': [r'legacySub2API\w+(?:\s*=\s*"sub2api-(?:data|bundle)")?'],
    'frontend/src/components/admin/account/ImportDataModal.vue': [r'LEGACY_SUB2API_DATA_TYPES(?: = \[[^\]]*\])?'],
}

# Ordered replacement rules (applied after masking the keep-lists).
RULES = [
    (r'github\.com/Wei-Shaw/sub2api', NEW_MODULE),
    (r'raw\.githubusercontent\.com/Wei-Shaw/sub2api', 'raw.githubusercontent.com/' + NEW_REPO),
    (r'api\.github\.com/repos/Wei-Shaw/sub2api', 'api.github.com/repos/' + NEW_REPO),
    (r'github\.com/weishaw/sub2api', 'github.com/' + NEW_REPO),
    (r'Wei-Shaw%2Fsub2api', 'mikecdd19891107-spec%2Fagentbyte'),
    (r'Wei-Shaw/sub2api', NEW_REPO),
    (r'weishaw/sub2api', NEW_IMAGE),
    (r'Wei-Shaw <github\.com/Wei-Shaw>', 'mikecdd19891107-spec <github.com/mikecdd19891107-spec>'),
    (r'SUB2API', 'AGENTBYTE'),
    (r'Sub2API', 'AgentByte'),
    (r'Sub2Api', 'AgentByte'),
    (r'Sub2api', 'Agentbyte'),
    (r'sub2API', 'agentByte'),
    (r'sub2Api', 'agentByte'),
    (r'sub2api', 'agentbyte'),
    (r'\bsub2ap\b', 'agentbyte'),
]
_RULES = [(re.compile(p), r) for p, r in RULES]


def _keep_patterns(path):
    pats = list(GLOBAL_KEEP)
    for glob, extra in FILE_KEEP.items():
        if path and fnmatch.fnmatch(path, glob):
            pats.extend(extra)
    return re.compile('|'.join('(?:%s)' % p for p in pats))


def transform(text, path=None):
    keep = _keep_patterns(path)
    saved = []

    def mask(m):
        saved.append(m.group(0))
        return '\x00KEEP%d\x00' % (len(saved) - 1)

    text = keep.sub(mask, text)
    for rx, rep in _RULES:
        text = rx.sub(rep, text)
    return re.sub(r'\x00KEEP(\d+)\x00', lambda m: saved[int(m.group(1))], text)


def transform_patch(text):
    """Rewrite a git patch, applying per-file keep rules to each file section."""
    out = []
    for chunk in re.split(r'(?m)^(?=diff --git )', text):
        m = re.match(r'diff --git a/(\S+) b/', chunk)
        path = m.group(1) if m else None
        if path and is_skipped(path):
            out.append(chunk)
        else:
            out.append(transform(chunk, path))
    return ''.join(out)


def transform_path(path):
    parts = path.split('/')
    return '/'.join(transform(p) for p in parts)


def tracked_files():
    out = subprocess.run(['git', 'ls-files', '-z'], capture_output=True, check=True).stdout
    return [p for p in out.decode().split('\0') if p]


def is_skipped(path):
    return path in SKIP_FILES or path.startswith(SKIP_PREFIXES)


def read_text(path):
    with open(path, 'rb') as f:
        data = f.read()
    if b'\0' in data:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def apply():
    sys.dont_write_bytecode = True
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    changed, renamed = 0, []
    for path in tracked_files():
        if is_skipped(path) or not os.path.isfile(path):
            continue
        if path.endswith('.pb.go') and 'rawDesc' in open(path, encoding='utf-8').read():
            import pbdesc  # needs: pip install protobuf
            pbdesc.rewrite(path, 'sub2api.plugin.v1', 'agentbyte.plugin.v1',
                           'github.com/Wei-Shaw/sub2api', NEW_MODULE)
        text = read_text(path)
        if text is not None:
            new = transform(text, path)
            if new != text:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new)
                changed += 1
        new_path = transform_path(path)
        if new_path != path:
            renamed.append((path, new_path))
    for old, new in renamed:
        os.makedirs(os.path.dirname(new) or '.', exist_ok=True)
        os.rename(old, new)
    for old, _ in renamed:  # remove now-empty directories
        d = os.path.dirname(old)
        while d and os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)
            d = os.path.dirname(d)
    print(f'rewrote {changed} files, renamed {len(renamed)} paths')
    for old, new in renamed:
        print(f'  {old} -> {new}')


def check():
    rx = re.compile(r'sub2api|wei-shaw|weishaw', re.I)
    left = 0
    for path in tracked_files():
        if is_skipped(path) or not os.path.isfile(path):
            continue
        text = read_text(path)
        if text is None:
            continue
        keep = _keep_patterns(path)
        masked = keep.sub('', text)
        for i, line in enumerate(masked.splitlines(), 1):
            if rx.search(line):
                left += 1
                print(f'{path}:{i}: {line.strip()[:160]}')
    print(f'{left} lines outside the allowlist')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else '--help'
    if mode == '--apply':
        apply()
    elif mode == '--check':
        check()
    elif mode == '--stdin':
        sys.stdout.write(transform_patch(sys.stdin.read()))
    else:
        print(__doc__)

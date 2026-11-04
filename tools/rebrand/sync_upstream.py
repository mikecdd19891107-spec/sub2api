#!/usr/bin/env python3
"""Cherry-pick commits from upstream sub2api into AgentByte.

For every file an upstream commit touches, both the "before" and "after"
upstream versions are rewritten with the rebrand rules (and gofmt for .go
files), then three-way merged into the current file with `git merge-file`.
Because the merge base already carries the rename, renamed identifiers and
re-sorted imports never conflict; only your own customisations can.

Usage (normally via tools/sync-upstream.sh):
  sync_upstream.py [--no-fetch] --list
  sync_upstream.py [--no-fetch] <commit|from..to> [...]
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rebrand  # noqa: E402

UPSTREAM_URL = 'https://github.com/Wei-Shaw/sub2api.git'
UPSTREAM_REF = 'upstream/main'
MARKER = '.upstream-synced'


def git(*args, check=True, text=True, input=None):
    r = subprocess.run(['git', *args], capture_output=True, text=text, input=input)
    if check and r.returncode != 0:
        raise SystemExit(f'git {" ".join(args)} failed:\n{r.stderr}')
    return r


def show(rev, path):
    r = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def gofmt(text):
    if not shutil.which('gofmt'):
        return text
    r = subprocess.run(['gofmt'], input=text, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else text


def rebranded(data, path):
    """Upstream blob -> AgentByte form. Returns bytes; binary data is unchanged."""
    if data is None:
        return None
    if b'\0' in data:
        return data
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return data
    new_path = rebrand.transform_path(path)
    if rebrand.is_skipped(new_path):
        return data
    text = rebrand.transform(text, new_path)
    if new_path.endswith('.go'):
        text = gofmt(text)
    return text.encode('utf-8')


def merge3(ours, base, theirs):
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (('ours', ours), ('base', base), ('theirs', theirs)):
            p = os.path.join(d, name)
            with open(p, 'wb') as f:
                f.write(data or b'')
            paths.append(p)
        r = subprocess.run(['git', 'merge-file', '-p', '-L', 'AgentByte', '-L', 'upstream-base',
                            '-L', 'upstream', *paths], capture_output=True)
        return r.stdout, r.returncode  # returncode = number of conflicts (<0 on error)


def commits_for(args):
    out = []
    for a in args:
        if '..' in a:
            revs = git('rev-list', '--reverse', '--no-merges', a).stdout.split()
        else:
            revs = [git('rev-parse', a).stdout.strip()]
        out.extend(revs)
    return out


def apply_commit(sha):
    parent = git('rev-parse', f'{sha}^').stdout.strip()
    subject = git('log', '-1', '--format=%s', sha).stdout.strip()
    print(f'==> {sha[:10]} {subject}')
    changes = git('diff-tree', '--no-commit-id', '-r', '-M', '--name-status', parent, sha).stdout.splitlines()
    conflicts, warnings = [], []
    for line in changes:
        parts = line.split('\t')
        status = parts[0][0]
        old_path = parts[1]
        new_path = parts[2] if status in 'RC' else parts[1]
        ours_path = rebrand.transform_path(new_path)
        old_ours_path = rebrand.transform_path(old_path)

        if new_path.endswith('.pb.go'):
            warnings.append(f'{ours_path}: protobuf 生成代码已跳过，请根据 .proto 重新生成')
            continue

        base = rebranded(show(parent, old_path), old_path) if status != 'A' else b''
        theirs = rebranded(show(sha, new_path), new_path) if status != 'D' else None

        if status == 'D':
            if os.path.exists(ours_path):
                with open(ours_path, 'rb') as f:
                    current = f.read()
                if current == base:
                    os.remove(ours_path)
                else:
                    warnings.append(f'{ours_path}: 上游删除了此文件，但你改过它，已保留，请自行决定')
            continue

        if status == 'R' and old_ours_path != ours_path and os.path.exists(old_ours_path):
            os.makedirs(os.path.dirname(ours_path) or '.', exist_ok=True)
            os.rename(old_ours_path, ours_path)

        if not os.path.exists(ours_path):
            os.makedirs(os.path.dirname(ours_path) or '.', exist_ok=True)
            with open(ours_path, 'wb') as f:
                f.write(theirs)
            if status not in 'AC':
                warnings.append(f'{ours_path}: 本地不存在，已直接使用上游版本')
            continue

        with open(ours_path, 'rb') as f:
            ours = f.read()
        if b'\0' in theirs or b'\0' in ours:
            if ours == base:
                with open(ours_path, 'wb') as f:
                    f.write(theirs)
            else:
                conflicts.append(f'{ours_path}（二进制文件，两边都改过）')
            continue
        merged, n = merge3(ours, base, theirs)
        with open(ours_path, 'wb') as f:
            f.write(merged)
        if n != 0:
            conflicts.append(ours_path)

    for w in warnings:
        print('    注意：' + w)
    if conflicts:
        print('\n以下文件有冲突（已写入 <<<<<<< 冲突标记）：')
        for c in conflicts:
            print('    ' + c)
        print('\n手动解决后执行：git add -A && git commit -C ' + sha + '，然后继续同步剩下的提交。')
        return False

    git('add', '-A')
    if not git('diff', '--cached', '--quiet', check=False).returncode:
        print('    （无实际改动，跳过）')
        return True
    msg = git('log', '-1', '--format=%B', sha).stdout.rstrip() + f'\n\n(cherry picked from upstream sub2api {sha})\n'
    author = git('log', '-1', '--format=%an <%ae>', sha).stdout.strip()
    date = git('log', '-1', '--format=%aI', sha).stdout.strip()
    git('commit', '-q', '--author', author, '--date', date, '-F', '-', input=msg)
    return True


def main():
    args = sys.argv[1:]
    os.chdir(git('rev-parse', '--show-toplevel').stdout.strip())
    fetch = True
    if args and args[0] == '--no-fetch':
        fetch = False
        args = args[1:]
    if fetch:
        if git('remote', 'get-url', 'upstream', check=False).returncode != 0:
            git('remote', 'add', 'upstream', UPSTREAM_URL)
        git('fetch', '--quiet', 'upstream', 'main')

    if not args or args[0] == '--list':
        if os.path.exists(MARKER):
            base = open(MARKER).read().strip()
            print(f'上次同步到：{base}')
            print(git('log', '--oneline', '--no-merges', f'{base}..{UPSTREAM_REF}').stdout)
        else:
            print('还没有同步记录。上游最近 30 个提交：')
            print(git('log', '--oneline', '--no-merges', '-30', UPSTREAM_REF).stdout)
            print(f'确认当前代码对应的上游提交后，执行 echo <commit> > {MARKER} 记录起点。')
        return

    if git('status', '--porcelain').stdout.strip():
        raise SystemExit('工作区有未提交的改动，请先提交或暂存后再同步。')

    done = None
    for sha in commits_for(args):
        if not apply_commit(sha):
            sys.exit(1)
        done = sha
    if done:
        with open(MARKER, 'w') as f:
            f.write(done + '\n')
        git('add', MARKER)
        git('commit', '-q', '-m', f'chore: record upstream sync position {done[:10]}')
        print(f'\n完成，同步位置已记录到 {MARKER}。')


if __name__ == '__main__':
    main()

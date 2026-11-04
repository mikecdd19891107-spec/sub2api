"""Rewrite the embedded FileDescriptorProto (rawDesc) in a protoc-gen-go *.pb.go file.

A plain text replace would corrupt it: the descriptor is length-prefixed binary.
This parses it with the protobuf library (pip install protobuf), renames the
proto package, and re-encodes it exactly the way protoc-gen-go does.

Usage: pbdesc.py <file.pb.go> <old_pkg> <new_pkg> <old_go_pkg> <new_go_pkg>
       pbdesc.py --selftest <file.pb.go>
"""
import re, sys, unicodedata
from google.protobuf import descriptor_pb2

START_RX = re.compile(r'const file_\w+_rawDesc = "" \+\n')

def go_unquote(lit):
    assert lit[0] == lit[-1] == '"'
    s = lit[1:-1]; out = bytearray(); i = 0
    simple = {'a':7,'b':8,'f':12,'n':10,'r':13,'t':9,'v':11,'\\':92,'"':34,"'":39}
    while i < len(s):
        c = s[i]
        if c != '\\':
            out += c.encode('utf-8'); i += 1; continue
        n = s[i+1]
        if n in simple: out.append(simple[n]); i += 2
        elif n == 'x': out.append(int(s[i+2:i+4], 16)); i += 4
        elif n in '01234567': out.append(int(s[i+1:i+4], 8)); i += 4
        elif n == 'u': out += chr(int(s[i+2:i+6], 16)).encode(); i += 6
        elif n == 'U': out += chr(int(s[i+2:i+10], 16)).encode(); i += 10
        else: raise ValueError(n)
    return bytes(out)

def is_print(ch):
    if ch == ' ': return True
    cat = unicodedata.category(ch)
    return not (cat.startswith('C') or cat.startswith('Z'))

def go_quote(b):
    out = ['"']; i = 0
    esc = {7:'\\a',8:'\\b',12:'\\f',10:'\\n',13:'\\r',9:'\\t',11:'\\v'}
    while i < len(b):
        x = b[i]
        if x < 0x80:
            ch = chr(x)
            if ch in '"\\': out.append('\\' + ch)
            elif 0x20 <= x < 0x7f: out.append(ch)
            elif x in esc: out.append(esc[x])
            else: out.append('\\x%02x' % x)
            i += 1; continue
        # try decode a utf-8 rune
        for w in (2, 3, 4):
            try:
                ch = b[i:i+w].decode('utf-8')
                if len(ch) == 1: break
            except UnicodeDecodeError:
                ch = None
        else:
            ch = None
        if ch is None or len(ch) != 1:
            out.append('\\x%02x' % x); i += 1; continue
        if is_print(ch): out.append(ch)
        elif ord(ch) < 0x10000: out.append('\\u%04x' % ord(ch))
        else: out.append('\\U%08x' % ord(ch))
        i += len(ch.encode('utf-8'))
    out.append('"')
    return ''.join(out)

def split_block(src):
    m = START_RX.search(src)
    if not m:
        raise ValueError('no rawDesc block found')
    a = m.end()
    lines = []; j = a
    while True:
        e = src.index('\n', j); line = src[j:e]; lines.append(line); j = e + 1
        if not line.rstrip().endswith('+'): break
    return a, j, lines

def decode_block(lines):
    data = b''
    for line in lines:
        lit = line.strip()
        if lit.endswith('+'): lit = lit[:-1].rstrip()
        data += go_unquote(lit)
    return data

def encode_block(data):
    parts = []; b = data
    while b:
        k = b.find(b'\n'); n = len(b) if k < 0 else k + 1
        parts.append(b[:n]); b = b[n:]
    out = []
    for idx, p in enumerate(parts):
        out.append('\t' + go_quote(p) + (' +' if idx < len(parts) - 1 else ''))
    return out

def main():
    if sys.argv[1] == '--selftest':
        src = open(sys.argv[2]).read(); a, j, lines = split_block(src)
        data = decode_block(lines)
        fd = descriptor_pb2.FileDescriptorProto(); fd.ParseFromString(data)
        assert fd.SerializeToString() == data, 'reserialize mismatch'
        assert encode_block(data) == lines, 'requote mismatch'
        print('selftest ok:', fd.package, len(data), 'bytes,', len(lines), 'lines'); return
    rewrite(*sys.argv[1:6])


def rewrite(path, old_pkg, new_pkg, old_go, new_go):
    src = open(path, encoding='utf-8').read(); a, j, lines = split_block(src)
    fd = descriptor_pb2.FileDescriptorProto(); fd.ParseFromString(decode_block(lines))
    if fd.package != old_pkg:
        return False
    fd.package = new_pkg
    fd.options.go_package = fd.options.go_package.replace(old_go, new_go)
    def fix(t): return t.replace('.' + old_pkg + '.', '.' + new_pkg + '.')
    def walk(msgs):
        for m in msgs:
            for f in m.field:
                if f.type_name: f.type_name = fix(f.type_name)
            walk(m.nested_type)
    walk(fd.message_type)
    for s in fd.service:
        for m in s.method:
            m.input_type = fix(m.input_type); m.output_type = fix(m.output_type)
    new = fd.SerializeToString()
    chk = descriptor_pb2.FileDescriptorProto(); chk.ParseFromString(new)
    assert old_pkg not in str(chk), 'old package still present'
    new_lines = encode_block(new)
    src = src[:a] + '\n'.join(new_lines) + '\n' + src[j:]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(src)
    print('rewrote descriptor in', path, '(%d bytes)' % len(new))
    return True


if __name__ == '__main__':
    main()

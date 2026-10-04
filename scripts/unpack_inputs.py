#!/usr/bin/env python3
"""Extract only the two hash-locked ROM inputs from a release archive."""
import hashlib
import json
import pathlib
import sys
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]
expected = json.loads((root/'inputs.lock.json').read_text())
with zipfile.ZipFile(sys.argv[1]) as src:
    if sorted(src.namelist()) != sorted(expected):
        raise ValueError('Unexpected files in source-inputs.zip')
    data = {name: src.read(name) for name in expected}
    for name, content in data.items():
        if hashlib.sha256(content).hexdigest() != expected[name]:
            raise ValueError(f'ROM input hash mismatch: {name}')
    (root/'inputs').mkdir(exist_ok=True)
    for name, content in data.items():
        (root/'inputs'/name).write_bytes(content)
print('ROM input hashes verified')

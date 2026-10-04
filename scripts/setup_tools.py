#!/usr/bin/env python3
"""Fetch pinned JADX and the public AOSP test signing key."""
import base64
import hashlib
import pathlib
import urllib.request
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]/'tools'
root.mkdir(exist_ok=True)
files = {
    'platform.pk8': '1ad8ef556870edb70f69a9d3c112544c07de5162ba440d84d33f8bb0c5962875',
    'platform.x509.pem': '9837de028f460c35cc8d3fa45f14eecce30f6fbfe4b93d399aef1acb80c20d14',
}
for name, expected in files.items():
    url = 'https://android.googlesource.com/platform/build/+/refs/heads/main/target/product/security/'+name+'?format=TEXT'
    data = base64.b64decode(urllib.request.urlopen(url, timeout=120).read())
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f'AOSP test key hash mismatch: {name}')
    (root/name).write_bytes(data)
archive = root/'jadx-1.5.6.zip'
if not archive.exists():
    urllib.request.urlretrieve('https://github.com/skylot/jadx/releases/download/v1.5.6/jadx-1.5.6.zip', archive)
if hashlib.sha256(archive.read_bytes()).hexdigest() != '545ea2be9c242511bc145755cf4bda2485ade42966e096f8b4d3da2a230e8974':
    raise ValueError('JADX release hash mismatch')
with zipfile.ZipFile(archive) as src:
    for item in src.infolist():
        target = (root/'jadx'/item.filename).resolve()
        if not target.is_relative_to((root/'jadx').resolve()):
            raise ValueError('Unsafe tool archive entry')
    src.extractall(root/'jadx')
print('JADX and public test keys ready')

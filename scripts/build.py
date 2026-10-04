#!/usr/bin/env python3
"""Package the tested launcher port from hash-locked ROM inputs."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CERT = 'c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(*args):
    return subprocess.check_output([str(a) for a in args], text=True, stderr=subprocess.STDOUT)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=pathlib.Path, default=ROOT/'inputs')
    parser.add_argument('--jadx-jar', type=pathlib.Path, default=ROOT/'tools/jadx/lib/jadx-1.5.6-all.jar')
    parser.add_argument('--keys', type=pathlib.Path, default=ROOT/'tools')
    parser.add_argument('--build-tools', type=pathlib.Path, required=True)
    args = parser.parse_args()
    for name, expected in json.loads((ROOT/'inputs.lock.json').read_text()).items():
        if digest(args.inputs/name) != expected:
            raise ValueError(f'Unexpected ROM input: {name}')
    build = ROOT/'build'
    build.mkdir(exist_ok=True)
    dist = ROOT/'dist'
    dist.mkdir(exist_ok=True)
    tools = args.build_tools.resolve()
    source = args.inputs/'Launcher3QuickStep.apk'
    original_cert = run(tools/'apksigner', 'verify', '--print-certs', source)
    if f'certificate SHA-256 digest: {CERT}' not in original_cert:
        raise ValueError('Source launcher certificate does not match the tested build')
    run('javac', '-cp', args.jadx_jar, '-d', build, ROOT/'scripts/DexSubset.java')
    refs = run('java', '-Xmx512m', '-cp', f'{build}:{args.jadx_jar}', 'DexSubset',
               args.inputs/'framework.jar', build/'omnijaws-client.dex',
               'Lcom/android/internal/util/crdroid/OmniJawsClient')
    (build/'client-refs.txt').write_text(refs)
    if not refs.rstrip().endswith('SELECTED 9'):
        raise ValueError('Expected all nine OmniJawsClient classes')
    with zipfile.ZipFile(source) as src, zipfile.ZipFile(build/'unsigned.apk','w') as dst:
        if 'classes3.dex' in src.namelist():
            raise ValueError('classes3.dex already exists')
        for entry in src.infolist():
            if not re.fullmatch(r'META-INF/[^/]+\.(SF|RSA|DSA|EC|MF)', entry.filename, re.I):
                dst.writestr(entry, src.read(entry.filename))
        # Match the tested v3 APK timestamp so repeated builds have stable bytes.
        dex_entry = zipfile.ZipInfo('classes3.dex', (2026, 10, 4, 18, 17, 52))
        dex_entry.compress_type = zipfile.ZIP_STORED
        dst.writestr(dex_entry, (build/'omnijaws-client.dex').read_bytes())
    run(tools/'zipalign', '-f', '-p', '4', build/'unsigned.apk', build/'aligned.apk')
    apk = build/'Launcher3QuickStep.apk'
    run(tools/'apksigner', 'sign', '--key', args.keys/'platform.pk8',
        '--cert', args.keys/'platform.x509.pem', '--out', apk, build/'aligned.apk')
    signed = run(tools/'apksigner', 'verify', '--verbose', '--print-certs', apk)
    if f'certificate SHA-256 digest: {CERT}' not in signed:
        raise ValueError('Patched launcher certificate changed')
    run(tools/'zipalign', '-c', '-p', '4', apk)
    with zipfile.ZipFile(source) as src, zipfile.ZipFile(apk) as dst:
        unchanged = [n for n in src.namelist() if not n.startswith('META-INF/')]
        if any(src.read(n) != dst.read(n) for n in unchanged):
            raise ValueError('An original launcher entry was changed')
    module = build/'module'
    if module.exists(): shutil.rmtree(module)
    shutil.copytree(ROOT/'module', module, symlinks=True)
    target = module/'system/system_ext/priv-app/Launcher3QuickStep/Launcher3QuickStep.apk'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(apk, target)
    output = dist/'crDroidHome-EvoX-v3.zip'
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for path in sorted(module.rglob('*')):
            if not path.is_file() and not path.is_symlink(): continue
            name = path.relative_to(module).as_posix()
            entry = zipfile.ZipInfo(name, (2026, 10, 4, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = ((0o120777 if path.is_symlink() else 0o100644) << 16)
            entry.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(entry, str(path.readlink()) if path.is_symlink() else path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None: raise ValueError('Corrupt module ZIP')
        if any('/framework/' in n for n in archive.namelist()): raise ValueError('Unexpected framework replacement')
    (dist/(output.name+'.sha256')).write_text(f'{digest(output)}  {output.name}\n')
    (dist/'build-report.json').write_text(json.dumps({
        'original_entries_preserved': len(unchanged), 'omnijaws_classes': 9,
        'apk_sha256': digest(apk), 'certificate_sha256': CERT,
        'module_sha256': digest(output), 'device_tested': False,
        'note': 'Build checks passed. Runtime testing of this artifact is separate.'
    }, indent=2)+'\n')
    print(f'Built and verified: {output}')

if __name__ == '__main__':
    main()

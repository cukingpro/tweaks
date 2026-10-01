"""Build flat, unsigned jailbreak APT repositories using Python and ar."""
import gzip
import hashlib
import html
import io
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "public"
SCHEMES = {"rootless": "iphoneos-arm64", "roothide": "iphoneos-arm64e"}


def control_fields(package):
    members = subprocess.check_output(["ar", "-t", str(package)], text=True).splitlines()
    member = next(name for name in members if name.startswith("control.tar"))
    data = subprocess.check_output(["ar", "-p", str(package), member])
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
        control = next(item for item in archive if item.name.lstrip("./") == "control")
        text = archive.extractfile(control).read().decode("utf-8")
    fields = {}
    key = None
    for line in text.splitlines():
        if line.startswith((" ", "\t")):
            if key is None:
                raise ValueError(f"Invalid control continuation: {package}")
            fields[key] += "\n" + line
        elif line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


def build():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    shutil.copyfile(ROOT / "index.html", OUTPUT / "index.html")
    (OUTPUT / ".nojekyll").touch()
    for scheme, architecture in SCHEMES.items():
        destination = OUTPUT / scheme
        (destination / "debs").mkdir(parents=True)
        entries = []
        downloads = []
        seen = set()
        for package in sorted((ROOT / scheme / "debs").glob("*.deb")):
            fields = control_fields(package)
            if fields["Architecture"] != architecture:
                raise ValueError(f"Wrong architecture in {package}")
            identity = (fields["Package"], fields["Version"], fields["Architecture"])
            if identity in seen:
                raise ValueError(f"Duplicate package version: {identity}")
            seen.add(identity)
            data = package.read_bytes()
            fields.update({
                "Filename": f"debs/{package.name}",
                "Size": str(len(data)),
                "MD5sum": hashlib.md5(data).hexdigest(),
                "SHA256": hashlib.sha256(data).hexdigest(),
                "SHA512": hashlib.sha512(data).hexdigest(),
            })
            entries.append("\n".join(f"{key}: {value}" for key, value in fields.items()))
            downloads.append(
                f'<li><a href="{html.escape(fields["Filename"], quote=True)}">'
                f'{html.escape(fields.get("Name", fields["Package"]))} '
                f'{html.escape(fields["Version"])} — tải .deb</a></li>'
            )
            shutil.copyfile(package, destination / "debs" / package.name)
        if not entries:
            raise ValueError(f"No packages found for {scheme}")
        index = ("\n\n".join(entries) + "\n\n").encode()
        (destination / "Packages").write_bytes(index)
        (destination / "Packages.gz").write_bytes(gzip.compress(index, mtime=0))
        release = [
            "Origin: Cukingpro Tweaks",
            f"Label: Cukingpro Tweaks ({scheme})",
            "Suite: stable",
            "Version: 1.0",
            f"Codename: cukingpro-{scheme}",
            f"Architectures: {architecture}",
            "Components: main",
            f"Description: Phim4K tweaks for {scheme}",
            f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')}",
        ]
        for label, algorithm in [("MD5Sum", "md5"), ("SHA256", "sha256"), ("SHA512", "sha512")]:
            release.append(f"{label}:")
            for name in ["Packages", "Packages.gz"]:
                data = (destination / name).read_bytes()
                release.append(f" {hashlib.new(algorithm, data).hexdigest()} {len(data)} {name}")
        (destination / "Release").write_text("\n".join(release) + "\n")
        url = f"https://cukingpro.github.io/tweaks/{scheme}/"
        title = "RootHide" if scheme == "roothide" else "Rootless"
        (destination / "index.html").write_text(f'''<!doctype html>
<html lang="vi">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cukingpro Tweaks — {title}</title>
<style>
body{{font:17px/1.6 system-ui,sans-serif;max-width:760px;margin:64px auto;padding:0 24px;background:#111827;color:#e5e7eb}}
a{{color:#93c5fd}} code{{overflow-wrap:anywhere}}
</style>
<h1>Cukingpro Tweaks — {title}</h1>
<p>Thêm địa chỉ này vào Sources trong Sileo hoặc Zebra:</p>
<p><code>{url}</code></p>
<p><a href="sileo://source/{url}">Thêm vào Sileo</a> ·
<a href="zbra://sources/add/{url}">Thêm vào Zebra</a></p>
<p>Kiến trúc package: <code>{architecture}</code>.</p>
<h2>Gói có sẵn</h2>
<ul>{"".join(downloads)}</ul>
<p><a href="Release">Release</a> · <a href="Packages">Packages</a> ·
<a href="Packages.gz">Packages.gz</a> · <a href="../">Trang chủ</a></p>
</html>
''', encoding="utf-8")
        print(f"Built {scheme}: {len(entries)} package(s)")


if __name__ == "__main__":
    build()

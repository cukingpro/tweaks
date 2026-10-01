# Cukingpro Tweaks

Repo Sileo/Zebra miễn phí, triển khai bằng GitHub Pages.

- Rootless: **https://cukingpro.github.io/tweaks/rootless/**
- RootHide: **https://cukingpro.github.io/tweaks/roothide/**
- Trang chủ: https://cukingpro.github.io/tweaks/

## Thêm bản cập nhật

1. Tăng `Version` trong `control` của project tweak và build `.deb` mới.
2. Đưa gói `iphoneos-arm64` vào `rootless/debs/`, gói `iphoneos-arm64e`
   vào `roothide/debs/`.
3. Commit và push lên `main`.
4. Đợi workflow **Publish tweak repository** hoàn tất; refresh nguồn trong Sileo/Zebra.

Không thay nội dung file `.deb` đã phát hành mà giữ nguyên version.
Có thể giữ các version cũ; trình quản lý gói chọn phiên bản mới nhất.

GitHub Actions tự sinh `Packages`, `Packages.gz`, `Release` với checksum,
sau đó deploy thư mục `public/`. Không cần chỉnh danh sách package bằng tay.
Đây là flat APT repository không ký GPG, truy cập qua HTTPS.

## Build website ở máy local

Cần Python 3 và `ar` (macOS có qua Xcode Command Line Tools;
Linux có trong binutils). Các gói hiện tại dùng tar.gz/tar.lzma mà Python hỗ trợ.

```bash
python3 scripts/build.py
python3 -m http.server 8080 --directory public
```

## Cấu hình GitHub

Trong Settings → Pages, chọn Source: **GitHub Actions**.
Workflow sử dụng quyền `pages: write`, `id-token: write` và `contents: read`.

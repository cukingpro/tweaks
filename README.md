# Cukingpro Tweaks

Repo Sileo/Zebra miễn phí, triển khai bằng GitHub Pages.

- Rootless: **https://cukingpro.github.io/tweaks/rootless/**
- RootHide: **https://cukingpro.github.io/tweaks/roothide/**
- Trang chủ: https://cukingpro.github.io/tweaks/

## Thêm bản cập nhật

### Ziga No Ads 1.1.0

- Có gói Rootless và RootHide; chỉ cài gói đúng với môi trường jailbreak.
- Nhận Ziga **1.34.2 trở lên có engine Cocos ARM64 và giao diện ads tương thích**.
- Tự dò hàm engine và địa chỉ singleton; không còn khóa UUID/địa chỉ của bản 1.34.2.
- Nếu ABI không khớp hoặc kết quả dò không duy nhất, tweak bỏ qua. Không bảo đảm
  mọi bản tương lai; hiện chưa có Ziga >1.34.2 để kiểm chứng trực tiếp.
- Bật injection cho Ziga, đóng hẳn rồi mở lại app sau khi cài/gỡ.
- Chặn banner, open-app ads qua JavaScript và interstitial; giữ video nhận thưởng.
- Payload đã thử qua Frida; resolver được kiểm tra trên artifact 1.34.2 và layout
  dịch chuyển tổng hợp. Bản deb 1.1.0 chưa được xác minh sau cài trên thiết bị.

### Quy trình phát hành

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

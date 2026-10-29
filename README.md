# Cukingpro Tweaks

Repo Sileo/Zebra miễn phí, triển khai bằng GitHub Pages.

- Rootless: **https://cukingpro.github.io/tweaks/rootless/**
- RootHide: **https://cukingpro.github.io/tweaks/roothide/**
- Trang chủ: https://cukingpro.github.io/tweaks/

## Thêm bản cập nhật

### Ziga Coach 0.1.3 — Rootless, iOS 15+

- Engine AB-JChess chạy trực tiếp trên iPhone, nút bật/tắt và cài đặt thời gian/luồng/Hash.
- Mũi tên gợi ý, điểm/depth và tỉ lệ quân úp trên bàn Ziga.
- Gói `iphoneos-arm64`, cài dưới `/var/jb`; yêu cầu iOS 15+ và binary Ziga 1.34.2 tương thích UUID.
- 0.1.3 hạ deployment target xuống 15.0 và bỏ yêu cầu ARMv8.2 dot-product cho CPU iPad cũ.
- Đã build và kiểm tra cấu trúc gói; chưa kiểm chứng trên thiết bị rootless.
- [Tải .deb và source tương ứng](https://github.com/cukingpro/Ziga/releases/tag/ziga-coach-v0.1.3).
- [Hướng dẫn sử dụng](https://github.com/cukingpro/Ziga/blob/main/tweak/ZigaCoach/README.vi.md).

### Ziga No Ads 1.1.1

- Có gói Rootless và RootHide; chỉ cài gói đúng với môi trường jailbreak.
- Nhận Ziga **1.34.2 trở lên có engine Cocos ARM64 và giao diện ads tương thích**.
- Tự dò hàm engine và địa chỉ singleton; không còn khóa UUID/địa chỉ của bản 1.34.2.
- Sửa RootHide nạp `systemhook` trước executable khiến bản cũ bỏ qua hook.
- Chặn ngay yêu cầu quảng cáo tự động sau trận, kể cả server chọn video.
- Nếu ABI không khớp hoặc kết quả dò không duy nhất, tweak bỏ qua. Không bảo đảm
  mọi bản tương lai; hiện chưa có Ziga >1.34.2 để kiểm chứng trực tiếp.
- Bật injection cho Ziga, đóng hẳn rồi mở lại app sau khi cài/gỡ.
- Chặn banner, open-app ads qua JavaScript và interstitial; giữ video nhận thưởng.
- Đã xác nhận lỗi image index và khôi phục native hook qua Frida trên RootHide;
  payload mới đã áp dụng live. Chưa kiểm chứng cold start với deb 1.1.1 hoặc quan sát
  thêm trận hoàn tất sau sửa.

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

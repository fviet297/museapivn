Tiện ích Muse2API Nhập Cookie —— Hướng dẫn cài đặt
=================================================

Tiện ích này chỉ làm một việc: đồng bộ Cookie đăng nhập muse.ai
trong trình duyệt của bạn vào dịch vụ muse2api.
Không cần cài Python, không cần mở terminal.


1. Giải nén
-----------
Giải nén muse2api-extension.zip vào thư mục bạn sẽ không xóa, ví dụ:

    Windows : D:\muse2api-extension
    macOS   : ~/Documents/muse2api-extension

Sau khi giải nén, bạn sẽ thấy ba tệp manifest.json, popup.html, popup.js.


2. Tải trong Chrome / Edge
--------------------------
Chrome:
  1. Nhập chrome://extensions vào thanh địa chỉ rồi nhấn Enter
  2. Bật công tắc "Chế độ dành cho nhà phát triển" ở góc trên bên phải
  3. Nhấn "Tải tiện ích đã giải nén" ở góc trên bên trái
  4. Chọn thư mục đã giải nén ở bước 1 (không chọn từng tệp bên trong)
  5. Biểu tượng mảnh ghép xuất hiện trên thanh công cụ; ghim nó vào thanh công cụ (tùy chọn nhưng tiện)

Edge:
  1. Nhập edge://extensions vào thanh địa chỉ rồi nhấn Enter
  2. Bật "Chế độ nhà phát triển" ở góc dưới bên trái
  3. Nhấn "Tải tiện ích đã giải nén"
  4. Các bước còn lại như trên

Các trình duyệt nhân Chromium khác (Brave / Vivaldi / 360 Tốc độ, v.v.) có các bước tương tự.


3. Sử dụng
----------
1. Trước tiên mở https://muse.ai/ và đăng nhập trong trình duyệt này,
   đăng nhập đến khi thấy giao diện chat.
2. Đến đầu tab "Bể tài khoản" trong trang quản trị muse2api, sao chép BASE URL và API Key.
3. Nhấn biểu tượng tiện ích trên thanh công cụ trình duyệt, điền hai mục này (chỉ cần điền một lần, sẽ được ghi nhớ).
4. Nhấn "Đọc và nhập". Khi thấy "✓ Nhập thành công" là xong.


4. Câu hỏi thường gặp
---------------------
Q: Báo "Không đọc được Cookie muse.ai"
A: Nghĩa là trình duyệt này chưa đăng nhập muse.ai. Hãy mở https://muse.ai/ và đăng nhập trước.

Q: Báo "thiếu mục cốt lõi hatch_sess..."
A: Như trên —— đăng nhập chưa hoàn tất. Xác nhận thấy giao diện chat rồi nhấn lại.

Q: Báo "API Key không đúng (dịch vụ trả về 401)"
A: Sao chép lại API Key ở trang quản trị. Lưu ý Key bắt đầu bằng m2a_.

Q: Báo lỗi cross-origin / mạng
A: Kiểm tra địa chỉ dịch vụ có phải https không, và dịch vụ có mở được không
   (thử truy cập trực tiếp địa chỉ dịch vụ/admin bằng trình duyệt).

Q: Tiện ích có gửi Cookie của tôi đi nơi khác không?
A: Không. Tiện ích chỉ có hai quyền cookies và storage, mã nguồn nằm trong popup.js,
   bạn có thể tự xem: nó chỉ gửi một POST đến địa chỉ dịch vụ bạn đã điền, không có yêu cầu nào khác.


5. Gỡ cài đặt
-------------
chrome://extensions → tìm "Muse2API Nhập Cookie" → Xóa.

# MUSE2API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker" alt="Docker" />
  <img src="https://img.shields.io/badge/API-OpenAI%20Compatible-green" alt="OpenAI API Compatible" />
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License" />
  <a href="https://linux.do/" target="_blank"><img src="https://img.shields.io/badge/Community-LINUX%20DO-111827?logo=linux&logoColor=white" alt="LINUX DO" /></a>
</p>

<p align="center">
  🤝 Dự án mã nguồn mở này đã liên kết và ghi nhận <b><a href="https://linux.do/" target="_blank">cộng đồng LINUX DO (https://linux.do/)</a></b> —— một cộng đồng kiểu mới lý tưởng (chân thành, thân thiện, đoàn kết, chuyên nghiệp)
</p>

Đóng gói ngược (reverse engineering) các khả năng đa phương thức tiên tiến của bản web **[muse.ai](https://muse.ai/)** thành **RESTful API tương thích OpenAI** chuẩn. Nhờ đi xuyên qua giao thức CDP của trình duyệt headless, tái dùng đường hầm WebSocket dự phòng nóng và quản lý Session động, dự án hỗ trợ sẵn chat văn bản (chữ đầu tiên dạng stream trong 2~3 giây), tạo ảnh từ văn bản, chỉnh sửa ảnh từ ảnh, tạo video từ văn bản, tạo video từ ảnh khung đầu; kèm xoay vòng bể nhiều tài khoản theo độ ưu tiên kết nối, tự động gia hạn phiên 48 giờ, đánh thức và giữ ấm VM trên đám mây, cùng tiện ích Chrome nhập tài khoản một chạm.

---

## 🌟 Tính năng chính

- 💬 **API chat chuẩn (Chat Completions & Responses API)**
  - Tương thích hoàn toàn giao thức chuẩn `/v1/chat/completions` và `/v1/responses` (Codex bản mới dùng mặc định).
  - Hỗ trợ sẵn stream SSE kiểu máy đánh chữ (`stream=True`) và trả về đồng bộ trọn vẹn; tích hợp tab nóng và tái dùng đường hầm Noise WebSocket theo độ ưu tiên, **độ trễ chữ đầu tiên khi chat liên tục chỉ 2~3 giây**.
  - Hỗ trợ ngữ cảnh hội thoại nhiều lượt và thiết lập System Prompt.
  - Ánh xạ bí danh model thông minh: các tên model phổ biến như `gpt-4o`, `gpt-5`, `claude-sonnet-4`, `deepseek-chat` được định tuyến tự động.
- 🎨 **Tạo ảnh chất lượng cao và chỉnh sửa ảnh (Images Generations & Edits)**
  - Tương thích hoàn toàn API `/v1/images/generations` (tạo ảnh từ văn bản) và `/v1/images/edits` (ảnh từ ảnh / chỉnh sửa theo ảnh tham chiếu).
  - Hỗ trợ nhiều khung hình `1:1`, `16:9`, `9:16`, `4:3`, `3:4`; hỗ trợ gửi thẳng ảnh tham chiếu và xuất ảnh sạch không watermark.
  - Hỗ trợ hai định dạng trả về: link trực tiếp `url` hoặc `b64_json`; tích hợp phát hiện trong vài giây khi model chỉ trả lời bằng văn bản, tránh kẹt hàng đợi.
  - Ảnh từ ảnh chỉ trả về media mới tạo của lần này: loại trừ ảnh xem trước khi tải lên và tệp đính kèm cũ, chỉ tải đúng kết quả đã chọn; nếu chưa xác nhận được việc tải ảnh tham chiếu hoặc gửi prompt thì báo lỗi rõ ràng, không còn lặng lẽ trả lại ảnh gốc.
- 🎬 **Tạo video từ văn bản / từ ảnh (Videos)**
  - Kết nối trực tiếp model tạo video cao cấp nhất của Muse; có thể yêu cầu thời lượng 5 / 6 / 8 / 10 giây (thời lượng thực tế theo kết quả Muse trả về) và tạo video dọc `9:16` / ngang `16:9`.
  - Hỗ trợ tải ảnh khung đầu (Data URL / HTTP URL) để tạo video bám chặt khung đầu.
  - Kiến trúc tác vụ bất đồng bộ (`/v1/videos` tạo tác vụ + `/v1/videos/{task_id}` hỏi trạng thái).
  - Tích hợp dịch vụ media `/v1/media/{filename}`, tự lưu trữ lâu dài các file MP4 / WebP đã tạo.
- ⚡ **Chạy song song thật sự trên nhiều tài khoản (Multi-Account Parallel Execution)**
  - Dựa trên container ẩn danh cô lập gốc của Chromium `Target.createBrowserContext`, nhiều tác vụ chạy đồng thời trong các sandbox riêng.
  - Nhiều tài khoản cùng lúc tạo ảnh, tạo video, chat stream mà không chặn nhau; Cookie và Session cô lập 100%, không bao giờ lẫn.
  - Tích hợp bộ điều phối xung đột tài khoản: cùng một tài khoản tự động loại trừ lẫn nhau, nhiều tài khoản tự động chạy song song hết công suất.
  - Có thể tăng giới hạn đồng thời qua `MUSE2API_CONCURRENCY` tuỳ cấu hình máy (mặc định 2).
- 🔄 **Bể nhiều tài khoản và điều phối ưu tiên kết nối nóng**
  - Hỗ trợ nhập không giới hạn số tài khoản Muse.
  - Phân phối thông minh theo ưu tiên kết nối nóng (Warm-Tab Affinity) và chiến lược LRU, vừa phản hồi nhanh cỡ 2 giây vừa tiêu hao đều giữa các tài khoản.
  - Khi một tài khoản hết hạn mức hoặc phiên bất thường, tự đánh dấu và chuyển ngay sang tài khoản dự phòng còn khoẻ mà người dùng không hề nhận ra.
- 🛡️ **Tự động gia hạn phiên 48 giờ và giữ ấm VM đám mây**
  - Coroutine nhịp tim chạy nền, gọi thẳng `/api/session` để tự gia hạn `hatch_vml` (+48h) và `hatch_sess` (+30d), đồng thời tự gọi `/api/hatch/vm/wake` để giữ VM workspace trên đám mây luôn sẵn sàng.
  - Giải quyết triệt để chuyện Cookie Meta hết hạn cố định sau 48 giờ và VM ngủ làm mất kết nối, không cần đăng nhập lại thường xuyên.
- 🧩 **Tiện ích Chrome nhập tài khoản một chạm**
  - Không cần mở F12 bắt gói tin: bấm biểu tượng tiện ích là lấy ngay trạng thái đăng nhập của trình duyệt hiện tại (gồm Cookie lõi `HttpOnly` và thời điểm hết hạn thật) rồi đẩy an toàn vào bể tài khoản.
- 🖥️ **Bảng điều khiển vận hành giao diện tối (Web Console) và nâng cấp nóng trực tuyến**
  - Web UI dùng ngay, xem trực tiếp sức khoẻ dịch vụ, hạn mức và trạng thái bể tài khoản, giữ phiên toàn bể một chạm, xem lại tiến trình tác vụ, quản lý thư viện media và thử API trực tuyến.
  - **Thông báo cập nhật thời gian thực và nâng cấp một chạm cho mọi node**: khi kho GitHub chính thức phát hành bản mới hoặc bản sửa lỗi, đầu trang quản trị của mọi node đã triển khai sẽ hiện thanh thông báo cập nhật; bấm **«⚡ Nâng cấp trực tuyến và khởi động lại»** là tự kéo code mới nhất và khởi động lại êm (giữ nguyên cấu hình `.env` và dữ liệu tài khoản cục bộ).

---

## 🚀 Triển khai nhanh

### Cách 1: Docker Compose (khuyên dùng, một lệnh là chạy)

1. **Clone code và vào thư mục**:

   ```bash
   git clone https://github.com/czg86389-hub/muse2api.git
   cd muse2api
   ```

2. **Cấu hình biến môi trường (tuỳ chọn)**:

   ```bash
   cp .env.example .env
   # Sửa .env theo nhu cầu, nên đổi MUSE2API_KEY thành khoá quản trị của riêng bạn
   ```

   Docker Compose đọc `MUSE2API_KEY` trong `.env`, không còn bị giá trị mẫu trong file Compose ghi đè.

3. **Khởi động container**:

   ```bash
   docker compose up -d
   ```

4. **Mở bảng quản trị**:
   Truy cập trên trình duyệt: `http://<IP máy chủ của bạn>:18610/admin?key=<MUSE2API_KEY của bạn>`

---

### Cách 2: Triển khai trên máy thật / VPS (Ubuntu / Debian)

1. **Cài gói hệ thống và Chromium**:

   ```bash
   sudo apt-get update
   sudo apt-get install -y chromium fonts-wqy-zenhei python3 python3-pip python3-venv
   ```

2. **Tạo môi trường ảo Python**:

   ```bash
   cd /opt/muse2api
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Cấu hình dịch vụ systemd**:

   ```bash
   sudo cp deploy/muse2api.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now muse2api
   ```

4. **Cấu hình reverse proxy Nginx (quan trọng: tránh lỗi 502 do timeout và stream bị khựng)**:
   Nếu dùng Nginx / BaoTa / 1Panel làm reverse proxy, nhất định phải tăng `proxy_read_timeout` lên `600s` và tắt `proxy_buffering` (xem `deploy/nginx.example.conf`):
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:18610;
       proxy_read_timeout 600s;      # Tránh Nginx báo 502 Bad Gateway khi tạo ảnh/video mất nhiều thời gian
       proxy_send_timeout 600s;
       proxy_buffering off;          # Đảm bảo chat stream SSE ra chữ không độ trễ
       client_max_body_size 64M;     # Cho phép tải lên ảnh tham chiếu dung lượng lớn
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   }
   ```

---

## 🧩 Nhập tài khoản (tiện ích Chrome / userscript Tampermonkey)

### Cách A: Tiện ích Chrome / Edge

Dự án có sẵn tiện ích Chrome chuyên để nhập tài khoản (thư mục `extension/`), khỏi phải lấy Cookie bằng F12 phức tạp:

1. Mở Chrome / Edge, vào `chrome://extensions`, bật **«Chế độ dành cho nhà phát triển»** ở góc trên bên phải.
2. Bấm **«Tải tiện ích đã giải nén»**, chọn thư mục `extension` của dự án.
3. Đăng nhập [muse.ai](https://muse.ai/) trên trình duyệt đó cho tới giao diện chat chính.
4. Bấm biểu tượng tiện ích ở góc trên bên phải trình duyệt, điền địa chỉ dịch vụ (ví dụ `http://1.2.3.4:18610`) và `MUSE2API_KEY`.
5. Bấm **«Đọc và nhập»**, tài khoản được đồng bộ vào kho trong vài giây!

### Cách B: Userscript Tampermonkey (dùng được trên nhiều trình duyệt, không cần cài tiện ích)

Nếu không muốn bật chế độ nhà phát triển hoặc dùng Firefox / Safari, nên cài thẳng userscript Tampermonkey bằng một chạm:

👉 **[⚡ Bấm để cài userscript Tampermonkey một chạm (Raw UserJS)](https://raw.githubusercontent.com/czg86389-hub/muse2api/main/tools/muse2api_cookie_importer.user.js)**

1. Cài tiện ích [Tampermonkey](https://www.tampermonkey.net/) cho trình duyệt.
2. Bấm link **«⚡ Bấm để cài userscript Tampermonkey một chạm»** ở trên, Tampermonkey sẽ tự hiện cửa sổ cài đặt, bấm «Cài đặt» là xong (không cần tự sao chép dán code).
3. Mở trang [muse.ai](https://muse.ai/), góc dưới bên phải sẽ có biểu tượng nổi **«⚡»**; bấm vào để mở bảng cấu hình và đẩy tài khoản vào kho một chạm (có dự phòng tự sao chép vào clipboard).

---

## 📖 Ví dụ gọi API

Mọi API được bảo vệ đều cần gửi kèm Header:

```http
Authorization: Bearer <MUSE2API_KEY của bạn>
```

### 1. Hoàn thành hội thoại (Chat Completions)

```bash
curl -X POST "http://localhost:18610/v1/chat/completions" \
  -H "Authorization: Bearer m2a_your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-spark",
    "messages": [
      {"role": "user", "content": "Viết một bài thơ lục bát về cyberpunk và mưa đêm ánh neon"}
    ],
    "stream": false
  }'
```

### 2. Tạo ảnh từ văn bản (Image Generation)

```bash
curl -X POST "http://localhost:18610/v1/images/generations" \
  -H "Authorization: Bearer m2a_your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "muse-image",
    "prompt": "Một chú chó Shiba máy mặc bộ đồ phi hành gia phản trọng lực, ánh sáng điện ảnh, độ phân giải 8k",
    "size": "16:9",
    "response_format": "url"
  }'
```

**Ví dụ phản hồi**:

```json
{
  "created": 1790148495,
  "data": [
    {
      "revised_prompt": "Một chú chó Shiba máy mặc bộ đồ phi hành gia phản trọng lực, ánh sáng điện ảnh, độ phân giải 8k",
      "url": "http://localhost:18610/v1/media/img_abc123.webp",
      "kind": "image",
      "bytes": 54210
    }
  ]
}
```

### 3. Tạo video từ văn bản / từ ảnh (Videos)

- **Bước 1: Tạo tác vụ**

  ```bash
  curl -X POST "http://localhost:18610/v1/videos" \
    -H "Authorization: Bearer m2a_your_secret_key" \
    -H "Content-Type: application/json" \
    -d '{
      "prompt": "Lá phong vàng nhẹ nhàng rơi trong làn gió, nắng xuyên qua ngọn cây",
      "duration": 5,
      "size": "16:9"
    }'
  ```

  Trả về ID tác vụ: `{"id": "task_xyz789", "status": "queued"}`

- **Bước 2: Hỏi tiến độ tác vụ**
  ```bash
  curl "http://localhost:18610/v1/videos/task_xyz789" \
    -H "Authorization: Bearer m2a_your_secret_key"
  ```
  Khi hoàn tất trả về:
  ```json
  {
    "id": "task_xyz789",
    "status": "succeeded",
    "progress": 100,
    "result": {
      "url": "http://localhost:18610/v1/media/vid_xyz789.mp4"
    }
  }
  ```

---

## ⚙️ Bảng biến môi trường

| Tên biến                 | Mặc định    | Tác dụng                                                                             |
| ------------------------ | ----------- | ------------------------------------------------------------------------------------ |
| `MUSE2API_KEY`           | Tự sinh     | Khoá xác thực cho bảng quản trị và API (bắt đầu bằng `m2a_`)                         |
| `MUSE2API_HOST`          | `127.0.0.1` | IP lắng nghe (trong Docker nên dùng `0.0.0.0`)                                       |
| `MUSE2API_PORT`          | `18610`     | Cổng chạy dịch vụ                                                                    |
| `MUSE2API_PUBLIC_BASE`   | `trống`     | Tiền tố URL đầy đủ ra bên ngoài; để trống thì giao diện tự nhận nguồn truy cập       |
| `MUSE2API_CHROMIUM`      | `chromium`  | Đường dẫn đầy đủ tới file thực thi trình duyệt                                       |
| `MUSE2API_CDP_PORT`      | `19210`     | Cổng giao tiếp gỡ lỗi CDP nội bộ                                                     |
| `MUSE2API_CONCURRENCY`   | `2`         | Số tác vụ tạo chạy đồng thời tối đa (có thể tăng tuỳ tài nguyên máy chủ, mặc định 2) |
| `MUSE2API_IMAGE_TIMEOUT` | `240`       | Thời gian chờ tối đa khi tạo ảnh (giây)                                              |
| `MUSE2API_VIDEO_TIMEOUT` | `600`       | Thời gian chờ tối đa khi tạo video (giây)                                            |
| `MUSE2API_CHAT_TIMEOUT`  | `300`       | Thời gian chờ tối đa khi chat (giây)                                                 |

---

## 🔒 Bảo mật và quyền riêng tư

- **Không rò rỉ dữ liệu**: toàn bộ dữ liệu của phần mềm (gồm thông tin đăng nhập tài khoản, hàng đợi tác vụ, file media) đều lưu cục bộ trong thư mục `data/`, không phụ thuộc bất kỳ dịch vụ đo lường hay trung chuyển bên thứ ba nào.
- **Tuân thủ mã nguồn mở**: dự án chỉ dùng cho trao đổi kỹ thuật, nghiên cứu tự động hoá vận hành hệ thống và kiểm thử tự động. Không dùng dự án vào mục đích vi phạm điều khoản dịch vụ của nền tảng Meta hay pháp luật của bất kỳ quốc gia nào.

---

## 🤝 Cộng đồng và liên kết

Dự án đã liên kết và đánh giá cao **[cộng đồng LINUX DO](https://linux.do/)**, cảm ơn các thành viên cộng đồng đã trao đổi, góp ý và ủng hộ:

- 🌐 **[Cộng đồng LINUX DO (https://linux.do/)](https://linux.do/)** —— một cộng đồng kiểu mới lý tưởng (chân thành, thân thiện, đoàn kết, chuyên nghiệp, cùng xây một cộng đồng mà tất cả chúng ta tự hào)

---

## 👥 Ghi nhận người đóng góp (Contributors)

Cảm ơn các lập trình viên sau đã đóng góp code và cải tiến cho MUSE2API (theo thứ tự PR được gộp):

- 🌟 **[@cpt-kenvie](https://github.com/cpt-kenvie)** (PR [#2](https://github.com/czg86389-hub/muse2api/pull/2)) —— Sửa lỗi Docker Compose đọc biến môi trường `.env` bị cấu hình mẫu ghi đè
- 🌟 **[@djs-91](https://github.com/djs-91)** (PR [#9](https://github.com/czg86389-hub/muse2api/pull/9)) —— Sửa lỗi Base URL bị thu gọn khi chưa cấu hình `MUSE2API_PUBLIC_BASE`, làm trang quản trị phân tích sai địa chỉ
- 🌟 **[@toby-bridges](https://github.com/toby-bridges)** (PR [#8](https://github.com/czg86389-hub/muse2api/pull/8)) —— Thích ứng giao diện tiếng Trung hiện hành của muse.ai, sửa lỗi xác nhận tải tệp đính kèm và nhận nhầm trạng thái Stop, tăng cường chống chọn nhầm video thành phẩm với ảnh bìa
- 🌟 **[@LF2023](https://github.com/LF2023)** (PR [#18](https://github.com/czg86389-hub/muse2api/pull/18)) —— Sửa lỗi tạo video chỉ dựa vào tid nên trúng ảnh bìa tĩnh, chuẩn hoá cơ chế khớp kết quả mong đợi và chống chọn nhầm
- 🌟 **[@wuliaolaozi](https://github.com/wuliaolaozi)** (PR [#27](https://github.com/czg86389-hub/muse2api/pull/27)) —— Hỗ trợ tra hạn mức trên giao diện tiếng Trung và tiếng Anh, sửa lỗi đọc hạn mức và thông báo lỗi trên trang quản trị
- 🌟 **[@CarloCPP](https://github.com/CarloCPP)** (PR [#6](https://github.com/czg86389-hub/muse2api/pull/6), [#26](https://github.com/czg86389-hub/muse2api/pull/26)) —— Đóng góp userscript Tampermonkey nhập tài khoản một chạm, nới kiểm tra Cookie bắt buộc xuống chỉ còn thông tin session và cài đặt một chạm
- 🌟 **[@gr219](https://github.com/gr219)** (PR [#31](https://github.com/czg86389-hub/muse2api/pull/31)) —— Hỗ trợ chuyển đổi song ngữ Trung–Anh cho trang quản trị và tiện ích Chrome

Mọi người cứ gửi PR và Issue, cùng nhau làm dự án mạnh hơn, dễ dùng hơn!

---

## 📄 Giấy phép mã nguồn mở

Dự án phát hành theo giấy phép [MIT License](LICENSE).

## Kiểm thử hồi quy việc chọn media

Sửa lỗi ảnh tham chiếu vừa tải lên bị nhận nhầm là kết quả tạo, và lỗi trong lúc tải về bị media khác trên trang ghi đè.
Bài kiểm thử dùng một profile Chromium tạm riêng và DOM tổng hợp cục bộ, không truy cập Muse, không đọc tài khoản, không tốn hạn mức tạo.
Sau khi cài các gói phụ thuộc và Chromium, chạy từ thư mục gốc của repo:

```bash
python tests/test_media_selection.py
```

Nếu trình duyệt không nằm trong PATH, đặt `MUSE2API_CHROMIUM` thành đường dẫn file thực thi.
Phạm vi kiểm thử: loại trừ ảnh xem trước khi tải lên, khử trùng lặp kết quả, loại trừ tệp đính kèm cũ, tải về đúng nguồn, giữ nguồn video,
cấm quay về tải toàn cục, và dừng khi đọc ảnh tham chiếu thất bại. Hiệu quả chỉnh sửa ảnh cuối cùng vẫn phải nghiệm thu qua API thật.

## v1.5.2: Tạo ảnh lâu sau reverse proxy/CDN

API ảnh đồng bộ kiểu OpenAI vẫn được giữ để tương thích, nhưng CDN/client có thể cắt request dài trước khi tạo xong.
Client chạy thật nên dùng kiểu gửi ngắn + hỏi trạng thái định kỳ, thay vì tăng HTTP timeout rồi tạo lại nhiều lần:

1. `POST /v1/images/tasks`: JSON giống `/v1/images/generations`, có thể truyền ảnh tham chiếu cho ảnh từ ảnh qua `reference_image`; nên thêm header `Idempotency-Key` cố định.
2. Nhận HTTP 202 và `id`, cứ 3 giây gọi `GET /v1/images/tasks/{id}` một lần.
3. Khi `status=completed` thì đọc `url` hoặc `data[0]`; khi `status=failed` thì hiển thị `error`. Hỏi trạng thái lỗi thì chỉ hỏi lại, đừng POST tạo ảnh lại.
4. Cùng khoá idempotency và cùng đầu vào thì trả về tác vụ cũ; cùng khoá khác đầu vào trả 409; hàng đợi đầy trả 429. Mỗi tiến trình dùng chung một trình duyệt, nhận tối đa 8 tác vụ ảnh chưa kết thúc.

JSON của `/v1/images/generations` cũ và JSON/multipart của `/v1/images/edits` cũng có thể truyền `async=true` để chuyển sang cùng luồng xử lý bất đồng bộ. Hành vi đồng bộ mặc định không đổi.
`timeout` là ngân sách chờ xếp hàng và tạo (1–600 giây); khởi tạo trình duyệt và lấy kết quả có timeout riêng; client nên tiếp tục hỏi cho tới khi tác vụ ở trạng thái cuối.
Metadata tác vụ được lưu lâu dài; khi tiến trình khởi động lại, các tác vụ ảnh chưa xong bị đánh dấu thất bại, không âm thầm tạo lại.
Phần thử API ảnh trong trang quản trị cũng đã chuyển sang hỏi trạng thái tác vụ.

Kiểm tra hồi quy (không tốn hạn mức tạo thật):

```bash
python tests/test_async_images.py
python tests/test_vm_wait.py engine.py --assert
```

Sửa lỗi tranh chấp khi xử lý ngoại lệ trình duyệt dùng chung reset tác vụ khác sau khi mở khoá; không còn coi chữ
`Connecting...` / `Still sending` sót lại ở thanh bên trang là bằng chứng lần tạo ảnh hiện tại thất bại trong 16 giây.

## v1.5.3: Trạng thái tài khoản bất thường và xử lý sự cố trên máy tự dựng

Request giữ phiên đi ra từ **đường mạng của máy chủ triển khai**, không phải từ trình duyệt đã xuất Cookie. Máy chủ của tác giả chạy được không chứng minh rằng mạng, khu vực, cấu hình proxy hay phiên của cùng tài khoản trên máy chủ khác cũng ổn.

- `/api/session HTTP 401`: phía trên từ chối xác thực. Trước tiên kiểm tra tài khoản đăng nhập được trên trang chính thức muse.ai, rồi nhập lại Cookie.
- `HTTP 403`: bị từ chối truy cập, có thể do quyền tài khoản, đường mạng máy chủ hoặc giới hạn khu vực/truy cập; **không đồng nghĩa với Cookie hết hạn**. Kiểm tra lỗi đầy đủ và mạng triển khai, đừng nhập lại mù quáng nhiều lần.
- `HTTP 429`, `5xx`, timeout, không phải JSON hoặc không trả về `assigned`: lần giữ phiên này chưa được xác nhận, không còn báo thành công giả hay ghi đè trạng thái tài khoản đã xác nhận lần trước; phần ghi chú hiển thị chẩn đoán. Trạng thái cũ là "chưa kiểm tra" hoặc "bất thường" cũng không bị ép thành "dùng được".
- Trang trình duyệt tải quá thời gian cũng không còn bị coi ngay là mất xác thực; chỉ khi xác thực thất bại rõ ràng mới đánh dấu tài khoản bất thường.
- "Dùng được" là kết quả đã xác nhận gần nhất, không đảm bảo lần này mạng thông; "thời hạn còn lại" là thời gian/ước tính của Cookie, không chứng minh phiên phía máy chủ còn hiệu lực. Kiểm tra thành công không còn tự cộng thêm 48 giờ, việc gia hạn dựa trên Cookie thực tế trả về.

Sau khi cập nhật lên v1.5.3 và khởi động lại dịch vụ, bấm "Kiểm tra" ở tài khoản để xác nhận lại. Trạng thái bất thường đã ghi từ bản cũ sẽ không bị tẩy thành bình thường vô điều kiện. Rê chuột lên ghi chú để xem lỗi đầy đủ; khi phản hồi hãy cung cấp mã HTTP, phiên bản và môi trường triển khai, **đừng công khai Cookie, API Key hay link trang quản trị có kèm key**.

Triển khai Git trên máy thật: `git pull --ff-only` rồi khởi động lại dịch vụ tương ứng; Docker Compose: `git pull --ff-only && docker compose up -d --build`. Hãy lưu các chỉnh sửa tuỳ biến cục bộ trước, giữ nguyên `.env` và `data/`.

Kiểm thử hồi quy không dùng tài khoản thật, không tốn hạn mức tạo:

```bash
python tests/test_session_health.py
```

# MUSE2API 1.6.1

## Ghi chú cập nhật (2026-10-13)

- Sửa lỗi tra hạn mức nhiều tài khoản bị đọc lẫn: việc tra hạn mức gắn với trang trình duyệt của đúng tài khoản, tránh hiển thị sai số dư và lượng dùng giữa các tài khoản.
- Khi đọc hạn mức thất bại hoặc không đọc được dữ liệu hợp lệ thì giữ bộ nhớ đệm cũ và báo rõ là đọc thất bại, tránh coi kết quả vô hiệu là hạn mức thời gian thực.
- Sửa lỗi báo nhầm giữ phiên thành công: phân biệt yêu cầu đánh thức đã được chấp nhận với VM đã chạy, chỉ khi kiểm tra lại thấy trạng thái RUNNING mới báo đánh thức thành công.
- Trang quản trị hiển thị thời điểm tra hạn mức và cảnh báo hết hạn; kiểm tra tài khoản phản hồi riêng tính hợp lệ của phiên và trạng thái đọc hạn mức.
- Thêm kiểm thử hồi quy ngoại tuyến, bao phủ việc cô lập hạn mức giữa các tài khoản và xác nhận trạng thái đánh thức VM.

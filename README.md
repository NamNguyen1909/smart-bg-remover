# Smart Background Remover

A high-precision, offline Python tool designed to remove backgrounds from both logos/graphics and complex illustrations.

*Note: [Xem tài liệu hướng dẫn bằng Tiếng Việt tại đây](#tiếng-việt).*

---

## 1. English Documentation

The tool supports three distinct processing modes:
1. **Solid Mode (`--mode solid`)**: A custom color-distance based engine. It is pixel-perfect for logos, icons, and flat vectors on a solid background. By default, it uses flood-fill to protect internal white details (like collar, eyes). You can use `--no-floodfill` to perform global keying for text-based logos containing enclosed loops (like inside the letters `b` or `o`).
2. **AI Mode (`--mode ai`)**: Deep learning segmentation via `rembg` (supporting models like `isnet-anime` and `birefnet-general`) for general photos and objects.
3. **Hybrid Mode (`--mode hybrid`)**: Combines AI segmentation (`isnet-anime`) with a **Core Protection Mask** and **Color-Distance Keying**. This is the ultimate mode for complex illustrations (e.g. anime characters) to cleanly remove background bleeding between fine hair strands while keeping the face, eyes, and clothing 100% solid.

### Visual Demos

#### A. Solid Mode (`--mode solid`) - Best for Logos & Badges
*Perfect for flat designs. Use `--no-floodfill` to clean up enclosed white spaces (like inside the letter `b` or the cat's face).*

| Input Image (`images/logo-03.cc5e5332.png`) | Output Image (`images/logo_output_clean.png`) |
| --- | --- |
| ![Logo Input](images/logo-03.cc5e5332.png) | ![Logo Output](images/logo_output_clean.png) |

#### B. Hybrid Mode (`--mode hybrid`) - Best for Complex Drawings & Anime Hair
*Handles gradient backgrounds, floating objects, and fine hair details without leaving background color casts or bleeding.*

| Input Image (`images/aot_input.jpg`) | Output Image (`images/aot_hybrid.png`) |
| --- | --- |
| ![Anime Input](images/aot_input.jpg) | ![Anime Output](images/aot_hybrid.png) |

---

### Features
- **Three Processing Engines:** Choose between Solid, AI, or Hybrid mode based on your image type.
- **Core Protection Mask:** Hybrid mode protects the inner parts of the character (eyes, face, body) using binary erosion, ensuring color-keying only cleans up outer hair strands and gaps.
- **Preserves Details:** Solid mode guarantees 100% border preservation (won't crop circular frames or thin lines).
- **Soft-Alpha Edge Matting:** Smooths borders to completely eliminate pixelated edges or color halos.
- **Full Resolution:** Keeps 100% of the original resolution and quality (supports 2K, 4K, 8K+).
- **100% Offline & Private:** Run completely locally on your system.

---

### Installation

1. Clone this repository.
2. Install the core dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Optional)* If you plan to use the **AI Mode** or **Hybrid Mode**, install the AI engine:
   ```bash
   pip install rembg
   # For GPU acceleration, run instead:
   # pip install rembg[gpu]
   ```

---

### Usage

Run the tool via terminal:
```bash
python remove_bg_smart.py <input_path> <output_path> [options]
```

#### Options:
- `--mode {solid,ai,hybrid}`: Select processing engine. Default is `solid`.
- `--model MODEL`: Specify AI model name (for `ai` and `hybrid` modes). 
  - `isnet-anime` (default): Best for anime and illustrations.
  - `birefnet-general`: Best for real photos and objects.
- `--tolerance TOL`: Color threshold limit for background detection (default: `40` for solid, `75` for hybrid).
- `--low-tolerance LOW_TOL`: Edge blending lower limit for soft transparency (default: `15` for solid, `35` for hybrid).
- `--no-floodfill`: Disable flood-fill connectivity for `solid` mode. Use this for flat logos/text containing enclosed spaces (like inside the letter `b` or `o`) to remove all background pixels globally.
- `--erosion-iterations ITER`: Size of the protection mask (default: `15`, only in `hybrid` mode). Higher values protect more of the inner body.
- `--alpha-matting`: Use rembg built-in alpha matting (only in `ai` mode).

#### Examples:
**Tách nền logo phẳng có chữ (Solid Mode + No Flood-fill):**
```bash
python remove_bg_smart.py images/logo-03.cc5e5332.png images/logo_output_clean.png --mode solid --no-floodfill
```

**Tách tranh anime phức tạp (Hybrid Mode - Khuyên dùng cho kẽ tóc):**
```bash
python remove_bg_smart.py images/aot_input.jpg images/aot_hybrid.png --mode hybrid --model isnet-anime
```

---

<a name="tiếng-việt"></a>
## 2. Tài Liệu Hướng Dẫn Tiếng Việt

Công cụ Python chạy offline với độ chính xác cao, hỗ trợ tách nền cho cả logo phẳng đơn sắc và tranh vẽ minh họa phức tạp. 

Công cụ tích hợp ba chế độ hoạt động chính:
1.  **Solid Mode (`--mode solid`)**: Thuật toán loang vùng (flood-fill) tùy biến dựa trên khoảng cách màu. Cực kỳ chính xác cho logo, icon trên nền phẳng (bảo vệ viền tròn ngoài mà AI thường cắt lẹm).
    *   *Mẹo:* Sử dụng thêm tham số `--no-floodfill` khi tách các logo có chữ hoặc khoảng trống khép kín (như trong lòng chữ `b` hoặc `o` hoặc khuôn mặt mèo Octocat) để xóa sạch nền ở mọi vị trí.
2.  **AI Mode (`--mode ai`)**: Sử dụng mạng nơ-ron thông qua thư viện `rembg` cho ảnh chụp và vật thể thông thường.
3.  **Hybrid Mode (`--mode hybrid`)**: Kết hợp phân tách AI (`isnet-anime`) với **Mặt nạ bảo vệ lõi** (Core Protection Mask) và **Khoảng cách màu**. Đây là chế độ tốt nhất cho tranh anime phức tạp, giúp xóa sạch màu nền bị kẹt giữa các khe tóc nhỏ mà không làm hỏng mắt, da, hay quần áo nhân vật.

### Demo Trực Quan

#### A. Solid Mode (`--mode solid`) - Dành cho Logo & Huy hiệu phẳng
*Thích hợp cho logo phẳng. Sử dụng thêm `--no-floodfill` để làm sạch các khoảng trắng khép kín.*

| Ảnh gốc (`images/logo-03.cc5e5332.png`) | Ảnh kết quả (`images/logo_output_clean.png`) |
| --- | --- |
| ![Logo Input](images/logo-03.cc5e5332.png) | ![Logo Output](images/logo_output_clean.png) |

#### B. Hybrid Mode (`--mode hybrid`) - Dành cho Tranh vẽ Anime & Tóc phức tạp
*Xử lý nền trời chuyển sắc, các vật thể lơ lửng và kẽ tóc siêu nhỏ mà không để lại vệt ám màu nền.*

| Ảnh gốc (`images/aot_input.jpg`) | Ảnh kết quả (`images/aot_hybrid.png`) |
| --- | --- |
| ![Anime Input](images/aot_input.jpg) | ![Anime Output](images/aot_hybrid.png) |

---

### Các Tính Năng Nổi Bật
- **Ba Chế Độ Linh Hoạt:** Dễ dàng lựa chọn giữa Solid, AI hoặc Hybrid tùy thuộc vào loại ảnh của bạn.
- **Mặt Nạ Bảo Vệ Lõi (Core Protection):** Chế độ Hybrid sử dụng thuật toán co ảnh để tự động bảo vệ mắt, da, quần áo nhân vật, chỉ tập trung loại bỏ nền ở rìa ngoài và các khe tóc mảnh.
- **Giữ Nguyên Viền Chi Tiết:** Chế độ Solid đảm bảo 100% đường viền nguyên vẹn (không bị lẹm viền tròn hay nét vẽ mảnh).
- **Khử Răng Cưa Cực Tốt (Soft-Alpha):** Bo mịn các rìa cắt giúp ảnh ghép tự nhiên, không dính viền trắng hay răng cưa.
- **Độ Phân Giải Nguyên Bản:** Hỗ trợ xử lý ảnh 2K, 4K, 8K+ mà không bị nén hay bóp chất lượng.
- **100% Ngoại Tuyến & Bảo Mật:** Chạy hoàn toàn trên máy tính cá nhân của bạn.

---

### Cài Đặt

1. Tải (clone) repository này về máy.
2. Cài đặt các thư viện cốt lõi:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Tùy chọn)* Nếu bạn muốn sử dụng **AI Mode** hoặc **Hybrid Mode**, hãy cài đặt thêm công cụ AI:
   ```bash
   pip install rembg
   # Để chạy bằng card đồ họa (Nvidia GPU), cài lệnh sau:
   # pip install rembg[gpu]
   ```

---

### Cách Sử Dụng

Chạy lệnh sau trong Terminal/PowerShell:
```bash
python remove_bg_smart.py <đường_dẫn_ảnh_gốc> <đường_dẫn_ảnh_đầu_ra> [các_tùy_chọn]
```

#### Các Tùy Chọn:
- `--mode {solid,ai,hybrid}`: Chọn chế độ xử lý. Mặc định là `solid`.
- `--model MODEL`: Tên mô hình AI sử dụng (cho chế độ `ai` và `hybrid`).
  - `isnet-anime` (mặc định): Tốt nhất cho tranh vẽ anime, manga.
  - `birefnet-general`: Tốt nhất cho ảnh chụp thật và vật thể.
- `--tolerance TOL`: Ngưỡng nhận diện màu nền (mặc định: `40` cho solid, `75` cho hybrid).
- `--low-tolerance LOW_TOL`: Ngưỡng làm mờ cạnh để khử răng cưa (mặc định: `15` cho solid, `35` cho hybrid).
- `--no-floodfill`: Tắt tính năng Flood-fill ở chế độ `solid`. Dùng cho các logo phẳng có chữ hoặc khoảng trống khép kín để xóa sạch nền ở mọi góc.
- `--erosion-iterations ITER`: Độ rộng mặt nạ bảo vệ cơ thể (mặc định: `15`, chỉ dùng trong chế độ `hybrid`). Số càng cao thì bảo vệ lõi càng sâu.
- `--alpha-matting`: Sử dụng bộ lọc viền mặc định của rembg (chỉ dùng trong chế độ `ai`).

#### Các Câu Lệnh Mẫu:
**Tách logo nền trắng có khoảng khép kín (như chữ b, o):**
```bash
python remove_bg_smart.py images/logo-03.cc5e5332.png images/logo_output_clean.png --mode solid --no-floodfill
```

**Tách hình vẽ anime phức tạp (Chế độ Hybrid - Sạch kẽ tóc):**
```bash
python remove_bg_smart.py images/aot_input.jpg images/aot_hybrid.png --mode hybrid
```

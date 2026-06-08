# Smart Background Remover

[Tiếng Việt bên dưới](#tiếng-việt)

A high-precision, offline Python tool designed to remove backgrounds from both logos/graphics and complex illustrations. It supports two distinct modes:
1. **Solid Mode (`--mode solid`)**: A custom flood-fill algorithm based on color distance that is pixel-perfect for logos, icons, and flat vectors on a solid background (preserves outline borders where AI usually fails).
2. **AI Mode (`--mode ai`)**: Integrated deep learning segmentation via `rembg` (supporting models like `isnet-anime` and `birefnet-general`) for complex drawings, illustrations, and photos with gradients or detailed backgrounds.

---

## Visual Demos

### 1. Solid Mode (`--mode solid`) - Best for Logos & Badges
*Perfect for flat designs. Preserves delicate details like the circular golden frame without any cutoffs.*

| Input Image (`images/input.jpg`) | Output Image (`images/output.png`) |
| --- | --- |
| ![Logo Input](images/input.jpg) | ![Logo Output](images/output.png) |

### 2. AI Mode (`--mode ai`) - Best for Complex Drawings & Anime
*Handles gradient backgrounds, floating objects, and complex character details using neural network models (e.g. `isnet-anime`).*

| Input Image (`images/input_complex.jpg`) | Output Image (`images/output_complex.png`) |
| --- | --- |
| ![Anime Input](images/input_complex.jpg) | ![Anime Output](images/output_complex.png) |

---

## Features
- **Dual Processing Engines:** Choose between high-precision color-keying or state-of-the-art AI segmentation.
- **Preserves Details:** Solid mode guarantees 100% border preservation (won't crop circular frames or thin lines).
- **Keeps Internal Details:** Solid mode only removes background connected to the borders; inner elements remain untouched.
- **Soft-Alpha Edge Matting:** Smooths borders to completely eliminate pixelated edges or white halo fringing.
- **Full Resolution:** Keeps 100% of the original resolution and quality (supports 2K, 4K, 8K+).
- **100% Offline & Private:** Run completely locally on your system.

---

## Installation

1. Clone this repository.
2. Install the core dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Optional)* If you plan to use the **AI Mode (`--mode ai`)**, install the AI engine:
   ```bash
   pip install rembg
   # For GPU acceleration, run instead:
   # pip install rembg[gpu]
   ```

---

## Usage

Run the tool via terminal:
```bash
python remove_bg_smart.py <input_path> <output_path> [options]
```

### Options:
- `--mode {solid,ai}`: Select processing engine. Default is `solid`.
- `--model MODEL`: Specify AI model name (only in `ai` mode). 
  - `isnet-anime` (default): Best for anime and illustrations.
  - `birefnet-general`: Best for real photos and objects.
  - `u2net`: General-purpose model.
- `--tolerance TOL`: Color threshold limit for background detection (only in `solid` mode, default: `40`).
- `--low-tolerance LOW_TOL`: Edge blending lower limit for soft transparency (only in `solid` mode, default: `15`).

### Examples:
**Tách nền logo trắng (Solid Mode):**
```bash
python remove_bg_smart.py images/input.jpg images/output.png --mode solid
```

**Tách nền tranh anime phức tạp (AI Mode):**
```bash
python remove_bg_smart.py images/input_complex.jpg images/output_complex.png --mode ai --model isnet-anime
```

---

<a name="tiếng-việt"></a>
# Smart Background Remover (Bộ Tách Nền Thông Minh)

Công cụ Python chạy offline với độ chính xác cao, hỗ trợ tách nền cho cả logo phẳng đơn sắc và tranh vẽ minh họa phức tạp. Dự án tích hợp hai chế độ hoạt động:

1.  **Solid Mode (`--mode solid`)**: Thuật toán loang vùng (flood-fill) tùy biến dựa trên khoảng cách màu. Cực kỳ chính xác cho logo, icon, vector trên nền phẳng (bảo vệ hoàn hảo viền tròn ngoài mà AI thường cắt lẹm).
2.  **AI Mode (`--mode ai`)**: Sử dụng mạng nơ-ron tích hợp thông qua thư viện `rembg` (hỗ trợ model `isnet-anime` và `birefnet-general`) để tách nền phức tạp, nền gradient hoặc ảnh đời thực.

## Tham số dòng lệnh:
- `--mode {solid,ai}`: Chọn chế độ xử lý. Mặc định là `solid`.
- `--model MODEL`: Tên mô hình AI sử dụng (chỉ áp dụng ở chế độ `ai`).
  - `isnet-anime` (mặc định): Tốt nhất cho tranh vẽ anime, manga.
  - `birefnet-general`: Tốt nhất cho ảnh chụp thật và vật thể.
- `--tolerance TOL`: Ngưỡng nhận diện màu nền (chỉ ở chế độ `solid`, mặc định: `40`).
- `--low-tolerance LOW_TOL`: Ngưỡng làm mờ cạnh để khử răng cưa (chỉ ở chế độ `solid`, mặc định: `15`).

## Lệnh mẫu:
**Tách logo nền trắng:**
```bash
python remove_bg_smart.py images/input.jpg images/output.png --mode solid
```

**Tách hình vẽ anime phức tạp:**
```bash
python remove_bg_smart.py images/input_complex.jpg images/output_complex.png --mode ai --model isnet-anime
```

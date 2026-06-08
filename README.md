# Smart Background Remover (for Logos & Graphics)

[Tiếng Việt bên dưới](#tiếng-việt)

A high-precision, offline Python tool designed specifically for removing solid backgrounds (like white or black) from logos, badges, illustrations, and icons.

Standard AI background removers (like `rembg` or other online services) are designed for salient object detection. They often fail on logos by cropping out geometric borders, circular frames, or thin lines. This tool solves that by using a color-distance-based flood-fill algorithm starting from the edges.

## Visual Demo
| Input Image (`images/input.jpg`) | Output Image (`images/output.png`) |
| --- | --- |
| ![Input](images/input.jpg) | ![Output](images/output.png) |

## Features
- **Preserves Details:** Does not crop circular gold/silver frames or details that standard AI tools typically miss.
- **Keeps Internal White/Colors:** Only removes the background connected to the borders. Internal white elements (like text background, eyes, collar) remain 100% intact.
- **Soft-Alpha Antialiasing:** Generates a smooth opacity transition on the edges to completely eliminate white halos/fringing.
- **Full Resolution:** Process 2K, 4K, and 8K+ images without any compression or quality loss.
- **100% Offline & Private:** Runs entirely on your local machine.

---

## Installation

1. Clone this repository.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the following command in your terminal:
```bash
python remove_bg_smart.py <input_path> <output_path> [tolerance] [low_tolerance]
```

### Parameters:
- **`input_path`**: Path to your source image (e.g., `.jpg`, `.png`).
- **`output_path`**: Path to save the transparent result (must be `.png` to support transparency).
- **`tolerance`** *(optional, default: 40)*: Color threshold limit. Higher values remove colors slightly further from the background color.
- **`low_tolerance`** *(optional, default: 15)*: Lower limit for edge blending. Pixels with distance lower than this become fully transparent.

### Example:
```bash
python remove_bg_smart.py images/input.jpg images/output.png 40 15
```

---

<a name="tiếng-việt"></a>
# Smart Background Remover (Dành cho Logo & Đồ Họa)

Công cụ Python chạy offline với độ chính xác cao, chuyên dùng để tách nền đơn sắc (trắng, đen...) cho logo, huy hiệu, hình minh họa vẽ tay và icon.

Các công cụ tách nền AI thông thường thường cố gắng dự đoán "chủ thể chính" và thường cắt phạm vào viền tròn trang trí hoặc các nét vẽ mảnh. Công cụ này khắc phục hoàn hảo điểm yếu đó bằng thuật toán Loang vùng (Flood-fill) dựa trên khoảng cách màu tính từ các cạnh ngoài.

## Các Tính Năng Nổi Bật
- **Giữ nguyên chi tiết viền:** Không bao giờ bị lẹm viền tròn trang trí hoặc các nét vẽ mỏng ở rìa ngoài.
- **Bảo vệ chi tiết bên trong:** Chỉ loại bỏ phần nền tiếp xúc với cạnh ngoài. Các mảng màu trắng bên trong (như lòng mắt, cổ áo, họa tiết trong) được giữ nguyên 100%.
- **Khử răng cưa cực tốt (Soft-Alpha):** Tạo vùng chuyển tiếp trong suốt mượt mà ở rìa ngoài để loại bỏ hoàn toàn viền hào quang trắng.
- **Độ phân giải nguyên bản:** Hỗ trợ xử lý ảnh 2K, 4K, 8K+ mà không bị nén hay bóp chất lượng.
- **100% Ngoại tuyến:** Chạy trực tiếp trên máy của bạn, không cần tải ảnh lên internet.

## Hướng dẫn sử dụng

Chạy lệnh sau trong Terminal/PowerShell:
```bash
python remove_bg_smart.py <đường_dẫn_ảnh_gốc> <đường_dẫn_ảnh_đầu_ra> [tolerance] [low_tolerance]
```

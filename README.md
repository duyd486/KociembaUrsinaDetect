#  Rubik Cube Kociemba
> Một phần mềm sử dụng python, openCv và thuật toán kociemba để hỗ trợ giải rubik

---

## 🧩 Tính năng nổi bật

- Sử dụng OpenCv để nhận diện khối rubik, lấy trực tiếp từ camera và khối rubik của người dùng
- Có các mô hình 3D, chức năng để hỗ trợ giúp dễ sử dụng, dễ hiểu các hoạt động và thao tác hơn
- Ứng dụng thuật toán Kociemba, hỗ trợ giải khối rubik trong khoảng 20 bước trở lại, giúp nhanh chóng tìm ra chuỗi bước giải ngắn nhất

---

## 🛠️ Công nghệ & Công cụ

| Công nghệ / Công cụ | Mục đích |
|---------------------|----------|
| Python          | Ngôn ngữ chính |
| Ursina  | Một game engine nhỏ hỗ trợ đồ họa 3D cho phần mềm |
| Open CV     | Thư viện hỗ trợ nhận diện và xử lí hình ảnh, sử dụng để xử lí khối rubik của người dùng từ camera |
| Numpy  | Thư viện hỗ trợ các phép tính toán, xử lí màu, vector |

---


## 📸 Demo

![image](https://github.com/user-attachments/assets/8b30f71a-14ef-468f-aa77-7903507f7665)

https://github.com/user-attachments/assets/8bc75c7f-b90a-4719-9522-3b91d5e2d49e

https://github.com/user-attachments/assets/9f3bc9a4-80dc-45a8-9c51-48010a75655a

![Demo Screenshot](./Screenshots/demo.png)

---

## Hướng dẫn sử dụng

### Ở màn hình ngoài
- Sẽ có các chức năng cơ bản đã có hướng dẫn
- Ngoài ra, để thao tác với khối rubik, sử dụng các phím U, L, D, B, R, F tương ứng với các mặt của khối trong tiếng anh
- Sử dụng phải chuột để thay đổi góc nhìn
### Khi đang ở trong màn nhận diện
- Sử dụng các phím tương tự trên để nhận màu của mặt khối rubik
- Nếu quét xong, ấn Enter để tiến hành áp vào khối 3D và tiến hành giải. Nếu muốn hủy ấn q.

## 📦 Cài đặt & chạy thử

### Yêu cầu
- Nếu bạn là người mới, nên sử dụng PyCharm để dễ cài đặt
- Máy tính chạy Windows / macOS

### Clone repo

```bash
git clone https://github.com/duyd486/KociembaUrsinaDetect.git
```
### Mở trong Pycharm
- Cài đặt các thư viện: numpy, opencv, kociemba, ursina
- 
- Nhấn Play để chạy thử

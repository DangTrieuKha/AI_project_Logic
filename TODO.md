`Giai đoạn 1`: 1/8 - 4/8
- Xử lí KB khi đi đến 1 ô : Kha [x]
- GUI: hiện được bản đồ: Trân [x]
- Chiến lược chọn nước đi - Ý tưởng : Phát, Hoàng
    - Phát: [x]
    - Hoàng [x]
`Giai đoạn 2`: 6/8 - 10/8
- Xử lí cập nhật lại map sau mỗi action (update_map() trong program): `Kha` []
- Tiếp tục hoàn thiện kb: `Kha` []
- GUI: hiện được map thep program hiện tại, hiện số điểm hiện tại, máu hiện tại (2 thông tin này hiện bên map của agent); kiểm tra lại hàm đọc file input : `Hoàng `[]
- GUI: hiện được map theo kb của agent, cụ thể : `Trân`
    + ô nào agent chưa biết thì tô đen
    + Những ô nào agent có thông tin chính xác thì mới hiện nhận thức về ô đó ( sử dụng truy vấn KB như đã hướng dẫn trong About_KB)
    + Vị trí và hướng hiện tại của agent
- Viết hàm `run()` cho agent : `Phát`

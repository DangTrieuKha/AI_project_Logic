- KB  xử lí logic cho việc xác định 1 ô có pit/healing/wumpus/poison_gas hay không
Ví dụ về cách truy vấn:
 Truy vấn việc có pit hay không tại ô (1,2):
 + Truy vấn ô (1,2) có phải đang có pit không: gọi hàm **is_there_pit(1,2)**
    Hàm trả về True tức là ô (1,2) này chắc chắn có pit, hàm này trả về false tức là không biết
+ Nếu hàm trả về false thì tiếp tục truy vấn: ô (1,2) có phải đang không có pit không: gọi hàm **is_there_not_pit(1,2)**
    Hàm trả về True tức là ô này chắc chắn không có pit, trả về false tức là không biết
+ Nếu cả 2 lần truy vấn đều trả về 'không biết' thì tức là với KB hiện tại chưa xác định được ô (1,2) có pit hay không
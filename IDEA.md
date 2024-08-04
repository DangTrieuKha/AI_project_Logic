Movement strategy 1:
- If the current cell is only containing Stench, then shoot the arrow to one next cell which is not visited yet, then move to that cell.
    - Assume the current cell is (x, y), then the next cell is (x+1, y). The agent will shoot the arrow to (x+1, y) and move to (x+1, y).
    - If no Scream appear, then the Wumpus is not in (x+1, y), the agent will be safe to move to (x+1, y)
    - Now we can assume the Wumpus is in (x, y+1). If the current cell still contains Stench, then the agent will shoot the arrow to (x+1, y+1) and move to (x+1, y+1).
    - If (x+1, y+1) is not containing Stench, then the Wumpus is in (x-1, y). The agent will be safe to move to (x, y+1).
    - If (x+1, y+1) is containing Stench, then the Wumpus maybe in (x+2, y+1) and/or (x, y+1) and/or (x+1, y+2). The agent will shoot the arrow to (x+2, y+1) and move to (x+2, y+1).
    - Continue checking process until the agent finish exploring the map.
- If the current cell is containing Stench and Breeze/Whiff, then shoot the arrow to next cells which is not visited yet until a Scream appear, then move to that cell.
    - After move to the cell which the Scream appear, if there is no Stench, go around the location to find the Pit.
    - If there is still Stench, continue the checking process above.
- If the current cell is only containing Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information.
- If the current cell is only containing Glow, then move around to find the Healing Potion.
- If the current cell is containing Glow and Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information.
- If the current cell is containing Glow and Stench, then shoot the arrow to next cells which is not visited yet until a Scream appear and no Stench remain, then move to other cell to look for the Healing Potion.

Strat của Hoàng:
1. Xử lý Wumpus trong phạm vi 3 ô xung quanh mình
1.1. Trường hợp có 1 Wumpus 
Giả sử ta di chuyển từ ô (x,y-1) đến ô (x,y) và thấy có S(tench), tức là các ô (x-1,y), (x+1,y), (x,y+1) có thể có Wumpus:
- Bắn 1 mũi tên vào ô (x,y+1) vì ta đang hướng mặt về ô này [-100]
    - TH 1: Nếu nghe thấy tiếng thét, tức là Wumpus đã bị giết, cập nhật lại map
    - TH 2: Nếu không nghe thấy tiếng hét, tức là ô đó không có Wumpus. Di chuyển về 1 trong 2 ô (x-1,y-1) hoặc (x+1,y-1) để kiểm tra. Ở đây chọn đi đến ô (x-1,y-1) [-50]: Quay 2 lần về phía sau [-20], di chuyển [-10], quay 1 lần [-10], di chuyển [-10]; nếu đi về ô (x+1,y-1) cũng có thể suy luận tương tự
        - TH 2.1: Nếu ô (x-1,y-1) có S(tench): Wumpus có thể ở ô này (khả năng khá cao)
        - TH 2.2: Nếu ô (x-1,y-1) không có S(tench): Wumpus chắc chắn ở (x+1,y)
    - TH 3: Nếu ô (x-1,y) được đánh dấu là an toàn còn (x+1,y) thì không, Wumpus chắc chắn ở ô (x+1,y). Nếu ngược lại, Wumpus chắc chắn ở ô (x-1,y)

Với các ô có nguy cơ hoặc chắc chắn có Wumpus, việc bắn mũi tên có thể tùy vào chiến thuật (Wumpus chặn đường đến Gold, mở đường thoát thân...).
Chiến thuật này hiệu quả hơn (mất tối đa 150 điểm), so với bắn mũi tên về 3 hướng để kiểm tra (mất 330 điểm).

1.2. Trường hợp có 2 đến 3 Wumpus: Diễn ra sau TH1 của 1.1, sau khi nghe tiếng hét nhưng vẫn thấy Stench: Di chuyển thẳng lên ô của con Wumpus mình đã giết. Lặp lại quy trình như 1.1.

2. Xử lý Pit
Giả sử ta di chuyển từ ô (x,y-1) đến ô (x,y) và thấy có B(reeze), tức là các ô (x-1,y), (x+1,y), (x,y+1) có thể có Pit: Đánh dấu các ô xung quanh đều có nguy cơ có pit và lui về ô an toàn tìm đường khác. Riêng trường hợp này buộc phải tạm thời bỏ qua và xử lý sau khi có đủ dữ kiện.

3. Xử lý Poisonous Gas
Giả sử ta di chuyển từ ô (x,y-1) đến ô (x,y) và thấy có W_H(iff), tức là các ô (x-1,y), (x+1,y), (x,y+1) có thể có Poisonous Gas: Xử lý tương tự như Pit.

4. Xử lý Glow
Giả sử ta di chuyển từ ô (x,y-1) đến ô (x,y) và thấy có G_L(ow), tức là các ô (x-1,y), (x+1,y), (x,y+1) có thể có Healing Potion (H_P): 
- Nếu máu dưới 100%: Di chuyển theo hướng kim đồng hồ, kiểm tra các ô (x-1,y) -> (x,y+1) -> (x+1,y) [-90], nếu phát hiện thì nhặt lên. 
- Nếu máu 100%: Lưu lại vị trí, bởi vì có thể phải sử dụng sau

5. Xử lý nhiều đối tượng chồng chéo nhau:
Thứ tự xử lý: Pit -> Wumpus -> Poisonous Gas -> Healing Potion.
Xử lý chi tiết sau.
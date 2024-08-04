Movement strategy 1 (Phát):
- x, y: current position with (1, 1) is the bottom-left corner.

- If the current cell is only containing Stench, then shoot the arrow to one next cell in the front [-100] which is not visited yet, then move to that cell.
    - Assume the current cell is (x, y), then the next cell is (x+1, y). The agent will shoot the arrow to (x+1, y) and move to (x+1, y). [-110]: Shoot an arrow [-100], move forward [-10]
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y), the agent will be safe to move to (x+1, y). And the Wumpus maybe in (x, y-1) or (x, y+1) (then use KB to update the information).
    - Now we can assume the Wumpus is in (x, y+1), and if the current cell still contains Stench, then the agent will shoot the arrow to (x+1, y+1) and move to (x+1, y+1). [-120]: Turn left [-10], shoot an arrow [-100], move forward [-10]
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y+1), the agent will be safe to move to (x+1, y+1)
    - If (x+1, y+1) is not containing Stench, then the Wumpus is in (x, y-1). The agent will be safe to move to (x, y+1).
    - If (x+1, y+1) is containing Stench, then the Wumpus maybe in (x+2, y+1) and/or (x, y+1) and/or (x+1, y+2). The agent will shoot the arrow to (x+1, y+2) and move to (x+1, y+2). [-110]: Shoot an arrow [-100], move forward [-10]
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y+2), the agent will be safe to move to (x+1, y+2)
    - Continue checking process until the agent finish exploring the map.

- If the current cell is only containing Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information.

- If the current cell is only containing Glow, then move around to find the Healing Potion. [-10] - [-100]: move forward [-10], turn around [-20], move forward [-10], turn left | turn right [-10], move forward [-10], turn around [-20], move forward[-10], move forward[-10]

- If the current cell (x, y) is containing Stench and Breeze/Whiff, then shoot the arrow to next cells which is not visited yet until a Scream appear, then move to that cell. [-110] - [-340]: Shoot an arrow [-100], turn left | turn right [-10], shoot an arrow[-100], turn around [-20], shoot an arrow [-100], move forward [-10]
    - After move to the cell which the Scream appear, if there is no Stench, update KB there is 1-2 Pit in two other cells.
    - If there is still Stench and/or Breeze, continue the checking process above.

- If the current cell is containing Glow and Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information. [-10]: move forward [-10]

- If the current cell is containing Glow and Stench, then shoot the arrow to next cells which is not visited yet until (a Scream appear and no Stench remain) or shoot 2 time, then update the Wumpus location and move to other cell to look for the Healing Potion.
    - If there is 1 Wumpus (the above condition): [-120] - [-220]:
        - Scream appear at first arrow [-120] - [-160]: Shoot an arrow [-100], turn left | turn right [-10], move forward [-10], turn around [-20], move forward [-10], move forward [-10]
        - Scream appear at second arrow [-220] - [-320]: Shoot an arrow [-100], turn left | turn right [-10], shoot an arrow [-100], move forward [-10], turn around [-20], move forward [-10], turn right | turn left [-10], move forward [-10], turn around [-20], move forward [-10], turn left | turn right [-10], move forward [-10]
        - No scream appear, then the Wumpus is in the remaining cell [-220] - [-270]: Shoot an arrow [-100], turn left | turn right [-10], shoot an arrow [-100], move forward [-10], turn around [-20], move forward [-10], turn left | turn right [-10], move forward [-10]
            - If still no Potion, then the Potion is in the same cell with the Wumpus, update KB and return to get if necessary.
    - If there are more than 1 Wumpus (a Scream appear but Stench remain): Shoot all direction and update the KB, then move to all cell to look for the Healing Potion. [-340] - [-440]: Shoot an arrow [-100], turn left | turn right [-10], shoot an arrow [-100], turn around [-20], shoot an arrow [-100], move forward [-10], turn around [-20], move forward [-10], turn left | turn right [-10], move forward [-10], turn around [-20], move forward [-10], turn left | turn right [-10], move forward [-10]

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
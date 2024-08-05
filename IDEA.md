Movement strategy 1 (Phát):
- x, y: current position with (1, 1) is the bottom-left corner.

- Using KB: Current cell is (x, y)
    - If there is a Wumpus in (x, y+1), and there maybe Pit in other cells but KB do not know exactly where.
        - Using KB to check if any other cells safe to move to. Choose between safe cells and cell (x, y+1) to move to by the cost of actions.
    - Other cases:
        - If there is a safe cell to move to, then move to that cell.
        - If there is no safe cell, and KB do not return any useful information, then process as following.

>__Note__:\
    - All the action "Shoot an arrow" below will only be considered finished when there isn't any Scream after that action.
    - Number of arrows shooted is $k$, $m$, $n$, e.t.c.
    - Every time a cell is visited, the agent will update the KB with the information of that cell.
- If the current cell is only containing Stench:
    - Assume the current cell is (x, y), and the next cell is (x+1, y). The agent will shoot the arrow to (x+1, y) and move to (x+1, y). __`-100k-10`__: Shoot an arrow __`-100k`__, move forward __`-10`__.
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y), the agent will be safe to move to (x+1, y). And the Wumpus maybe in (x, y-1) or (x, y+1) (then use KB to update the information).
    - Now we can assume the Wumpus is in (x, y+1), and if the current cell still contains Stench, then the agent will shoot the arrow to (x+1, y+1) and move to (x+1, y+1). __`-100k-20`__: Turn left __`-10`__, shoot an arrow __`-100k`__, move forward __`-10`__
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y+1), the agent will be safe to move to (x+1, y+1)
    - If (x+1, y+1) is not containing Stench, then the Wumpus is in (x, y-1). The agent will be safe to move to (x, y+1).
    - If (x+1, y+1) is containing Stench, then the Wumpus maybe in (x+2, y+1) and/or (x, y+1) and/or (x+1, y+2). The agent will shoot the arrow to (x+1, y+2) and move to (x+1, y+2). __`-100k-10`__: Shoot an arrow __`-100k`__, move forward __`-10`__
        - If Scream appear, update map and continue exploring the map.
        - If no Scream appear, then the Wumpus is not in (x+1, y+2), the agent will be safe to move to (x+1, y+2)
    - Continue checking process until the agent finish exploring the map.

- If the current cell is only containing Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information.

- If the current cell is only containing Glow, then move around to find the Healing Potion. __`-20`__ - __`-110`__: move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn left | turn right __`-10`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, move forward __`-10`__, grab the Potion __`-10`__

- If the current cell (x, y) is containing Stench and Breeze/Whiff, then shoot the arrow to next cells which is not visited yet until a Scream appear, then move to that cell. __`-100k-10`__ - __`-100(k+m+n)-40`__: Shoot an arrow __`-100k`__, turn left | turn right __`-10`__, shoost an arrow __`-100m`__, turn around __`-20`__, shoot an arrow __`-100n`__, move forward __`-10`__
    - After move to the cell which the Scream appear, if there is no Stench, update KB there is 1-2 Pit in two other cells.
    - If there is still Stench and/or Breeze, continue the checking process above.

- If the current cell is containing Glow and Breeze/Whiff, then move to the next cell which is not visited yet, and go back if necessary and having enough information. __`-10`__: move forward __`-10`__

- If the current cell is containing Glow and Stench, then shoot the arrow to next cells which is not visited yet until (a Scream appear and no Stench remain) or shoot 2 time, then update the Wumpus location and move to other cell to look for the Healing Potion.
    - If there is 1 Wumpus (the above condition): __`-100k-20`__ - __`-100(k+m)-20`__:
        - Scream appear at first arrow __`-100k-20`__ - __`-100k-60`__: Shoot an arrow __`-100k`__, turn left | turn right __`-10`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, move forward __`-10`__
        - Scream appear at second arrow __`-100(k+m)-20`__ - __`-100(k+m)-120`__: Shoot an arrow __`-100k`__, turn left | turn right __`-10`__, shoot an arrow __`-100m`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn right | turn left __`-10`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn left | turn right __`-10`__, move forward __`-10`__
        - No scream appear, then the Wumpus is in the remaining cell __`-100(k+m)-20`__ - __`-100(k+m)-70`__: Shoot an arrow __`-100k`__, turn left | turn right __`-10`__, shoot an arrow __`-100m`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn left | turn right __`-10`__, move forward __`-10`__
            - If still no Potion, then the Potion is in the same cell with the Wumpus, update KB and return to get if necessary.
    - If there are more than 1 Wumpus (a Scream appear but Stench remain): Shoot all direction and update the KB, then move to all cell to look for the Healing Potion. __`-100(k+m+n)-40`__ - __`-100(k+m+n)-140`__: Shoot an arrow __`-100k`__, turn left | turn right __`-10`__, shoot an arrow __`-100m`__, turn around __`-20`__, shoot an arrow __`-100n`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn left | turn right __`-10`__, move forward __`-10`__, turn around __`-20`__, move forward __`-10`__, turn left | turn right __`-10`__, move forward __`-10`__

Strat của Hoàng (mới)
1. Xử lý Wumpus
Nếu ô (x,y) có Stench, tức là 3 ô xung quanh có thể tồn tại Wumpus.
Sử dụng KB để kiểm tra các ô xung quanh là chắc chắn có, chắc chắn không có và chưa rõ là có Wumpus hay không.

1.1. 3 ô không rõ. Giả sử  từ ô (x,y-1) tiến vào ô (x,y) và hướng về (x,y+1)
- Lặp lại: Liên tục bắn mũi tên vào ô (x,y+1) cho đến khi không còn nghe Scream nữa
- Nếu không còn thấy Stench: Đánh dấu 3 ô đều an toàn
- Nếu vẫn còn thấy Stench:
    - Đánh dấu `W(x-1,y) or W(x+1,y)`
    <!-- - Di chuyển đến một ô an toàn -->
    - Di chuyển đến (x-1,y+1)
    - Nếu có Stench: Đánh dấu `W(x-1,y)`
    - Nếu không có Stench: Đánh dấu `not W(x-1,y)` và `W(x+1,y)`

1.2. 2 ô không rõ. Giả sử  từ ô (x,y-1) tiến vào ô (x,y) và hướng về (x,y+1).
1.2.1. (x-1,y) an toàn. 
- Lặp lại: Liên tục bắn mũi tên vào ô (x,y+1) cho đến khi không còn nghe Scream nữa
- Nếu không còn thấy Stench: Đánh dấu 2 ô đều an toàn
- Nếu vẫn còn thấy Stench:
    - Đánh dấu `W(x+1,y)`
    - Di chuyển đến một ô an toàn
1.2.2. (x,y+1) an toàn
- Đánh dấu `W(x-1,y) or W(x+1,y)`
<!-- - Di chuyển đến một ô an toàn -->
- Di chuyển đến (x-1,y+1)
- Nếu có Stench: Đánh dấu `W(x-1,y)`
- Nếu không có Stench: Đánh dấu `not W(x-1,y)` và `W(x+1,y)`

1.3. 1 ô không rõ
Đánh dấu ô này có Wumpus

2. Xử lý Pit
Nếu ô (x,y) có Breeze, tức là 3 ô xung quanh có thể tồn tại Pit.
Sử dụng KB để kiểm tra các ô xung quanh là chắc chắn có, chắc chắn không có và chưa rõ là có Pit hay không. 
Đánh dấu các ô không rõ thành 1 mệnh đề là không an toàn. Di chuyển đến một ô an toàn.

3. Xử lý Poisonous Gas
Nếu ô (x,y) có Whiff, tức là 3 ô xung quanh có thể tồn tại Poisonous Gas.
Sử dụng KB để kiểm tra các ô xung quanh là chắc chắn có, chắc chắn không có và chưa rõ là có Poisonous Gas hay không.
Đánh dấu các ô không rõ thành 1 mệnh đề là không an toàn. Di chuyển đến một ô an toàn.

4. Xử lý Healing Potion
Nếu ô (x,y) có Glow, tức là 3 ô xung quanh có thể tồn tại Healing Potion.
Sử dụng KB để kiểm tra các ô xung quanh là chắc chắn có, chắc chắn không có và chưa rõ là có Healing Potion hay không.
Nếu như máu dưới 100%: Tìm cách lấy được Healing Potion.

5. Xử lý các trường hợp hỗn hợp
Thứ tự xử lý các đối tượng nguy hiểm: Pit -> Wumpus -> Poisonous Gas.
Xử lý Healing Potion cùng lúc xử lý các đối tượng nguy hiểm.
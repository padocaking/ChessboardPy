<pre>
  +-------------------------------------+
  |      - ARDUINO x FUNÇÕES Flow: -    |
  +-------------------------------------+
  | 1. REST (waiting reed low) =>       |
  | 2. => ARDUINO (reed low) =>         |
  | 3. => Serial.write(xy) =>           |
  | 4. => Serial.read(showmoves) =>     |
  | 5. => calculate_piece_move(x,y) =>  |
  | 6. => Serial.write([xy, xy...]) =>  |
  | 7. => Serial.read(led) =>           |
  | 8. => ARDUINO (led) =>              |
  | 9. => REST (waiting reed high) =>   |
  | 10. => ARDUINO (reed high) =>       |
  | 11. => Serial.write(xy) =>          |
  | 12. => Serial.read(makemove) =>     |
  | 13. => make_move(x,y,newX,newY) =>  |
  | 14. => get_best_move() =>           |
  | 15. => Serial.write(xy) =>          |
  | 16. => Serial.read(stckfsh move) => |
  | 17. => ARDUINO (led) =>             |
  | 18. => REST (waiting reed high) =>  |
  | 19. => ARDUINO (reed high) =>       |
  | 20. => REST (waiting reed low)...   |
  +-------------------------------------+
</pre>

[Stockfish download](https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-avx2.zip)

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Xếp Khối Màu - Block Puzzle",
    page_icon="🟩",
    layout="centered",
)

st.title("🟩 Game Xếp Khối Màu (Style Block Blast)")
st.markdown(
    "**Cách chơi:** Dùng chuột click vào khối hình bên dưới, sau đó click vào vị trí trên bảng 10x10 để đặt khối vào. "
    "Xếp **đầy một hàng ngang hoặc cột dọc** để làm nổ khối và ghi điểm! Trò chơi kết thúc khi không còn chỗ đặt."
)

# Mã nguồn HTML5/JavaScript dựng logic game xếp hình kéo thả/click phẳng
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; }
  #container { max-width: 500px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  #score-board { font-size: 24px; font-weight: bold; margin-bottom: 15px; color: #f59e0b; display: flex; justify-content: space-around; }
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); grid-gap: 4px; background: #334155; padding: 6px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #475569; border-radius: 4px; transition: background 0.15s; cursor: pointer; }
  .cell.filled { box-shadow: inset 0 0 6px rgba(0,0,0,0.3); }
  #shapes-container { display: flex; justify-content: space-around; min-height: 90px; background: #334155; padding: 10px; border-radius: 8px; }
  .shape-box { display: grid; grid-gap: 2px; padding: 5px; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.05); transition: transform 0.2s, background 0.2s; }
  .shape-box:hover { background: rgba(255,255,255,0.15); transform: scale(1.05); }
  .shape-box.selected { background: #f59e0b !important; transform: scale(1.08); box-shadow: 0 0 12px #f59e0b; }
  .s-cell { width: 16px; height: 16px; border-radius: 2px; }
  .empty-s-cell { width: 16px; height: 16px; }
  #game-over { display: none; margin-top: 15px; font-size: 28px; font-weight: bold; color: #ef4444; animation: pulse 1s infinite; }
  #reset-btn { margin-top: 10px; padding: 10px 24px; font-size: 16px; font-weight: bold; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; }
  #reset-btn:hover { background: #059669; }
  @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.03); } 100% { transform: scale(1); } }
</style>
</head>
<body>

<div id="container">
  <div id="score-board">
    <div>Điểm: <span id="score">0</span></div>
    <div>Kỷ lục: <span id="high-score">0</span></div>
  </div>
  
  <div id="grid"></div>
  
  <div id="shapes-container"></div>
  
  <div id="game-over">TRÒ CHƠI KẾT THÚC!</div>
  <button id="reset-btn">Chơi Lại 🔄</button>
</div>

<script>
(() => {
  const BOARD_SIZE = 10;
  let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
  let score = 0;
  let highScore = localStorage.getItem('block_puzzle_high') || 0;
  let currentShapes = [];
  let selectedShapeIndex = null;

  // Bảng màu sắc rực rỡ phong cách Block Blast
  const colors = {
    1: '#ef4444', // Đỏ
    2: '#3b82f6', // Xanh dương
    3: '#10b981', // Xanh lá
    4: '#a855f7', // Tím
    5: '#f59e0b', // Cam vàng
    6: '#06b6d4'  // Xanh ngọc
  };

  // Định nghĩa kho thư viện các khối hình học
  const rawShapes = [
    [[1]], // Khối đơn 1x1
    [[1, 1]], // Khối ngang 1x2
    [[1, 1, 1]], // Khối ngang 1x3
    [[1], [1]], // Khối dọc 2x1
    [[1], [1], [1]], // Khối dọc 3x1
    [[1, 1], [1, 1]], // Khối vuông 2x2
    [[1, 1, 1], [0, 1, 0]], // Khối chữ T
    [[1, 0], [1, 0], [1, 1]], // Khối chữ L
    [[0, 1], [0, 1], [1, 1]], // Khối chữ L ngược
    [[1, 1, 0], [0, 1, 1]]  // Khối chữ Z
  ];

  document.getElementById('high-score').textContent = highScore;
  const gridDOM = document.getElementById('grid');
  const shapesContainerDOM = document.getElementById('shapes-container');
  const gameOverDOM = document.getElementById('game-over');

  // 1. Tạo ma trận bảng chơi ảo
  function initBoard() {
    gridDOM.innerHTML = '';
    for (let r = 0; r < BOARD_SIZE; r++) {
      for (let c = 0; c < BOARD_SIZE; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.r = r;
        cell.dataset.c = c;
        cell.addEventListener('click', () => handleCellClick(r, c));
        gridDOM.appendChild(cell);
      }
    }
  }

  // 2. Tạo ngẫu nhiên 3 khối hình mới cho lượt lựa chọn
  function spawnShapes() {
    shapesContainerDOM.innerHTML = '';
    currentShapes = [];
    selectedShapeIndex = null;

    for (let i = 0; i < 3; i++) {
      const randType = Math.floor(Math.random() * rawShapes.length);
      const randColor = Math.floor(Math.random() * 6) + 1;
      const matrix = rawShapes[randType];

      currentShapes.push({ matrix, color: randColor, used: false });

      const box = document.createElement('div');
      box.className = 'shape-box';
      box.id = `shape-${i}`;
      box.style.gridTemplateRows = `repeat(${matrix.length}, 1fr)`;
      box.style.gridTemplateColumns = `repeat(${matrix[0].length}, 1fr)`;
      
      box.addEventListener('click', (e) => {
        if (currentShapes[i].used) return;
        document.querySelectorAll('.shape-box').forEach(b => b.classList.remove('selected'));
        box.classList.add('selected');
        selectedShapeIndex = i;
        e.stopPropagation();
      });

      for (let r = 0; r < matrix.length; r++) {
        for (let c = 0; c < matrix[0].length; c++) {
          const sCell = document.createElement('div');
          if (matrix[r][c]) {
            sCell.className = 's-cell';
            sCell.style.background = colors[randColor];
          } else {
            sCell.className = 'empty-s-cell';
          }
          box.appendChild(sCell);
        }
      }
      shapesContainerDOM.appendChild(box);
    }
  }

  // Cập nhật giao diện màu sắc của bảng 10x10 dựa trên dữ liệu mảng
  function renderBoard() {
    const cells = gridDOM.children;
    for (let r = 0; r < BOARD_SIZE; r++) {
      for (let c = 0; c < BOARD_SIZE; c++) {
        const idx = r * BOARD_SIZE + c;
        const val = board[r][c];
        if (val > 0) {
          cells[idx].style.background = colors[val];
          cells[idx].classList.add('filled');
        } else {
          cells[idx].style.background = '#475569';
          cells[idx].classList.remove('filled');
        }
      }
    }
  }

  // Kiểm tra khối hình có vừa khít để đặt xuống vị trí (startR, startC) không
  function canPlace(matrix, startR, startC) {
    if (startR + matrix.length > BOARD_SIZE || startC + matrix[0].length > BOARD_SIZE) return false;
    for (let r = 0; r < matrix.length; r++) {
      for (let c = 0; c < matrix[0].length; c++) {
        if (matrix[r][c] && board[startR + r][startC + c] > 0) return false;
      }
    }
    return true;
  }

  // 3. Xử lý đặt khối hình khi người dùng bấm chọn một ô trên bảng
  function handleCellClick(startR, startC) {
    if (selectedShapeIndex === null) return;
    const shape = currentShapes[selectedShapeIndex];

    if (canPlace(shape.matrix, startR, startC)) {
      // Ghi dữ liệu khối vào mảng board
      for (let r = 0; r < shape.matrix.length; r++) {
        for (let c = 0; c < shape.matrix[0].length; c++) {
          if (shape.matrix[r][c]) {
            board[startR + r][startC + c] = shape.color;
          }
        }
      }

      // Đánh dấu khối này đã được sử dụng
      shape.used = true;
      document.getElementById(`shape-${selectedShapeIndex}`).style.opacity = '0.2';
      document.getElementById(`shape-${selectedShapeIndex}`).classList.remove('selected');
      selectedShapeIndex = null;

      // Cộng điểm khi đặt thành công khối hình
      score += 10;
      
      checkCombos();
      renderBoard();

      // Nếu cả 3 khối đều dùng hết, tự động hồi cấp 3 khối mới
      if (currentShapes.every(s => shape.used || s.used)) {
        spawnShapes();
      }

      // Kiểm tra xem người chơi còn đường đi nào hợp lệ không
      if (checkGameOver()) {
        gameOverDOM.style.display = 'block';
      }
    }
  }

  // 4. Quét kiểm tra combo làm nổ hàng ngang / cột dọc đầy đủ màu
  function checkCombos() {
    let rowsToClear = [];
    let colsToClear = [];

    // Kiểm tra hàng ngang
    for (let r = 0; r < BOARD_SIZE; r++) {
      if (board[r].every(val => val > 0)) rowsToClear.push(r);
    }
    // Kiểm tra cột dọc
    for (let c = 0; c < BOARD_SIZE; c++) {
      let full = true;
      for (let r = 0; r < BOARD_SIZE; r++) {
        if (board[r][c] === 0) { full = false; break; }
      }
      if (full) colsToClear.push(c);
    }

    // Làm nổ các khối và tính điểm combo thưởng lớn
    const totalLines = rowsToClear.length + colsToClear.length;
    if (totalLines > 0) {
      rowsToClear.forEach(r => board[r].fill(0));
      colsToClear.forEach(c => {
        for (let r = 0; r < BOARD_SIZE; r++) board[r][c] = 0;
      });

      score += totalLines * 100; // 100 điểm cho mỗi hàng biến mất
      if (score > highScore) {
        highScore = score;
        localStorage.setItem('block_puzzle_high', highScore);
        document.getElementById('high-score').textContent = highScore;
      }
    }
    document.getElementById('score').textContent = score;
  }

  // 5. Thuật toán kiểm tra điều kiện thua cuộc
  function checkGameOver() {
    // Duyệt qua tất cả các khối hình còn tồn tại chưa dùng
    for (let i = 0; i < currentShapes.length; i++) {
      const shape = currentShapes[i];
      if (shape.used) continue;

      // Tìm xem có bất kỳ vị trí trống nào trên bảng nhét vừa khối không
      for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
          if (canPlace(shape.matrix, r, c)) {
            return false; // Còn đi tiếp được
            }
}
}
}
return true; // Không còn chỗ trống để vừa bất kỳ khối nào
}
// Khởi động lại vòng chơi mới
function restartGame() {
board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
score = 0;
document.getElementById('score').textContent = score;
gameOverDOM.style.display = 'none';
initBoard();
spawnShapes();
renderBoard();
}
document.getElementById('reset-btn').addEventListener('click', restartGame);
// Chạy thiết lập lần đầu tiên khi tải game
initBoard();
spawnShapes();
renderBoard();
})();



"""

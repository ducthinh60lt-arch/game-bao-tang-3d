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

game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; }
  #container { max-width: 450px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  #score-board { font-size: 22px; font-weight: bold; margin-bottom: 15px; color: #f59e0b; display: flex; justify-content: space-around; }
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); grid-gap: 4px; background: #334155; padding: 6px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #475569; border-radius: 4px; transition: background 0.1s; cursor: pointer; }
  .cell.filled { box-shadow: inset 0 0 6px rgba(0,0,0,0.4); }
  #shapes-container { display: flex; justify-content: space-around; align-items: center; min-height: 100px; background: #334155; padding: 10px; border-radius: 8px; }
  .shape-box { display: grid; grid-gap: 2px; padding: 8px; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.05); transition: transform 0.2s, background 0.2s; }
  .shape-box:hover { background: rgba(255,255,255,0.12); transform: scale(1.05); }
  .shape-box.selected { background: rgba(245, 158, 11, 0.3) !important; border: 2px solid #f59e0b; transform: scale(1.05); }
  .s-cell { width: 14px; height: 16px; border-radius: 3px; }
  .empty-s-cell { width: 14px; height: 16px; }
  #game-over { display: none; margin-top: 15px; font-size: 26px; font-weight: bold; color: #ef4444; }
  #reset-btn { margin-top: 15px; padding: 10px 24px; font-size: 16px; font-weight: bold; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; }
  #reset-btn:hover { background: #059669; }
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

  const colors = {
    1: '#ef4444', 2: '#3b82f6', 3: '#10b981', 
    4: '#a855f7', 5: '#f59e0b', 6: '#06b6d4'
  };

  const rawShapes = [
    [[1]], 
    [[1, 1]], 
    [[1, 1, 1]], 
    [[1], [1]], 
    [[1], [1], [1]], 
    [[1, 1], [1, 1]], 
    [[1, 1, 1], [0, 1, 0], [0, 0, 0]], 
    [[1, 0, 0], [1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]], 
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
  ];

  document.getElementById('high-score').textContent = highScore;
  const gridDOM = document.getElementById('grid');
  const shapesContainerDOM = document.getElementById('shapes-container');
  const gameOverDOM = document.getElementById('game-over');

  function initBoard() {
    gridDOM.innerHTML = '';
    for (let r = 0; r < BOARD_SIZE; r++) {
      for (let c = 0; c < BOARD_SIZE; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.addEventListener('click', () => handleCellClick(r, c));
        gridDOM.appendChild(cell);
      }
    }
  }

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

  function canPlace(matrix, startR, startC) {
    if (startR + matrix.length > BOARD_SIZE || startC + matrix[0].length > BOARD_SIZE) return false;
    for (let r = 0; r < matrix.length; r++) {
      for (let c = 0; c < matrix[0].length; c++) {
        if (matrix[r][c] && board[startR + r][startC + c] > 0) return false;
      }
    }
    return true;
  }

  function handleCellClick(startR, startC) {
    if (selectedShapeIndex === null) return;
    const shape = currentShapes[selectedShapeIndex];

    if (canPlace(shape.matrix, startR, startC)) {
      for (let r = 0; r < shape.matrix.length; r++) {
        for (let c = 0; c < shape.matrix[0].length; c++) {
          if (shape.matrix[r][c]) {
            board[startR + r][startC + c] = shape.color;
          }
        }
      }

      shape.used = true;
      const boxDOM = document.getElementById(`shape-${selectedShapeIndex}`);
      boxDOM.style.visibility = 'hidden';
      boxDOM.classList.remove('selected');
      selectedShapeIndex = null;

      score += 15;
      checkCombos();
      renderBoard();

      if (currentShapes.every(s => s.used)) {
        spawnShapes();
      }

      if (checkGameOver()) {
        gameOverDOM.style.display = 'block';
      }
    }
  }

  function checkCombos() {
    let rowsToClear = [];
    let colsToClear = [];

    for (let r = 0; r < BOARD_SIZE; r++) {
      if (board[r].every(val => val > 0)) rowsToClear.push(r);
    }
    for (let c = 0; c < BOARD_SIZE; c++) {
      let full = true;
      for (let r = 0; r < BOARD_SIZE; r++) {
        if (board[r][c] === 0) { full = false; break; }
      }
      if (full) colsToClear.push(c);
    }

    const totalLines = rowsToClear.length + colsToClear.length;
    if (totalLines > 0) {
      rowsToClear.forEach(r => board[r].fill(0));
      colsToClear.forEach(c => {
        for (let r = 0; r < BOARD_SIZE; r++) board[r][c] = 0;
      });

      score += totalLines * 100;
      if (score > highScore) {
        highScore = score;
        localStorage.setItem('block_puzzle_high', highScore);
        document.getElementById('high-score').textContent = highScore;
      }
    }
    document.getElementById('score').textContent = score;
  }

  function checkGameOver() {
    for (let i = 0; i < currentShapes.length; i++) {
      const shape = currentShapes[i];
      if (shape.used) continue;

      for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
          if (canPlace(shape.matrix, r, c)) {
            return false;
          }
        }
      }
    }
    return currentShapes.every(s => s.used) ? false : true;
  }

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

  initBoard();
  spawnShapes();
  renderBoard();
})();
</script>
</body>
</html>
"""

components.html(game_html, height=620, scrolling=False)


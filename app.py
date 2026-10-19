import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Siêu Game Xếp Khối Màu - Block Puzzle Pro",
    page_icon="🟩",
    layout="centered",
)

st.title("🟩 Game Xếp Khối Màu (Block Blast Pro)")
st.markdown(
    "**Cách chơi:** Click chuột trái vào khối hình bên dưới để chọn, "
    "sau đó click vào một ô trên bảng 10x10 để đặt khối xuống. "
    "Xếp kín một hàng ngang hoặc cột dọc để làm nổ khối và ghi điểm! Tùy chỉnh độ khó tại màn hình Menu."
)

# TRÌNH PHÁT NHẠC NỀN CHILL: Great Little Things (Spotify Player)
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# MÃ NGUỒN GAME HOÀN THIỆN ĐÃ ĐƯỢC NẠP ĐẦY ĐỦ CÁC KHỐI HÌNH
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; user-select: none; }
  #container { max-width: 450px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; min-height: 520px; box-sizing: border-box; }
  
  /* Menu mở đầu */
  #start-screen { position: absolute; inset: 0; background: #1e293b; border-radius: 16px; z-index: 10; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
  #start-title { font-size: 28px; font-weight: bold; color: #f59e0b; margin-bottom: 25px; }
  .menu-section { width: 80%; margin-bottom: 25px; text-align: left; }
  .menu-label { font-size: 14px; margin-bottom: 6px; color: #94a3b8; font-weight: bold; }
  
  select, button.setting-toggle { width: 100%; padding: 10px 14px; font-size: 15px; font-weight: bold; border-radius: 6px; border: 2px solid #475569; background: #334155; color: white; cursor: pointer; outline: none; }
  button.setting-toggle { background: #1e293b; border-color: #f59e0b; color: #f59e0b; }
  button.setting-toggle.active { background: #10b981; color: white; border-color: #10b981; }
  
  #start-btn { width: 80%; padding: 12px 0; font-size: 18px; font-weight: bold; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(59,130,246,0.4); margin-top: 15px; }
  #start-btn:hover { background: #2563eb; }
  
  /* Bàn cờ chính */
  #game-area { display: none; }
  #score-board { font-size: 22px; font-weight: bold; margin-bottom: 15px; color: #f59e0b; display: flex; justify-content: space-around; }
  #diff-indicator { font-size: 14px; background: #334155; padding: 2px 10px; border-radius: 12px; color: #cbd5e1; }
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); grid-gap: 4px; background: #334155; padding: 6px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #475569; border-radius: 4px; transition: background 0.1s; cursor: pointer; }
  .cell.filled { box-shadow: inset 0 0 6px rgba(0,0,0,0.4); }
  
  /* Khay chứa khối hình */
  #shapes-container { display: flex; justify-content: space-around; align-items: center; min-height: 120px; background: #334155; padding: 10px; border-radius: 8px; }
  .shape-box { display: grid; grid-gap: 2px; padding: 8px; border-radius: 6px; background: rgba(255,255,255,0.03); cursor: pointer; border: 2px solid transparent; }
  .shape-box.selected { border-color: #f59e0b; background: rgba(245, 158, 11, 0.2); transform: scale(1.05); }
  .s-cell { width: 14px; height: 14px; border-radius: 2px; }
  .empty-s-cell { width: 14px; height: 14px; }
  
  #game-over { display: none; margin-top: 15px; font-size: 26px; font-weight: bold; color: #ef4444; }
  #reset-btn { margin-top: 15px; padding: 10px 24px; font-size: 15px; font-weight: bold; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; margin-right: 8px; }
  #config-btn { margin-top: 15px; padding: 10px 24px; font-size: 15px; font-weight: bold; background: #64748b; color: white; border: none; border-radius: 6px; cursor: pointer; }
</style>
</head>
<body>

<div id="container">
  <!-- MENU MỞ ĐẦU / CÀI ĐẶT -->
  <div id="start-screen">
    <div id="start-title">🧱 BLOCK PUZZLE PRO</div>
    
    <div class="menu-section">
      <div class="menu-label">⚙️ CẤP ĐỘ THỬ THÁCH:</div>
      <select id="difficulty-select">
        <option value="easy">DỄ (Khối Nhỏ Thư Giãn)</option>
        <option value="medium" selected>VỪA (Cân Bằng Chuẩn Gốc)</option>
        <option value="hard">KHÓ (Siêu Khối Thách Thức)</option>
      </select>
    </div>

    <div class="menu-section">
      <div class="menu-label">🔊 HIỆU ỨNG NỔ KHỐI (SFX):</div>
      <button id="sfx-toggle" class="setting-toggle active" type="button">ÂM THANH: ĐANG MỞ</button>
    </div>

    <button id="start-btn" type="button">ÁP DỤNG & VÀO CHƠI 🎮</button>
  </div>

  <!-- PHẦN GAMEPLAY CHÍNH -->
  <div id="game-area">
    <div id="score-board">
      <div>Điểm: <span id="score">0</span> <span id="diff-indicator">Vừa</span></div>
      <div>Kỷ lục: <span id="high-score">0</span></div>
    </div>
    
    <div id="grid"></div>
    <div id="shapes-container"></div>
    
    <div id="game-over">TRÒ CHƠI KẾT THÚC!</div>
    <button id="reset-btn">Chơi Lại 🔄</button>
    <button id="config-btn">Cấu Hình 🏠</button>
  </div>
</div>

<script>
(() => {
  const BOARD_SIZE = 10;
  let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
  let score = 0;
  let highScore = localStorage.getItem('block_puzzle_high') || 0;
  let currentShapes = [];
  let selectedShapeIndex = null;
  let currentDifficulty = 'medium';
  let isGameInitialized = false;
  let sfxEnabled = true;

  const colors = {
    1: '#ef4444', 2: '#3b82f6', 3: '#10b981', 
    4: '#a855f7', 5: '#f59e0b', 6: '#06b6d4'
  };

  // ĐÃ SỬA LỖI: Điền đầy đủ dữ liệu ma trận hình học cho các khối
  const shapesPool = {
    easy: [
      [[1]], 
      [[1, 1]], 
      [[1], [1]], 
      [[1, 1], [1, 0]]
    ],
    medium: [
      [[1]], 
      [[1, 1]], 
      [[1, 1, 1]], 
      [[1], [1]], 
      [[1], [1], [1]], 
      [[1, 1], [1, 1]], 
      [[1, 1, 1], [0, 1, 0], [0, 0, 0]], 
      [[1, 1, 1], [1, 0, 0], [1, 0, 0]], 
      [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
    ],
    hard: [
      [[1, 1], [1, 1]], 
      [[1, 1, 1, 1]], 
      [[1], [1], [1], [1]], 
      [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 
      [[1, 1, 1], [1, 0, 0], [1, 0, 0]], 
      [[1, 1, 1], [0, 1, 0], [0, 1, 0]]
    ]
  };

  document.getElementById('high-score').textContent = highScore;
  const gridDOM = document.getElementById('grid');
  const shapesContainerDOM = document.getElementById('shapes-container');
  const gameOverDOM = document.getElementById('game-over');
  const startScreen = document.getElementById('start-screen');
  const gameArea = document.getElementById('game-area');
  const diffIndicator = document.getElementById('diff-indicator');
  const sfxToggle = document.getElementById('sfx-toggle');
  const startBtn = document.getElementById('start-btn');

  let audioCtx = null;
  function playBlastSound() {
    if (!sfxEnabled) return;
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      let osc = audioCtx.createOscillator();
      let gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(550, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(150, audioCtx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + 0.2);
    } catch(e){}
  }

  sfxToggle.addEventListener('click', () => {
    sfxEnabled = !sfxEnabled;
    if (sfxEnabled) {
      sfxToggle.textContent = "ÂM THANH: ĐANG MỞ";
      sfxToggle.classList.add('active');
    } else {
      sfxToggle.textContent = "ÂM THANH: ĐANG TẮT";
      sfxToggle.classList.remove('active');
    }
  });

  startBtn.addEventListener('click', () => {
    const oldDiff = currentDifficulty;
    currentDifficulty = document.getElementById('difficulty-select').value;
    diffIndicator.textContent = currentDifficulty === 'easy' ? 'Dễ' : currentDifficulty === 'hard' ? 'Khó' : 'Vừa';
    
    startScreen.style.display = 'none';
    gameArea.style.display = 'block';
    
    if (!isGameInitialized || oldDiff !== currentDifficulty) {
      restartGame();
      isGameInitialized = true;
    }
    startBtn.textContent = "QUAY LẠI TRẬN ĐẤU 🎮";
  });

  document.getElementById('config-btn').addEventListener('click', () => {
    gameArea.style.display = 'none';
    startScreen.style.display = 'flex';
  });

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

    const pool = shapesPool[currentDifficulty];
    for (let i = 0; i < 3; i++) {
      const randType = Math.floor(Math.random() * pool.length);
      const randColor = Math.floor(Math.random() * 6) + 1;
      const matrix = pool[randType];

      currentShapes.push({ matrix, color: randColor, used: false });

      const box = document.createElement('div');
      box.className = 'shape-box';
      box.id = `shape-${i}`;
      box.style.gridTemplateRows = `repeat(${matrix.length}, 1fr)`;
box.style.gridTemplateColumns = repeat(${matrix.length}, 1fr);
box.addEventListener('click', (e) => {
if (currentShapes[i].used) return;
document.querySelectorAll('.shape-box').forEach(b => b.classList.remove('selected'));
box.classList.add('selected');
selectedShapeIndex = i;
e.stopPropagation();
});
for (let r = 0; r < matrix.length; r++) {
for (let c = 0; c < matrix.length; c++) {
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
const boxDOM = document.getElementById(shape-${selectedShapeIndex});
boxDOM.style.visibility = 'hidden';
boxDOM.classList.remove('selected');
selectedShapeIndex = null;
score += 20;
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
let rowsToClear = [], colsToClear = [];
for (let r = 0; r < BOARD_SIZE; r++) {
if (board[r].every(v => v > 0)) rowsToClear.push(r);
}
for (let c = 0; c < BOARD_SIZE; c++) {
let full = true;
for (let r = 0; r < BOARD_SIZE; r++) { if (board[r][c] === 0) { full = false; break; } }
if (full) colsToClear.push(c);
}
const totalLines = rowsToClear.length + colsToClear.length;
if (totalLines > 0) {
playBlastSound();
rowsToClear.forEach(r => board[r].fill(0));
colsToClear.forEach(c => { for (let r = 0; r < BOARD_SIZE; r++) board[r][c] = 0; });
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
if (canPlace(shape.matrix, r, c)) return false;
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
})();



"""
components.html(game_html, height=590, scrolling=False)

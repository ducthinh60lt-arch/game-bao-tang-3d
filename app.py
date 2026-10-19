import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Siêu Game Xếp Khối Màu - Block Puzzle Pro",
    page_icon="🟩",
    layout="centered",
)

st.title("🟩 Game Xếp Khối Màu (Block Blast Pro)")
st.markdown(
    "**Cách chơi:** Giữ chuột trái vào khối hình bên dưới, **kéo rê khối hình** và thả vào vị trí trống trên bảng 10x10. "
    "Xếp kín hàng hoặc cột để kích nổ ghi điểm! Tùy chỉnh độ khó tại màn hình Menu."
)

# TRÌNH PHÁT NHẠC NỀN CHILL: Great Little Things (Spotify Player)
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# MÃ NGUỒN GAME CSS/HTML5 SỬA HOÀN TOÀN LỖI ĐÓNG BĂNG MẢNG
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; user-select: none; -webkit-user-select: none; }
  #container { max-width: 450px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; min-height: 520px; }
  
  /* Menu mở đầu */
  #start-screen { position: absolute; inset: 0; background: #1e293b; border-radius: 16px; z-index: 10; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
  #start-title { font-size: 28px; font-weight: bold; color: #f59e0b; margin-bottom: 25px; }
  .menu-section { width: 80%; margin-bottom: 25px; text-align: left; }
  .menu-label { font-size: 14px; margin-bottom: 6px; color: #94a3b8; font-weight: bold; }
  
  select, button.setting-toggle { width: 100%; padding: 10px 14px; font-size: 15px; font-weight: bold; border-radius: 6px; border: 2px solid #475569; background: #334155; color: white; cursor: pointer; outline: none; box-sizing: border-box; }
  button.setting-toggle { background: #1e293b; border-color: #f59e0b; color: #f59e0b; }
  button.setting-toggle.active { background: #10b981; color: white; border-color: #10b981; }
  
  #start-btn { width: 80%; padding: 12px 0; font-size: 18px; font-weight: bold; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(59,130,246,0.4); margin-top: 15px; }
  #start-btn:hover { background: #2563eb; }
  
  /* Bàn cờ chính */
  #game-area { display: none; }
  #score-board { font-size: 22px; font-weight: bold; margin-bottom: 15px; color: #f59e0b; display: flex; justify-content: space-around; }
  #diff-indicator { font-size: 14px; background: #334155; padding: 2px 10px; border-radius: 12px; color: #cbd5e1; }
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); grid-gap: 4px; background: #334155; padding: 6px; border-radius: 8px; margin-bottom: 20px; position: relative; }
  .cell { aspect-ratio: 1; background: #475569; border-radius: 4px; transition: background 0.1s; }
  .cell.filled { box-shadow: inset 0 0 6px rgba(0,0,0,0.4); }
  .cell.hovered { background: #64748b !important; opacity: 0.8; }
  
  /* Khay chứa khối hình chưa xếp */
  #shapes-container { display: flex; justify-content: space-around; align-items: center; min-height: 120px; background: #334155; padding: 10px; border-radius: 8px; position: relative; }
  .shape-box { display: grid; grid-gap: 2px; padding: 8px; border-radius: 6px; background: rgba(255,255,255,0.03); touch-action: none; position: relative; z-index: 2; }
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
    <button id="reset-btn">Chroi Lại 🔄</button>
    <button id="config-btn">Menu Cấu Hình 🏠</button>
  </div>
</div>

<script>
(() => {
  const BOARD_SIZE = 10;
  let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
  let score = 0;
  let highScore = localStorage.getItem('block_puzzle_high') || 0;
  let currentShapes = [];
  let dragIdx = null;
  let currentDifficulty = 'medium';
  let isGameInitialized = false;
  let sfxEnabled = true;

  const colors = {
    1: '#ef4444', 2: '#3b82f6', 3: '#10b981', 
    4: '#a855f7', 5: '#f59e0b', 6: '#06b6d4'
  };

  // ĐÃ SỬA: Định hình ma trận rõ ràng, không dùng khai báo trống gây sập luồng JS
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
      [[1, 1, 1], [0, 1, 0]], 
      [[1, 1], [1, 0], [1, 0]], 
      [[1, 1, 0], [0, 1, 1]]
    ],
    hard: [
      [[1, 1], [1, 1]], 
      [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 
      [[1, 1, 1, 1]], 
      [[1], [1], [1], [1]], 
      [[1, 1, 1], [1, 0, 0], [1, 0, 0]], 
      [[1, 1, 1], [0, 0, 1], [0, 0, 1]]
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
      sfxToggle.textContent = "AM THANH: ĐANG MỞ";
      sfxToggle.classList.add('active');
    } else {
      sfxToggle.textContent = "AM THANH: ĐANG TẮT";
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
        cell.dataset.r = r;
        cell.dataset.c = c;
        gridDOM.appendChild(cell);
      }
    }
  }

  function createDraggableShape(shapeData, index) {
    const matrix = shapeData.matrix;
    const box = document.createElement('div');
    box.className = 'shape-box';
    box.id = `shape-${index}`;
    box.style.gridTemplateRows = `repeat(${matrix.length}, 1fr)`;
    box.style.gridTemplateColumns = `repeat(${matrix[0].length}, 1fr)`;

    for (let r = 0; r < matrix.length; r++) {
      for (let c = 0; c < matrix[0].length; c++) {
        const sCell = document.createElement('div');
        if (matrix[r][c]) {
          sCell.className = 's-cell';
          sCell.style.background = colors[shapeData.color];
        } else {
          sCell.className = 'empty-s-cell';
        }
        box.appendChild(sCell);
}
}
box.addEventListener('mousedown', (e) => startDrag(e, index));
box.addEventListener('touchstart', (e) => startDrag(e, index), {passive: false});
return box;
}
let dragDOM = null;
let startX = 0, startY = 0;
function startDrag(e, index) {
if (currentShapes[index].used) return;
e.preventDefault();
dragIdx = index;
dragDOM = document.getElementById(shape-${index});
const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;
const rect = dragDOM.getBoundingClientRect();
startX = clientX - rect.left;
startY = clientY - rect.top;
dragDOM.style.position = 'fixed';
dragDOM.style.width = ${rect.width}px;
dragDOM.style.height = ${rect.height}px;
dragDOM.style.zIndex = '100';
updateDragPosition(clientX, clientY);
window.addEventListener('mousemove', onMouseMove);
window.addEventListener('mouseup', onMouseUp);
window.addEventListener('touchmove', onTouchMove, {passive: false});
window.addEventListener('touchend', onMouseUp);
}
function onMouseMove(e) { updateDragPosition(e.clientX, e.clientY); }
function onTouchMove(e) { updateDragPosition(e.touches[0].clientX, e.touches[0].clientY); }
function updateDragPosition(clientX, clientY) {
if (!dragDOM) return;
dragDOM.style.left = ${clientX - startX}px;
dragDOM.style.top = ${clientY - startY}px;
clearHoverEffects();
const hoverCell = getCellUnderDrag(clientX, clientY);
if (hoverCell) {
const r = parseInt(hoverCell.dataset.r);
const c = parseInt(hoverCell.dataset.c);
showPlacementPreview(currentShapes[dragIdx].matrix, r, c);
}
}
function getCellUnderDrag(clientX, clientY) {
dragDOM.style.pointerEvents = 'none';
const elem = document.elementFromPoint(clientX, clientY);
dragDOM.style.pointerEvents = 'auto';
return (elem && elem.classList.contains('cell')) ? elem : null;
}
function showPlacementPreview(matrix, startR, startC) {
if (!canPlace(matrix, startR, startC)) return;
const cells = gridDOM.children;
for (let r = 0; r < matrix.length; r++) {
for (let c = 0; c < matrix[0].length; c++) {
if (matrix[r][c]) {
const idx = (startR + r) * BOARD_SIZE + (startC + c);
if (cells[idx]) cells[idx].classList.add('hovered');
}
}
}
}
function clearHoverEffects() {
document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('hovered'));
}
function onMouseUp(e) {
window.removeEventListener('mousemove', onMouseMove);
window.removeEventListener('mouseup', onMouseUp);
window.removeEventListener('touchmove', onTouchMove);
window.removeEventListener('touchend', onMouseUp);
if (!dragDOM) return;
const clientX = e.type.startsWith('touch') ? (e.changedTouches[0]?.clientX || 0) : e.clientX;
const clientY = e.type.startsWith('touch') ? (e.changedTouches[0]?.clientY || 0) : e.clientY;
const dropCell = getCellUnderDrag(clientX, clientY);
let placed = false;
if (dropCell) {
const r = parseInt(dropCell.dataset.r);
const c = parseInt(dropCell.dataset.c);
const shape = currentShapes[dragIdx];
if (canPlace(shape.matrix, r, c)) {
for (let sR = 0; sR < shape.matrix.length; sR++) {
for (let sC = 0; sC < shape.matrix[0].length; sC++) {
if (shape.matrix[sR][sC]) board[r + sR][c + sC] = shape.color;
}
}
shape.used = true;
dragDOM.remove();
score += 20;
checkCombos();
placed = true;
}
}
if (!placed) {
dragDOM.style.position = 'relative';
dragDOM.style.left = '0px';
dragDOM.style.top = '0px';
dragDOM.style.width = 'auto';
dragDOM.style.height = 'auto';
}
clearHoverEffects();
renderBoard();
dragDOM = null;
if (currentShapes.every(s => s.used)) spawnShapes();
if (checkGameOver()) gameOverDOM.style.display = 'block';
}
function spawnShapes() {
shapesContainerDOM.innerHTML = '';
currentShapes = [];
const pool = shapesPool[currentDifficulty];
for (let i = 0; i < 3; i++) {
const randType = Math.floor(Math.random() * pool.length);
const randColor = Math.floor(Math.random() * 6) + 1;
currentShapes.push({ matrix: pool[randType], color: randColor, used: false });
const box = createDraggableShape(currentShapes[i], i);
shapesContainerDOM.appendChild(box);
}
}
function renderBoard() {
const cells = gridDOM.children;
for (let r = 0; r < BOARD_SIZE; r++) {
for (let c = 0; c < BOARD_SIZE; c++) {
const idx = r * BOARD_SIZE + c;
if (board[r][c] > 0) {
cells[idx].style.background = colors[board[r][c]];
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
if (currentShapes[i].used) continue;
for (let r = 0; r < BOARD_SIZE; r++) {
for (let c = 0; c < BOARD_SIZE; c++) {
if (canPlace(currentShapes[i].matrix, r, c)) return false;
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

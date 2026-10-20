import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Siêu Game Xếp Khối Màu - Block Puzzle Pro",
    page_icon="🟩",
    layout="centered",
)

st.title("🟩 Game Xếp Khối Màu (Block Blast Pro)")
st.markdown(
    "**Cách chơi:** \n"
    "1. **Click chuột trái** vào một khối hình bên dưới để lựa chọn (khối sẽ đổi sang viền vàng).\n"
    "2. **Click chuột trái** vào một ô bất kỳ trên bảng 10x10 phía trên để đặt khối hình xuống!\n"
    "3. Xếp kín một hàng ngang hoặc cột dọc để phá khối ghi điểm."
)

# 2. Mã nguồn Game HTML5/JS tích hợp Nhạc nền, Menu mở đầu và Cài đặt
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 420px; margin: 0 auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; overflow: hidden; min-height: 520px; }
  
  /* Đầu mục điểm số & Cài đặt */
  #header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
  #score-board { font-size: 22px; font-weight: bold; color: #f59e0b; }
  #btn-settings { background: #334155; border: none; color: white; font-size: 22px; cursor: pointer; padding: 5px 10px; border-radius: 6px; transition: 0.2s; }
  #btn-settings:hover { background: #475569; }

  /* Bảng lưới game 10x10 */
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; background: #334155; padding: 8px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #1e293b; border-radius: 4px; cursor: pointer; transition: background 0.15s; }
  .cell.filled { background: #3b82f6; box-shadow: inset 0 0 5px rgba(255,255,255,0.4); }
  .cell:hover { background: #475569; }

  /* Khu vực chứa 3 khối hình để chọn */
  #pieces { display: flex; justify-content: space-around; min-height: 100px; background: #334155; padding: 12px; border-radius: 8px; align-items: center; }
  .piece { display: grid; gap: 3px; cursor: pointer; padding: 8px; border: 2px dashed #475569; border-radius: 6px; background: rgba(15, 23, 42, 0.4); transition: all 0.2s; }
  .piece.selected { border-color: #f59e0b; background: rgba(245, 158, 11, 0.2); box-shadow: 0 0 10px #f59e0b; }
  .p-cell { width: 14px; height: 14px; border-radius: 2px; }
  .p-cell.filled { background: #3b82f6; }

  /* Màn hình mở đầu & Bảng cài đặt đè lên */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.95); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 26px; font-weight: bold; color: #f59e0b; margin-bottom: 20px; }
  
  .setting-row { width: 80%; margin-bottom: 20px; text-align: left; }
  .setting-label { font-size: 14px; color: #94a3b8; margin-bottom: 5px; font-weight: bold; }
  
  select { width: 100%; padding: 10px; border-radius: 6px; background: #334155; border: 2px solid #475569; color: white; font-size: 15px; outline: none; }
  .btn-main { width: 80%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #10b981; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; }
  .btn-main:hover { background: #059669; }
  .btn-close { background: #ef4444 !important; }
  .btn-close:hover { background: #dc2626 !important; }
</style>
</head>
<body>

<div id="container">
  <!-- MÀN HÌNH MỞ ĐẦU -->
  <div id="start-screen" class="overlay">
    <div class="overlay-title">BLOCK PUZZLE PRO</div>
    <div class="setting-row">
      <div class="setting-label">Chọn nhạc nền khởi đầu:</div>
      <select id="start-music-select">
        <option value="https://mixkit.co">Chill Game Level (Mặc định)</option>
        <option value="https://mixkit.co">Dreaming Big (Nhẹ nhàng)</option>
        <option value="https://mixkit.co">Tech House (Sôi động)</option>
      </select>
    </div>
    <button class="btn-main" onclick="startGame()">BẮT ĐẦU CHƠI</button>
  </div>

  # PANEL CÀI ĐẶT TRONG GAME
  <div id="settings-screen" class="overlay" style="display: none;">
    <div class="overlay-title">⚙️ CÀI ĐẶT</div>
    <div class="setting-row">
      <div class="setting-label">Trạng thái nhạc:</div>
      <select id="music-toggle" onchange="toggleMusicState()">
        <option value="on">Đang Bật (On)</option>
        <option value="off">Tắt Nhạc (Off)</option>
      </select>
    </div>
    <div class="setting-row">
      <div class="setting-label">Đổi bài hát khác:</div>
      <select id="game-music-select" onchange="changeTrack(this.value)">
        <option value="https://mixkit.co">Chill Game Level</option>
        <option value="https://mixkit.co">Dreaming Big</option>
        <option value="https://mixkit.co">Tech House</option>
      </select>
    </div>
    <button class="btn-main btn-close" onclick="closeSettings()">QUAY LẠI GAME</button>
  </div>

  <!-- KHU VỰC GIAO DIỆN CHƠI GAME CHÍNH -->
  <div id="header-bar">
    <div id="score-board">Điểm số: <span id="score">0</span></div>
    <button id="btn-settings" onclick="openSettings()">⚙️</button>
  </div>
  <div id="grid"></div>
  <div id="pieces"></div>
</div>

<!-- Trình phát nhạc ẩn của hệ thống -->
<audio id="bg-audio" loop></audio>

<script>
  const gridEl = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const piecesEl = document.getElementById('pieces');
  const startScreen = document.getElementById('start-screen');
  const settingsScreen = document.getElementById('settings-screen');
  const audioPlayer = document.getElementById('bg-audio');

  let score = 0;
  let board = Array(10).fill().map(() => Array(10).fill(0));
  let selectedPieceIndex = null;
  let isMusicPlaying = true;

  // Ma trận cấu trúc hình khối (Đã điền số 1 và 0 chuẩn không bị lỗi cú pháp)
  const pieceTemplates = [
    [[1]], 
    [[1, 1]], 
    [[1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[1, 0], [1, 1]], 
    [[1, 1, 1], [0, 1, 0]]
  ];
  let currentPieces = [];

  // HÀM KHỞI ĐẦU GAME VÀ TỰ ĐỘNG BẬT NHẠC
  function startGame() {
    const startSelect = document.getElementById('start-music-select');
    audioPlayer.src = startSelect.value;
    
    // Đồng bộ danh mục bài hát ở cả 2 menu
    document.getElementById('game-music-select').value = startSelect.value;
    
    // Phát nhạc tự động ngay khi tương tác bấm nút nhập cuộc
    audioPlayer.play().catch(err => console.log("Chặn phát nhạc tự động: ", err));
    
    // Ẩn màn hình chào để vào game
    startScreen.style.display = 'none';
  }

  // CÁC HÀM ĐIỀU KHIỂN MENU CÀI ĐẶT
  function openSettings() {
    settingsScreen.style.display = 'flex';
  }

  function closeSettings() {
    settingsScreen.style.display = 'none';
  }

  function toggleMusicState() {
    const state = document.getElementById('music-toggle').value;
    if (state === 'off') {
      audioPlayer.pause();
      isMusicPlaying = false;
    } else {
      audioPlayer.play();
      isMusicPlaying = true;
    }
  }

  function changeTrack(url) {
    audioPlayer.src = url;
    if (isMusicPlaying) {
      audioPlayer.play();
    }
  }

  // LOGIC VẬN HÀNH GAME CHÍNH (CLICK-TO-PLACE)
  function initBoard() {
    gridEl.innerHTML = '';
    for (let r = 0; r < 10; r++) {
      for (let c = 0; c < 10; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.row = r;
        cell.dataset.col = c;
        cell.addEventListener('click', () => placePiece(r, c));
        gridEl.appendChild(cell);
      }
    }
  }

  function drawBoard() {
    const cells = gridEl.children;
    for (let r = 0; r < 10; r++) {
      for (let c = 0; c < 10; c++) {
        const idx = r * 10 + c;
        if (board[r][c] === 1) {
          cells[idx].classList.add('filled');
        } else {
          cells[idx].classList.remove('filled');
        }
      }
    }
  }

  function spawnPieces() {
    piecesEl.innerHTML = '';
    currentPieces = [];
    selectedPieceIndex = null;

    for (let i = 0; i < 3; i++) {
      const randIdx = Math.floor(Math.random() * pieceTemplates.length);
      const piece = pieceTemplates[randIdx];
      currentPieces.push(piece);

      const pieceDiv = document.createElement('div');
      pieceDiv.className = 'piece';
      pieceDiv.style.gridTemplateRows = `repeat(${piece.length}, 1fr)`;
      pieceDiv.style.gridTemplateColumns = `repeat(${piece[0].length}, 1fr)`;
      pieceDiv.dataset.index = i;

      piece.forEach(row => {
        row.forEach(val => {
          const pCell = document.createElement('div');
          pCell.className = 'p-cell' + (val ? ' filled' : '');
          pieceDiv.appendChild(pCell);
        });
      });

      pieceDiv.addEventListener('click', () => {
        if (currentPieces[i] === null) return;
        document.querySelectorAll('.piece').forEach(p => p.classList.remove('selected'));
        selectedPieceIndex = i;
        pieceDiv.classList.add('selected');
      });

      piecesEl.appendChild(pieceDiv);
    }
  }

  function placePiece(r, c) {
    if (selectedPieceIndex === null) return;
    const piece = currentPieces[selectedPieceIndex];
    if (!piece) return;

    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
const targetC = c + pc;
if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
return;
}
}
}
}
for (let pr = 0; pr < piece.length; pr++) {
for (let pc = 0; pc < piece[pr].length; pc++) {
if (piece[pr][pc]) {
board[r + pr][c + pc] = 1;
}
}
}
currentPieces[selectedPieceIndex] = null;
const pieceDiv = piecesEl.querySelector([data-index="${selectedPieceIndex}"]);
if (pieceDiv) {
pieceDiv.classList.remove('selected');
pieceDiv.style.opacity = '0.1';
pieceDiv.style.cursor = 'default';
}
selectedPieceIndex = null;
checkLines();
drawBoard();
if (currentPieces.every(p => p === null)) {
spawnPieces();
}
}
function checkLines() {
let rowsToClear = [];
let colsToClear = [];
for (let r = 0; r < 10; r++) {
if (board[r].every(val => val === 1)) rowsToClear.push(r);
}
for (let c = 0; c < 10; c++) {
let colFull = true;
for (let r = 0; r < 10; r++) {
if (board[r][c] === 0) colFull = false;
}
if (colFull) colsToClear.push(c);
}
rowsToClear.forEach(r => {
board[r] = Array(10).fill(0);
score += 10;
});
colsToClear.forEach(c => {
for (let r = 0; r < 10; r++) board[r][c] = 0;
score += 10;
});
scoreEl.innerText = score;
}
// Khởi động nạp dữ liệu bảng lúc ban đầu
initBoard();
spawnPieces();
"""
components.html(game_html, height=580, scrolling=False)

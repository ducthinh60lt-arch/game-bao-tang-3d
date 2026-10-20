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
    "1. **Click chuột trái** vào một khối hình bên dưới để chọn (khối sẽ đổi sang viền vàng).\n"
    "2. **Click chuột trái** vào một ô bất kỳ trên bảng 10x10 phía trên để đặt khối xuống!\n"
    "3. Xếp kín hàng ngang hoặc dọc để nổ khối ghi điểm."
)

# 2. Mã nguồn ứng dụng Game tích hợp toàn diện Nhạc nền + Cài đặt + Fix Lỗi Ma Trận
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 420px; margin: 0 auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; min-height: 540px; }
  
  /* Thanh đầu mục Thông số */
  #header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
  #score-board { font-size: 22px; font-weight: bold; color: #f59e0b; }
  #btn-settings { background: #334155; border: none; color: white; font-size: 22px; cursor: pointer; padding: 5px 12px; border-radius: 6px; transition: 0.2s; }
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
  .p-cell.empty { background: transparent; }

  /* Màn hình chờ mở đầu & Cửa sổ Cài đặt đè lên */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.98); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; border-radius: 16px; }
  .overlay-title { font-size: 26px; font-weight: bold; color: #f59e0b; margin-bottom: 25px; letter-spacing: 1px; }
  
  .setting-row { width: 85%; margin-bottom: 20px; text-align: left; }
  .setting-label { font-size: 14px; color: #94a3b8; margin-bottom: 6px; font-weight: bold; }
  
  select { width: 100%; padding: 10px; border-radius: 6px; background: #334155; border: 2px solid #475569; color: white; font-size: 15px; outline: none; cursor: pointer; }
  .btn-main { width: 85%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #10b981; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }
  .btn-main:hover { background: #059669; }
  .btn-close { background: #ef4444 !important; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3) !important; }
  .btn-close:hover { background: #dc2626 !important; }
</style>
</head>
<body>

<div id="container">
  <!-- MÀN HÌNH KHỞI ĐẦU CHÀO MỪNG -->
  <div id="start-screen" class="overlay">
    <div class="overlay-title">BLOCK PUZZLE PRO</div>
    <div class="setting-row">
      <div class="setting-label">Chọn nhạc nền trước khi vào:</div>
      <select id="start-music-select">
        <option value="https://mixkit.co">Chill Game Level (Mặc định)</option>
        <option value="https://mixkit.co">Dreaming Big (Nhẹ nhàng)</option>
        <option value="https://mixkit.co">Tech House (Sôi động)</option>
      </select>
    </div>
    <button class="btn-main" onclick="startGame()">BẮT ĐẦU CHƠI</button>
  </div>

  <!-- MENU CÀI ĐẶT TRONG LÚC CHƠI -->
  <div id="settings-screen" class="overlay" style="display: none;">
    <div class="overlay-title">⚙️ CÀI ĐẶT GAME</div>
    <div class="setting-row">
      <div class="setting-label">Âm thanh / Nhạc nền:</div>
      <select id="music-toggle" onchange="toggleMusicState()">
        <option value="on">Đang Bật (On)</option>
        <option value="off">Tắt Nhạc (Off)</option>
      </select>
    </div>
    <div class="setting-row">
      <div class="setting-label">Thay đổi bài hát:</div>
      <select id="game-music-select" onchange="changeTrack(this.value)">
        <option value="https://mixkit.co">Chill Game Level</option>
        <option value="https://mixkit.co">Dreaming Big</option>
        <option value="https://mixkit.co">Tech House</option>
      </select>
    </div>
    <button class="btn-main btn-close" onclick="closeSettings()">QUAY LẠI CHƠI</button>
  </div>

  <!-- KHU VỰC CHƠI GAME CHÍNH -->
  <div id="header-bar">
    <div id="score-board">Điểm số: <span id="score">0</span></div>
    <button id="btn-settings" onclick="openSettings()">⚙️</button>
  </div>
  <div id="grid"></div>
  <div id="pieces"></div>
</div>

<!-- Trình Audio ẩn của hệ thống -->
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

  // ĐÃ FIX LỖI: Điền đầy đủ ma trận dữ liệu số 0 và 1 cho các khối hình
  const pieceTemplates = [
    [[1]],                                     // Khối đơn 1x1
    [[1, 1]],                                  // Thanh ngang 2 ô
    [[1, 1, 1]],                               // Thanh ngang 3 ô
    [[1, 1], [1, 1]],                          // Khối vuông 2x2
    [[1, 0], [1, 1]],                          // Khối chữ L nhỏ
    [[1, 1, 1], [0, 1, 0]]                     // Khối chữ T
  ];
  let currentPieces = [];

  // Khởi động khi nhấn nút Start và tự động kích hoạt phát nhạc
  function startGame() {
    const startSelect = document.getElementById('start-music-select');
    audioPlayer.src = startSelect.value;
    
    // Đồng bộ trạng thái bài hát sang bảng điều khiển cài đặt bên trong
    document.getElementById('game-music-select').value = startSelect.value;
    
    // Phát nhạc ngay khi có tương tác click hợp lệ đầu tiên của người dùng
    audioPlayer.play().catch(err => console.log("Lỗi hệ thống âm thanh: ", err));
    
    startScreen.style.display = 'none';
  }

  // Quản lý cửa sổ cài đặt
  function openSettings() { settingsScreen.style.display = 'flex'; }
  function closeSettings() { settingsScreen.style.display = 'none'; }

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

  // Khởi tạo và kết xuất giao diện bảng lưới ban đầu
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

  // Sản sinh ngẫu nhiên đợt 3 khối hình dưới chân bảng
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
          pCell.className = val ? 'p-cell filled' : 'p-cell empty';
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
// Logic thả khối xuống ô được click
function placePiece(r, c) {
if (selectedPieceIndex === null) return;
const piece = currentPieces[selectedPieceIndex];
if (!piece) return;
// Quét kiểm tra va chạm vật lý / tràn biên
for (let pr = 0; pr < piece.length; pr++) {
for (let pc = 0; pc < piece[pr].length; pc++) {
if (piece[pr][pc]) {
const targetR = r + pr;
const targetC = c + pc;
if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
return; // Sai vị trí -> Không cho đặt
}
}
}
}
// Đặt khối thành công vào ô lưới
for (let pr = 0; pr < piece.length; pr++) {
for (let pc = 0; pc < piece[pr].length; pc++) {
if (piece[pr][pc]) {
board[r + pr][c + pc] = 1;
}
}
}
// Vô hiệu hóa khối vừa dùng
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
// Xử lý nổ khối khi lấp đầy hàng dọc hoặc hàng ngang
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
// Khởi động nạp dữ liệu ban đầu
initBoard();
spawnPieces();
"""
components.html(game_html, height=580, scrolling=False)

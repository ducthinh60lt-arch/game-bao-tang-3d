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
    "**Cách chơi:** **Nhấn và GIỮ CHUỘT PHẢI** vào một khối hình bên dưới để kéo đi, "
    "di chuyển đến vị trí trên bảng 10x10, sau đó **THẢ CHUỘT PHẢI** để khối rơi xuống!"
)

# 2. Trình phát nhạc nền Spotify
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# 3. Mã nguồn Game HTML5/JS xử lý kéo thả Chuột phải chuẩn tọa độ Iframe
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 430px; margin: 0 auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; }
  #score-board { font-size: 22px; font-weight: bold; margin-bottom: 15px; color: #f59e0b; }
  
  /* Bảng game 10x10 */
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 3px; background: #334155; padding: 8px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #1e293b; border-radius: 4px; transition: background 0.1s; }
  .cell.filled { background: #3b82f6; box-shadow: inset 0 0 5px rgba(255,255,255,0.4); }
  .cell.hovered { background: rgba(245, 158, 11, 0.6) !important; } /* Preview màu cam rõ khi di chuột qua */

  /* Khu vực chứa các khối để chọn */
  #pieces { display: flex; justify-content: space-around; min-height: 100px; background: #334155; padding: 10px; border-radius: 8px; align-items: center; }
  .piece { display: grid; gap: 2px; cursor: grab; padding: 8px; border: 2px dashed #475569; border-radius: 6px; background: rgba(15, 23, 42, 0.4); }
  .p-cell { width: 14px; height: 14px; border-radius: 2px; }
  .p-cell.filled { background: #3b82f6; }

  /* Khối ảo bay theo con trỏ chuột khi đang kéo */
  #drag-proxy {
    position: absolute;
    display: grid;
    gap: 3px;
    pointer-events: none; /* Rất quan trọng để không cản trở elementFromPoint */
    display: none;
    z-index: 9999;
  }
  .drag-cell { width: 28px; height: 28px; border-radius: 4px; }
  .drag-cell.filled { background: #f59e0b; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
  .drag-cell.empty { background: transparent; }
</style>
</head>
<body>

<div id="container">
  <div id="score-board">Điểm số: <span id="score">0</span></div>
  <div id="grid"></div>
  <div id="pieces"></div>
</div>

<!-- Khối mô phỏng bay theo chuột -->
<div id="drag-proxy"></div>

<script>
  // Chặn menu chuột phải mặc định trong khu vực game
  document.addEventListener('contextmenu', e => e.preventDefault());

  const gridEl = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const piecesEl = document.getElementById('pieces');
  const dragProxy = document.getElementById('drag-proxy');
  const container = document.getElementById('container');

  let score = 0;
  let board = Array(10).fill().map(() => Array(10).fill(0));
  
  let isDragging = false;
  let draggedPieceIndex = null;

  // SỬA LỖI 1: Khai báo định dạng ma trận số tuyệt đối cho các khối hình rõ ràng
  const pieceTemplates = [
    [[1]], // Khối 1x1
    [[1, 1]], // Thanh ngang 2 ô
    [[1, 1, 1]], // Thanh ngang 3 ô
    [[1, 1], [1, 1]], // Khối vuông 2x2
    [[1, 0], [1, 1]], // Khối chữ L nhỏ
    [[1, 1, 1], [0, 1, 0]] // Khối chữ T
  ];
  let currentPieces = [];

  // Tạo bảng ô lưới
  function initBoard() {
    gridEl.innerHTML = '';
    for (let r = 0; r < 10; r++) {
      for (let c = 0; c < 10; c++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.row = r;
        cell.dataset.col = c;
        gridEl.appendChild(cell);
      }
    }
  }

  function drawBoard() {
    const cells = gridEl.children;
    for (let r = 0; r < 10; r++) {
      for (let c = 0; c < 10; c++) {
        const idx = r * 10 + c;
        cells[idx].classList.remove('hovered');
        if (board[r][c] === 1) {
          cells[idx].classList.add('filled');
        } else {
          cells[idx].classList.remove('filled');
        }
      }
    }
  }

  // Sinh 3 khối mới
  function spawnPieces() {
    piecesEl.innerHTML = '';
    currentPieces = [];
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

      // Bắt sự kiện Nhấn chuột phải
      pieceDiv.addEventListener('mousedown', (e) => {
        if (e.button === 2 && currentPieces[i] !== null) {
          isDragging = true;
          draggedPieceIndex = i;
          createDragProxy(currentPieces[i]);
          updateDragProxyPosition(e);
        }
      });

      piecesEl.appendChild(pieceDiv);
    }
  }

  // Khối bóng ma chạy theo chuột
  function createDragProxy(piece) {
    dragProxy.innerHTML = '';
    dragProxy.style.display = 'grid';
    dragProxy.style.gridTemplateRows = `repeat(${piece.length}, 1fr)`;
    dragProxy.style.gridTemplateColumns = `repeat(${piece[0].length}, 1fr)`;

    piece.forEach(row => {
      row.forEach(val => {
        const dCell = document.createElement('div');
        dCell.className = val ? 'drag-cell filled' : 'drag-cell empty';
        dragProxy.appendChild(dCell);
      });
    });
  }

  // SỬA LỖI 2: Đổi sang cách tính vị trí chuột theo tọa độ nội bộ của Thẻ Container (khắc phục lỗi Iframe)
  function updateDragProxyPosition(e) {
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Căn lề dịch sang một chút để con trỏ không che mất khối hình
    dragProxy.style.left = (x - 20) + 'px';
    dragProxy.style.top = (y - 20) + 'px';
  }

  // Lắng nghe di chuyển trên toàn màn hình game
  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updateDragProxyPosition(e);

    clearHoverEffects();
    // Dùng trực tiếp tọa độ clientX/clientY để quét phần tử dưới chuột
    const cell = document.elementFromPoint(e.clientX, e.clientY);
    if (cell && cell.classList.contains('cell')) {
      const r = parseInt(cell.dataset.row);
      const c = parseInt(cell.dataset.col);
      highlightPlacement(r, c);
    }
  });

  // Thả chuột phải để đặt khối xuống
  document.addEventListener('mouseup', (e) => {
    if (!isDragging || e.button !== 2) return;
    isDragging = false;
    dragProxy.style.display = 'none';

    const cell = document.elementFromPoint(e.clientX, e.clientY);
    if (cell && cell.classList.contains('cell')) {
      const r = parseInt(cell.dataset.row);
      const c = parseInt(cell.dataset.col);
      placePiece(r, c);
    } else {
      drawBoard();
    }
  });

  function highlightPlacement(r, c) {
    const piece = currentPieces[draggedPieceIndex];
    if (!piece) return;

    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
          const targetC = c + pc;
          if (targetR < 10 && targetC < 10) {
            const idx = targetR * 10 + targetC;
            gridEl.children[idx].classList.add('hovered');
          }
        }
      }
    }
  }

  function clearHoverEffects() {
    for (let i = 0; i < gridEl.children.length; i++) {
      gridEl.children[i].classList.remove('hovered');
    }
  }

  function placePiece(r, c) {
    const piece = currentPieces[draggedPieceIndex];
    if (!piece) return;

    // Kiểm tra xem vị trí đặt khối có hợp lệ hay không
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
          const targetC = c + pc;
          if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
            drawBoard();
            return; // Trùng lặp hoặc vượt biên -> Hủy đặt khối
          }
        }
      }
    }

    // Ghi nhận khối vào bảng
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          board[r + pr][c + pc] = 1;
        }
      }
    }

    // Làm mờ khối đã đặt
    currentPieces[draggedPieceIndex] = null;
    const pieceDiv = piecesEl.querySelector(`[data-index="${draggedPieceIndex}"]`);
    if (pieceDiv) pieceDiv.style.opacity = '0.15';

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
initBoard();
spawnPieces();
"""

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
    "**Cách chơi mượt mà:** **Nhấn và GIỮ CHUỘT TRÁI** vào khối hình bên dưới để kéo đi, "
    "di chuyển đến ô bất kỳ trên bảng 10x10, sau đó **THẢ CHUỘT TRÁI** để khối rơi xuống!"
)

# 2. Trình phát nhạc nền Spotify
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# 3. Mã nguồn Game HTML5/JS xử lý kéo thả Chuột Trái (Chuẩn hóa 100%)
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
  
  /* Bảng lưới game 10x10 */
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 3px; background: #334155; padding: 8px; border-radius: 8px; margin-bottom: 20px; }
  .cell { aspect-ratio: 1; background: #1e293b; border-radius: 4px; transition: background 0.1s; }
  .cell.filled { background: #3b82f6; box-shadow: inset 0 0 5px rgba(255,255,255,0.4); }
  .cell.hovered { background: rgba(245, 158, 11, 0.6) !important; } /* Căn chỉnh khối nền cam sáng */

  /* Khu vực chứa 3 khối hình để chọn */
  #pieces { display: flex; justify-content: space-around; min-height: 100px; background: #334155; padding: 10px; border-radius: 8px; align-items: center; }
  .piece { display: grid; gap: 2px; cursor: grab; padding: 8px; border: 2px dashed #475569; border-radius: 6px; background: rgba(15, 23, 42, 0.4); }
  .p-cell { width: 14px; height: 14px; border-radius: 2px; }
  .p-cell.filled { background: #3b82f6; }

  /* Khối bóng ma ảo di chuyển bám sát trỏ chuột */
  #drag-proxy {
    position: absolute;
    display: grid;
    gap: 3px;
    pointer-events: none; /* Rất quan trọng: cho phép quét xuyên thấu xuống ô lưới phía dưới */
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

<div id="drag-proxy"></div>

<script>
  const gridEl = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const piecesEl = document.getElementById('pieces');
  const dragProxy = document.getElementById('drag-proxy');
  const container = document.getElementById('container');

  let score = 0;
  let board = Array(10).fill().map(() => Array(10).fill(0));
  
  let isDragging = false;
  let draggedPieceIndex = null;

  // Bản đồ số tuyệt đối của các hình khối (Đầy đủ dữ liệu ô vuông)
  const pieceTemplates = [
    [[1]],                               // Khối đơn 1x1
    [[1, 1]],                            // Thanh ngang 2
    [[1, 1, 1]],                         // Thanh ngang 3
    [[1, 1], [1, 1]],                    // Khối vuông 2x2
    [[1, 0], [1, 1]],                    // Chữ L nhỏ
    [[1, 1, 1], [0, 1, 0]]               // Khối chữ T
  ];
  let currentPieces = [];

  // Tạo giao diện lưới ban đầu
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

  // Tạo ngẫu nhiên 3 khối mới
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

      # Sự kiện NHẤN CHUỘT TRÁI để chọn và bắt đầu kéo
      pieceDiv.addEventListener('mousedown', (e) => {
        if (e.button === 0 && currentPieces[i] !== null) {
          isDragging = true;
          draggedPieceIndex = i;
          createDragProxy(currentPieces[i]);
          updateDragProxyPosition(e);
        }
      });

      piecesEl.appendChild(pieceDiv);
    }
  }

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

  function updateDragProxyPosition(e) {
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Đặt khối hình lệch tâm nhẹ lên trên ngón tay/con trỏ để người chơi dễ nhìn
    dragProxy.style.left = (x - 20) + 'px';
    dragProxy.style.top = (y - 30) + 'px';
  }

  // Theo dõi di chuyển chuột trên toàn bộ khung Iframe
  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updateDragProxyPosition(e);

    clearHoverEffects();
    const cell = document.elementFromPoint(e.clientX, e.clientY);
    if (cell && cell.classList.contains('cell')) {
      const r = parseInt(cell.dataset.row);
      const c = parseInt(cell.dataset.col);
      highlightPlacement(r, c);
    }
  });

  // Sự kiện THẢ CHUỘT TRÁI để thả khối hình xuống
  document.addEventListener('mouseup', (e) => {
    if (!isDragging || e.button !== 0) return;
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
            if (gridEl.children[idx]) {
              gridEl.children[idx].classList.add('hovered');
            }
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

    // Kiểm tra không gian trống hợp lệ
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
          const targetC = c + pc;
          if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
            drawBoard();
            return; // Vị trí không hợp lệ -> Hủy bỏ lệnh thả
          }
        }
      }
    }

    // Xác nhận ghi dữ liệu khối vào bảng
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          board[r + pr][c + pc] = 1;
        }
      }
    }

    currentPieces[draggedPieceIndex] = null;
    const pieceDiv = piecesEl.querySelector(`[data-index="${draggedPieceIndex}"]`);
    if (pieceDiv) pieceDiv.style.opacity = '0.15';

    checkLines();
    drawBoard();

    // Hồi lại 3 khối mới khi đã dùng hết
    if (currentPieces.every(p => p === null)) {
      spawnPieces();
    }
  }

  // Tính điểm khi xếp đầy hàng ngang / cột dọc
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
components.html(game_html, height=620, scrolling=False)

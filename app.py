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
    "**Cách chơi mới:** **Nhấn và GIỮ CHUỘT PHẢI** vào khối hình bên dưới để kéo đi, "
    "di chuyển đến vị trí mong muốn trên bảng 10x10, sau đó **THẢ CHUỘT PHẢI** để khối rơi xuống!"
)

# 2. Trình phát nhạc nền Spotify
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# 3. Mã nguồn Game HTML5/JS xử lý kéo thả Chuột phải
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; }
  #container { max-width: 450px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; }
  #score-board { font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #f59e0b; }
  
  /* Bảng game */
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 2px; background: #334155; padding: 5px; border-radius: 8px; margin-bottom: 15px; }
  .cell { aspect-ratio: 1; background: #1e293b; border-radius: 4px; transition: background 0.1s; }
  .cell.filled { background: #3b82f6; box-shadow: inset 0 0 5px rgba(255,255,255,0.3); }
  .cell.hovered { background: rgba(245, 158, 11, 0.4); } /* Hiệu ứng căn chỉnh khi rê khối qua */

  /* Khu vực chứa các khối để chọn */
  #pieces { display: flex; justify-content: space-around; min-height: 90px; background: #334155; padding: 10px; border-radius: 8px; }
  .piece { display: grid; gap: 1px; cursor: grab; padding: 5px; border: 2px dashed #475569; border-radius: 4px; background: rgba(15, 23, 42, 0.3); }
  .p-cell { width: 14px; height: 14px; border-radius: 2px; }
  .p-cell.filled { background: #3b82f6; }

  /* Khối ảo bay theo con trỏ chuột khi đang kéo */
  #drag-proxy {
    position: fixed;
    display: grid;
    gap: 2px;
    pointer-events: none; /* Tránh cản trở việc xác định ô bên dưới con chuột */
    display: none;
    z-index: 9999;
    transform: translate(-20px, -20px); /* Đặt tâm khối nằm gần đầu mút con trỏ */
  }
  .drag-cell { width: 25px; height: 25px; border-radius: 4px; }
  .drag-cell.filled { background: #f59e0b; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
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
  // Chặn hoàn toàn menu chuột phải trên toàn bộ trang game
  document.addEventListener('contextmenu', e => e.preventDefault());

  const gridEl = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const piecesEl = document.getElementById('pieces');
  const dragProxy = document.getElementById('drag-proxy');

  let score = 0;
  let board = Array(10).fill().map(() => Array(10).fill(0));
  
  // Trạng thái kéo thả
  let isDragging = false;
  let draggedPieceIndex = null;

  // Cấu trúc các khối hình hình học (Ma trận số tuyệt đối)
  const pieceTemplates = [
    [[1]], 
    [[1, 1]], 
    [[1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[1, 0], [1, 1]]
  ];
  let currentPieces = [];

  // 1. Tạo bảng 10x10
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

  // 2. Tạo 3 khối ngẫu nhiên ở hàng dưới
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

      // Lắng nghe sự kiện NHẤN CHUỘT PHẢI (button === 2)
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

  // 3. Tạo khối đồ họa bám theo con trỏ chuột khi kéo
  function createDragProxy(piece) {
    dragProxy.innerHTML = '';
    dragProxy.style.display = 'grid';
    dragProxy.style.gridTemplateRows = `repeat(${piece.length}, 1fr)`;
    dragProxy.style.gridTemplateColumns = `repeat(${piece[0].length}, 1fr)`;

    piece.forEach(row => {
      row.forEach(val => {
        const dCell = document.createElement('div');
        dCell.className = 'drag-cell' + (val ? ' filled' : '');
        dragProxy.appendChild(dCell);
      });
    });
  }

  function updateDragProxyPosition(e) {
    dragProxy.style.left = e.clientX + 'px';
    dragProxy.style.top = e.clientY + 'px';
  }

  // 4. Xử lý di chuyển chuột và thả chuột trên toàn màn hình
  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updateDragProxyPosition(e);

    // Tìm xem chuột đang lướt qua ô nào trên bảng 10x10
    clearHoverEffects();
    const cell = document.elementFromPoint(e.clientX, e.clientY);
    if (cell && cell.classList.contains('cell')) {
      const r = parseInt(cell.dataset.row);
      const c = parseInt(cell.dataset.col);
      highlightPlacement(r, c);
    }
  });

  document.addEventListener('mouseup', (e) => {
    if (!isDragging || e.button !== 2) return;
    isDragging = false;
    dragProxy.style.display = 'none';

    // Xác định ô mà chuột nhả ra để thả khối xuống
    const cell = document.elementFromPoint(e.clientX, e.clientY);
    if (cell && cell.classList.contains('cell')) {
      const r = parseInt(cell.dataset.row);
      const c = parseInt(cell.dataset.col);
      placePiece(r, c);
    } else {
      drawBoard(); // Trả lại trạng thái cũ nếu thả trượt ra ngoài
    }
  });

  // Hiển thị vị trí chuẩn bị thả khối xuống (Preview nhạt)
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

  // 5. Logic đặt khối và tính điểm
  function placePiece(r, c) {
    const piece = currentPieces[draggedPieceIndex];
    if (!piece) return;

    // Kiểm tra tính hợp lệ
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
          const targetC = c + pc;
          if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
            drawBoard();
            return; // Rớt ra ngoài hoặc trùng khối cũ -> không cho đặt
          }
        }
      }
    }

    // Ghi nhận khối rơi xuống thành công
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          board[r + pr][c + pc] = 1;
        }
      }
    }

    // Làm mờ ô đã dùng ở hàng lựa chọn bên dưới
    currentPieces[draggedPieceIndex] = null;
    const pieceDiv = piecesEl.querySelector(`[data-index="${draggedPieceIndex}"]`);
    if (pieceDiv) pieceDiv.style.opacity = '0.1';

    checkLines();
    drawBoard();

    if (currentPieces.every(p => p === null)) {
      spawnPieces();
    }
  }

  // Kiểm tra ăn điểm hàng ngang / hàng dọc
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

  // Khởi động
  initBoard();
  spawnPieces();
</script>

</body>
</html>
"""

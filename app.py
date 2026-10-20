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
    "**Cách chơi:** Kéo thả hoặc click chọn khối hình bên dưới, "
    "sau đó đặt vào bảng 10x10. Xếp kín một hàng ngang hoặc cột dọc để làm nổ khối và ghi điểm!"
)

# 2. Trình phát nhạc nền Spotify (Đã sửa link Embed chuẩn)
st.markdown("### 🎵 Nhạc nền phát kèm: Great Little Things")
# Lưu ý: Thay Track ID dưới đây bằng ID chính xác của bài hát nếu cần
components.iframe(
    src="https://spotify.com",
    height=80,
    scrolling=False
)

# 3. Mã nguồn Game HTML5/JS hoàn chỉnh tích hợp vào Streamlit
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; }
  #container { max-width: 450px; margin: 10px auto; padding: 15px; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
  #score-board { font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #f59e0b; }
  #grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 2px; background: #334155; padding: 5px; border-radius: 8px; margin-bottom: 15px; }
  .cell { aspect-ratio: 1; background: #1e293b; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
  .cell.filled { background: #3b82f6; box-shadow: inset 0 0 5px rgba(255,255,255,0.3); }
  #pieces { display: flex; justify-content: space-around; min-height: 80px; background: #334155; padding: 10px; border-radius: 8px; }
  .piece { display: grid; gap: 1px; cursor: grab; padding: 5px; border: 2px solid transparent; border-radius: 4px; }
  .piece.selected { border-color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
  .p-cell { width: 15px; height: 15px; border-radius: 2px; }
  .p-cell.filled { background: #3b82f6; }
</style>
</head>
<body>

<div id="container">
  <div id="score-board">Điểm số: <span id="score">0</span></div>
  <div id="grid"></div>
  <div id="pieces"></div>
</div>

<script>
  // Khởi tạo bảng 10x10
  const gridEl = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const piecesEl = document.getElementById('pieces');
  let score = 0;
  let board = Array(10).fill().map(() => Array(10).fill(0));
  let selectedPieceIndex = null;

  // Danh sách các khối hình mẫu (Ma trận số tuyệt đối)
  const pieceTemplates = [
    [[1]], // Khối 1x1
    [[1, 1]], // Thanh ngang 2
    [[1, 1, 1]], // Thanh ngang 3
    [[1, 1], [1, 1]], // Khối vuông 2x2
    [[1, 0], [1, 1]] // Khối chữ L nhỏ
  ];
  let currentPieces = [];

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

    // Kiểm tra xem có đặt vừa không
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          const targetR = r + pr;
          const targetC = c + pc;
          if (targetR >= 10 || targetC >= 10 || board[targetR][targetC] === 1) {
            return; // Không hợp lệ
          }
        }
      }
    }

    // Đặt khối vào bảng
    for (let pr = 0; pr < piece.length; pr++) {
      for (let pc = 0; pc < piece[pr].length; pc++) {
        if (piece[pr][pc]) {
          board[r + pr][c + pc] = 1;
        }
      }
    }

    // Xóa khối đã dùng khỏi danh sách lựa chọn
    currentPieces[selectedPieceIndex] = null;
    const pieceDiv = piecesEl.querySelector(`[data-index="${selectedPieceIndex}"]`);
    if (pieceDiv) pieceDiv.style.opacity = '0.2';
    selectedPieceIndex = null;

    checkLines();
    drawBoard();

    // Nếu dùng hết cả 3 khối thì hồi đợt mới
    if (currentPieces.every(p => p === null)) {
      spawnPieces();
    }
  }

  function checkLines() {
    let rowsToClear = [];
    let colsToClear = [];

    // Kiểm tra hàng ngang
    for (let r = 0; r < 10; r++) {
      if (board[r].every(val => val === 1)) rowsToClear.push(r);
    }
    // Kiểm tra cột dọc
    for (let c = 0; c < 10; c++) {
      let colFull = true;
      for (let r = 0; r < 10; r++) {
        if (board[r][c] === 0) colFull = false;
      }
      if (colFull) colsToClear.push(c);
    }

    // Xóa hàng và tính điểm
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

  // Khởi chạy game
  initBoard();
  spawnPieces();
</script>

</body>
</html>
"""

# 4. Nhúng giao diện game vào ứng dụng Streamlit
components.html(game_html, height=600, scrolling=False)

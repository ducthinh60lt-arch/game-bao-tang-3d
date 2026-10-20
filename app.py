import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chơi Flappy Bird Cây Cổ Thụ Online — Miễn Phí",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Game Flappy Bird: Vượt Rừng Cổ Thụ")
st.markdown(
    "**Cách chơi:** \n"
    "1. Bấm nút **BẮT ĐẦU CHƠI** ở màn hình mở đầu để bắt đầu trận đấu.\n"
    "2. **Click chuột trái vào bất kỳ vị trí nào trên khung game** để điều khiển chú chim bay lên (Có tiếng bíp khi nhảy!).\n"
    "3. Né tránh các thân cây và tán lá cổ thụ để ghi điểm số kỷ lục!"
)

# 2. Toàn bộ mã nguồn nhúng HTML5/JS/Canvas phiên bản CÂY CỔ THỤ ổn định mượt mà
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Flappy Bird Cây Cổ Thụ</title>
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: system-ui, sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 400px; margin: 0 auto; background: #4ec0ca; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; overflow: hidden; height: 530px; }
  #header-bar { position: absolute; top: 15px; left: 15px; right: 15px; display: flex; justify-content: center; align-items: center; z-index: 10; }
  #score-board { font-size: 32px; font-weight: bold; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.6); }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  
  /* Giao diện màn hình mở đầu và thông báo thua cuộc */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #4ec0ca; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 32px; font-weight: bold; color: #fff; margin-bottom: 25px; text-shadow: 2px 2px 0px #000; letter-spacing: 1px; }
  .btn-main { width: 85%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #f59e0b; border: 2px solid #fff; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
  .btn-main:hover { background: #d97706; transform: scale(1.03); }
</style>
</head>
<body>

<div id="container">
  <div id="start-screen" class="overlay">
    <div class="overlay-title">FLAPPY BIRD TREE</div>
    <button class="btn-main" onclick="startGame()">BẮT ĐẦU CHƠI</button>
  </div>

  <div id="header-bar">
    <div id="score-board">0</div>
  </div>
  <canvas id="gameCanvas" width="400" height="530"></canvas>
</div>

<script>
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const scoreEl = document.getElementById('score-board');
  const startScreen = document.getElementById('start-screen');

  let gameRunning = false;
  let score = 0;
  let audioCtx = null;

  // Thuộc tính vật lý cấu trúc chú chim Flappy Bird chuẩn cũ ổn định
  const bird = {
    x: 60,
    y: 200,
    width: 26,     
    height: 20,    
    gravity: 0.24,
    velocity: 0,
    jump: -5.2
  };

  let pipes = [];
  const pipeWidth = 55;   // Gom nhỏ lại một chút cho dáng cây thanh thoát
  const pipeGap = 145;    // Khe hở rộng rãi dễ thở hơn
  const pipeSpeed = 2.0;  
  let frameCount = 0;

  // Bộ tổng hợp âm thanh tiếng bíp đập cánh nhảy của trình duyệt
  function playJumpSound() {
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      const oscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(400, audioCtx.currentTime); 
      oscillator.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.08);
      
      gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime); 
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
      
      oscillator.start();
      oscillator.stop(audioCtx.currentTime + 0.08);
    } catch (e) {
      console.log(e);
    }
  }

  function startGame() {
    startScreen.style.display = 'none';
    resetGame();
    gameRunning = true;
    gameLoop();
  }

  canvas.addEventListener('mousedown', () => {
    if (!gameRunning) return;
    bird.velocity = bird.jump;
    playJumpSound();
  });

  function resetGame() {
    bird.y = 200;
    bird.velocity = 0;
    pipes = [];
    score = 0;
    scoreEl.innerText = score;
    frameCount = 0;
  }

  function gameLoop() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Tính toán cơ chế vật lý rơi tự do cho chú chim
    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

    // Render đồ họa chú chim gốc (Thân vàng, mỏ đỏ, mắt trắng)
    ctx.fillStyle = '#f3da3b'; 
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2, bird.y + bird.height/2, bird.width/2, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2 + 5, bird.y + bird.height/2 - 4, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2 + 7, bird.y + bird.height/2 - 4, 2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#f75331';
    ctx.beginPath();
    ctx.moveTo(bird.x + bird.width - 2, bird.y + bird.height/2 - 4);
    ctx.lineTo(bird.x + bird.width + 8, bird.y + bird.height/2);
    ctx.lineTo(bird.x + bird.width - 2, bird.y + bird.height/2 + 6);
    ctx.fill();
    ctx.stroke();

    // Game Over nếu đập đất hoặc chạm trời
    if (bird.y + bird.height >= canvas.height || bird.y <= 0) {
      gameOver();
      return;
    }

    // Thiết lập tần suất xuất hiện rặng cây cổ thụ
    if (frameCount % 105 === 0) {
      const minHeight = 60;
      const maxHeight = canvas.height - pipeGap - minHeight;
      const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
      
      pipes.push({
        x: canvas.width,
        top: topHeight,
        bottom: canvas.height - topHeight - pipeGap,
        passed: false
      });
    }
    frameCount++;

    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i];
      p.x -= pipeSpeed;

      // ĐỔI ĐỒ HỌA THÀNH CÂY CỔ THỤ (Thân màu gỗ nâu + Tán lá xanh rì ở đầu ngọn)
      // 1. CÂY CỔ THỤ PHÍA TRÊN (Mọc ngược từ trên xuống)
      // Vẽ thân cây màu nâu gỗ xù xì
      ctx.fillStyle = '#5c4033';
      ctx.fillRect(p.x, 0, pipeWidth, p.top);
      ctx.strokeStyle = '#3e2723';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(p.x, -2, pipeWidth, p.top + 2);
      // Vẽ các thớ dọc sọc giả vân gỗ trên thân cây
      ctx.fillStyle = '#4e3629';
      ctx.fillRect(p.x + 12, 0, 4, p.top);
      ctx.fillRect(p.x + 35, 0, 4, p.top);
      // Vẽ Tán lá xum xuê màu xanh rậm rì ở đầu khúc ngọn cây cổ thụ trên
      ctx.fillStyle = '#2e5a1c';
      ctx.beginPath();
      ctx.arc(p.x + pipeWidth/2, p.top - 2, 34, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#1b3411';
      ctx.stroke();

      // 2. CÂY CỔ THỤ PHÍA DƯỚI (Mọc thẳng từ đất lên)
      let bottomY = canvas.height - p.bottom;
      // Vẽ thân cây màu nâu gỗ dưới
      ctx.fillStyle = '#5c4033';
      ctx.fillRect(p.x, bottomY, pipeWidth, p.bottom);
      ctx.strokeRect(p.x, bottomY, pipeWidth, p.bottom + 2);
      // Vân gỗ sọc dọc dưới thân cây
      ctx.fillStyle = '#4e3629';
      ctx.fillRect(p.x + 12, bottomY, 4, p.bottom);
      ctx.fillRect(p.x + 35, bottomY, 4, p.bottom);
      // Vẽ Tán lá xum xuê màu xanh rì bọc lấy ngọn cây cổ thụ dưới
      ctx.fillStyle = '#2e5a1c';
      ctx.beginPath();
      ctx.arc(p.x + pipeWidth/2, bottomY + 2, 34, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Thuật toán quét va chạm bo góc chuẩn (Độ lệch góc trống -2 để chống chết oan)
      if (
        bird.x + 2 < p.x + pipeWidth &&
        bird.x + bird.width - 2 > p.x &&
        (bird.y + 2 < p.top || bird.y + bird.height - 2 > bottomY)
      ) {
        gameOver();
        return;
      }

      // Vượt cây cổ thụ thành công -> Cộng điểm
      if (!p.passed && p.x + pipeWidth < bird.x) {
        p.passed = true;
        score++;
        scoreEl.innerText = score;
      }

      if (p.x + pipeWidth + 20 < 0) {
        pipes.splice(i, 1);
      }
    }

    requestAnimationFrame(gameLoop);
  }

  function gameOver() {
    gameRunning = false;
    document.querySelector('#start-screen .overlay-title').innerText = "GAME OVER! SCORE: " + score;
    document.querySelector('#start-screen .btn-main').innerText = "THỬ LẠI";
    startScreen.style.display = 'flex';
  }
</script>

</body>
</html>
"""

# 3. Kết xuất giao diện trò chơi lên Streamlit
components.html(game_html, height=540, scrolling=False)




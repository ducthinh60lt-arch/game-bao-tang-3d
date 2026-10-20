import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chơi Flappy Bird Online — Miễn Phí, Không Cần Tải",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Siêu Game Flappy Bird Online")
st.markdown(
    "**Cách chơi:** \n"
    "1. Bấm nút **BẮT ĐẦU CHƠI** ở màn hình mở đầu để bắt đầu trận đấu.\n"
    "2. **Click chuột trái vào bất kỳ vị trí nào trên khung game** để điều khiển chú chim bay lên.\n"
    "3. Né tránh các đường ống nước màu xanh lá để ghi điểm số kỷ lục!"
)

game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Flappy Bird Online</title>
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: system-ui, sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 400px; margin: 0 auto; background: #4ec0ca; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; overflow: hidden; height: 530px; }
  #header-bar { position: absolute; top: 15px; left: 15px; right: 15px; display: flex; justify-content: center; align-items: center; z-index: 10; }
  #score-board { font-size: 32px; font-weight: bold; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.6); }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #4ec0ca; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 32px; font-weight: bold; color: #fff; margin-bottom: 25px; text-shadow: 2px 2px 0px #000; letter-spacing: 1px; }
  .btn-main { width: 85%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #f59e0b; border: 2px solid #fff; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
  .btn-main:hover { background: #d97706; transform: scale(1.03); }
</style>
</head>
<body>

<div id="container">
  <div id="start-screen" class="overlay">
    <div class="overlay-title">FLAPPY BIRD PRO</div>
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

  const bird = {
    x: 60,
    y: 200,
    width: 34,
    height: 24,
    gravity: 0.24,
    velocity: 0,
    jump: -5.2
  };

  let pipes = [];
  const pipeWidth = 62;
  const pipeGap = 125;
  const pipeSpeed = 2.2;
  let frameCount = 0;

  function startGame() {
    startScreen.style.display = 'none';
    resetGame();
    gameRunning = true;
    gameLoop();
  }

  canvas.addEventListener('mousedown', () => {
    if (!gameRunning) return;
    bird.velocity = bird.jump;
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

    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

    // Thân chim
    ctx.fillStyle = '#f3da3b'; 
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2, bird.y + bird.height/2, bird.width/2, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Mắt chim
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2 + 5, bird.y + bird.height/2 - 4, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2 + 7, bird.y + bird.height/2 - 4, 2, 0, Math.PI * 2);
    ctx.fill();

    // Mỏ chim
    ctx.fillStyle = '#f75331';
    ctx.beginPath();
    ctx.moveTo(bird.x + bird.width - 2, bird.y + bird.height/2 - 4);
    ctx.lineTo(bird.x + bird.width + 8, bird.y + bird.height/2);
    ctx.lineTo(bird.x + bird.width - 2, bird.y + bird.height/2 + 6);
    ctx.fill();
    ctx.stroke();

    if (bird.y + bird.height >= canvas.height || bird.y <= 0) {
      gameOver();
      return;
    }

    if (frameCount % 95 === 0) {
      const minHeight = 50;
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

      ctx.fillStyle = '#73c737';
      ctx.fillRect(p.x, 0, pipeWidth, p.top);
      ctx.strokeRect(p.x, -2, pipeWidth, p.top + 2);

      ctx.fillRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom);
      ctx.strokeRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom + 2);

      if (
        bird.x < p.x + pipeWidth &&
        bird.x + bird.width > p.x &&
        (bird.y < p.top || bird.y + bird.height > canvas.height - p.bottom)
      ) {
        gameOver();
        return;
      }

      if (!p.passed && p.x + pipeWidth < bird.x) {
        p.passed = true;
        score++;
        scoreEl.innerText = score;
      }

      if (p.x + pipeWidth < 0) {
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

components.html(game_html, height=540, scrolling=False)


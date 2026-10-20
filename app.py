import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chơi Flappy Bird Cây Cổ Thụ Online — Miễn Phí",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Flappy Bird: Đại Ngàn Kỳ Vĩ")
st.markdown(
    "**Cách chơi:** \n"
    "1. Bấm nút **BẮT ĐẦU CHƠI** để nhập cuộc.\n"
    "2. **Click chuột trái vào bất kỳ vị trí nào trên khung game** để điều khiển chú chim bay lên (Có tiếng bíp khi nhảy).\n"
    "3. Bản này đã **loại bỏ hoàn toàn dải đất/cỏ phía dưới**, giúp không gian bay rộng mở thênh thang!"
)

# 2. Toàn bộ mã nguồn nhúng HTML5/JS/Canvas (Đã xóa thảm cỏ và nền đất ở đáy)
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Flappy Bird Đại Ngàn</title>
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: system-ui, sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 400px; margin: 0 auto; background: #1e293b; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); position: relative; overflow: hidden; height: 530px; }
  #header-bar { position: absolute; top: 15px; left: 15px; right: 15px; display: flex; justify-content: center; align-items: center; z-index: 10; }
  #score-board { font-size: 38px; font-weight: 900; color: #fff; text-shadow: 2px 2px 8px rgba(0,0,0,0.8), -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000; font-family: 'Arial Black', sans-serif; }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  
  /* Giao diện màn hình mở đầu mượt mà */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #4ec0ca, #2f9ea8); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 34px; font-weight: 900; color: #fff; margin-bottom: 25px; text-shadow: 3px 3px 0px #1e3a3d; letter-spacing: 2px; font-family: 'Arial Black', sans-serif; }
  .btn-main { width: 85%; padding: 14px; font-size: 18px; font-weight: bold; color: white; background: linear-gradient(to bottom, #f59e0b, #d97706); border: 2px solid #fff; border-radius: 12px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }
  .btn-main:hover { transform: scale(1.04); box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
</style>
</head>
<body>

<div id="container">
  <div id="start-screen" class="overlay">
    <div class="overlay-title">FLAPPY TREE HD</div>
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

  // Cấu hình vật lý bản dễ chơi lơ lửng
  const bird = {
    x: 70,
    y: 200,
    width: 28,     
    height: 22,    
    gravity: 0.15,  
    velocity: 0,
    jump: -3.7      
  };

  let pipes = [];
  const pipeWidth = 58;   
  const pipeGap = 175;    
  const pipeSpeed = 1.4;  
  let frameCount = 0;

  // ĐÃ ĐỔI: Đặt chiều cao mặt đất về bằng 0 để chim tận dụng hết đáy màn hình
  const groundHeight = 0; 

  // Hiệu ứng âm thanh bíp khi nhảy
  function playJumpSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();
      oscillator.connect(gainNode); gainNode.connect(audioCtx.destination);
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(420, audioCtx.currentTime); 
      oscillator.frequency.exponentialRampToValueAtTime(850, audioCtx.currentTime + 0.08);
      gainNode.gain.setValueAtTime(0.12, audioCtx.currentTime); 
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
      oscillator.start(); oscillator.stop(audioCtx.currentTime + 0.08);
    } catch (e) {}
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

  // HÀM VẼ TOÀN BỘ BỐI CẢNH ĐỒ HỌA HD VECTOR LUNG LINH
  function drawBeautifulScene() {
    let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    skyGrad.addColorStop(0, '#3ba8b3');
    skyGrad.addColorStop(0.4, '#4ec0ca');
    skyGrad.addColorStop(0.7, '#a9e3e8');
    skyGrad.addColorStop(1, '#fff6d1'); 
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
    drawCloud(80, 100, 25); drawCloud(260, 70, 30);

    ctx.fillStyle = '#3ca3ad';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    ctx.quadraticCurveTo(80, canvas.height - 50, 180, canvas.height - 15);
    ctx.quadraticCurveTo(290, canvas.height - 60, canvas.width, canvas.height);
    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.fill();
  }

  function drawCloud(x, y, r) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.arc(x + r * 0.6, y - r * 0.3, r * 0.8, 0, Math.PI * 2);
    ctx.arc(x + r * 1.2, y, r * 0.6, 0, Math.PI * 2);
    ctx.fill();
  }

  // HÀM VẼ CÂY CỔ THỤ ĐA TẦNG ĐỔ BÓNG 3D
  function drawPremiumTree(px, py, pw, ph, isTop) {
    ctx.save();
    let trunkGrad = ctx.createLinearGradient(px, 0, px + pw, 0);
    trunkGrad.addColorStop(0, '#4a3329'); 
    trunkGrad.addColorStop(0.2, '#6d4c41');
    trunkGrad.addColorStop(0.5, '#8d6e63'); 
    trunkGrad.addColorStop(0.8, '#5d4037');
    trunkGrad.addColorStop(1, '#3e2723'); 

    ctx.fillStyle = trunkGrad;
    ctx.fillRect(px, py, pw, ph);

    ctx.fillStyle = 'rgba(40, 20, 10, 0.15)';
    ctx.fillRect(px + pw * 0.25, py, 3, ph);
    ctx.fillRect(px + pw * 0.65, py, 2, ph);

    let leafY = isTop ? py + ph : py;
    
    ctx.fillStyle = '#1b4314'; 
    ctx.beginPath(); ctx.arc(px + pw/2, leafY, 36, 0, Math.PI * 2); ctx.fill();

    let leafGrad = ctx.createRadialGradient(px + pw/2, leafY - 5, 5, px + pw/2, leafY, 32);
    leafGrad.addColorStop(0, '#4caf50'); 
    leafGrad.addColorStop(0.7, '#2e7d32');
    leafGrad.addColorStop(1, '#1b5e20'); 
    ctx.fillStyle = leafGrad;
    ctx.beginPath(); ctx.arc(px + pw/2, leafY, 32, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = '#81c784';
    ctx.beginPath();
    ctx.arc(px + pw/2 - 8, leafY - 12, 14, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function gameLoop() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBeautifulScene();

    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

    // GAME OVER nếu chạm đáy hoặc trần nhà canvas
    if (bird.y + bird.height >= canvas.height || bird.y <= 0) {
      gameOver();
      return;
    }

    if (frameCount % 135 === 0) {
      const minHeight = 60;
      const maxHeight = canvas.height - pipeGap - minHeight;
      const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
      
      pipes.push({ x: canvas.width, top: topHeight, bottom: canvas.height - topHeight - pipeGap, passed: false });
    }
    frameCount++;

    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i];
      p.x -= pipeSpeed;

      drawPremiumTree(p.x, 0, pipeWidth, p.top, true);

      let bottomY = canvas.height - p.bottom;
      drawPremiumTree(p.x, bottomY, pipeWidth, p.bottom, false);

      if (
        bird.x + 3 < p.x + pipeWidth &&
        bird.x + bird.width - 3 > p.x &&
        (bird.y + 3 < p.top || bird.y + bird.height - 3 > bottomY)
      ) {
        gameOver();
        return;
      }

      if (!p.passed && p.x + pipeWidth < bird.x) {
        p.passed = true;
        score++;
        scoreEl.innerText = score;
      }

      if (p.x + pipeWidth + 40 < 0) pipes.splice(i, 1);
    }

    // VẼ CHÚ CHIM FLAPPY BIRD CHUẨN VECTOR
    ctx.save();
    let angle = bird.velocity * 0.08;
    ctx.translate(bird.x + bird.width/2, bird.y + bird.height/2);
    ctx.rotate(Math.max(-0.2, Math.min(0.5, angle)));

    let birdGrad = ctx.createRadialGradient(-2, -2, 2, 0, 0, bird.width/2);
    birdGrad.addColorStop(0, '#fff176'); 
    birdGrad.addColorStop(0.5, '#fdd835');
    birdGrad.addColorStop(1, '#f4511e'); 
    ctx.fillStyle = birdGrad;
    ctx.beginPath(); ctx.arc(0, 0, bird.width/2, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#212121'; ctx.lineWidth = 1.5; ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.arc(5, -4, 5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#000';
    ctx.beginPath(); ctx.arc(6, -4, 2, 0, Math.PI * 2); ctx.fill(); 
    ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.arc(5, -5, 0.8, 0, Math.PI * 2); ctx.fill(); 

    let beakGrad = ctx.createLinearGradient(6, 0, 16, 0);
    beakGrad.addColorStop(0, '#ff7043'); beakGrad.addColorStop(1, '#d84315');
    ctx.fillStyle = beakGrad;
    ctx.beginPath(); ctx.moveTo(7, -2); ctx.lineTo(16, 1); ctx.lineTo(5, 5); ctx.closePath(); ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#fff9c4';
    ctx.beginPath(); ctx.ellipse(-6, 2, 6, 4, Math.PI/4, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

    ctx.restore();

requestAnimationFrame(gameLoop);
}
function gameOver() {
gameRunning = false;
document.querySelector('#start-screen .overlay-title').innerText = "SCORE KỶ LỤC: " + score;
document.querySelector('#start-screen .btn-main').innerText = "THỬ LẠI NGAY";
startScreen.style.display = 'flex';

components.html(game_html, height=540, scrolling=False)

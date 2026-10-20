import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Flappy Bird: Đại Ngàn Kỳ Vĩ",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Flappy Bird: Thung Lũng Đại Ngàn")
st.markdown(
    "**Cách chơi:** \n"
    "1. Bấm nút **BẮT ĐẦU CHƠI** ở màn hình mở đầu để bắt đầu trận đấu.\n"
    "2. **Click chuột trái vào bất kỳ vị trí nào trên khung game** để điều khiển chú chim bay lên (Có tiếng bíp khi nhảy).\n"
    "3. Né tránh các thân cây cổ thụ để ghi điểm số kỷ lục!"
)

# 2. Toàn bộ mã nguồn nhúng HTML5/JS/Canvas tích hợp trọn gói đã SỬA LỖI VẼ
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
  #score-board { font-size: 38px; font-weight: 900; color: #fff; text-shadow: 2px 2px 8px rgba(0,0,0,0.8), -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, -1px 1px 0 #000; font-family: 'Arial Black', sans-serif; }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  
  /* Giao diện màn hình mở đầu mượt mà */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #2e5a1c, #4ec0ca); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 34px; font-weight: 900; color: #fff; margin-bottom: 25px; text-shadow: 3px 3px 0px #1b3411; letter-spacing: 2px; font-family: 'Arial Black', sans-serif; }
  .btn-main { width: 85%; padding: 14px; font-size: 18px; font-weight: bold; color: white; background: linear-gradient(to bottom, #f59e0b, #d97706); border: 2px solid #fff; border-radius: 12px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }
  .btn-main:hover { transform: scale(1.04); box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
</style>
</head>
<body>

<div id="container">
  <div id="start-screen" class="overlay">
    <div class="overlay-title">FLAPPY FOREST</div>
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

  // Cấu hình vật lý chim lơ lửng, rơi chậm bản dễ kiểm soát
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

  // Hiệu ứng âm thanh khi nhảy của trình duyệt
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

  // HÀM VẼ PHÔNG NỀN RỪNG XANH ĐA TẦNG & MÂY HD
  function drawBeautifulForestScene() {
    // 1. Gradient bầu trời từ xanh ngọc xuống vàng nắng ấm
    let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    skyGrad.addColorStop(0, '#2b8a94');
    skyGrad.addColorStop(0.4, '#4ec0ca');
    skyGrad.addColorStop(0.7, '#a2e0e6');
    skyGrad.addColorStop(1, '#fffcd1'); 
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Vẽ các cụm mây HD bồng bềnh đổ bóng mịn
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    drawCloud(70, 90, 22); drawCloud(280, 60, 28);

    // 3. TẦNG RỪNG XA (Màu xanh lam nhạt mờ ảo phía đường chân trời)
    ctx.fillStyle = '#489da6';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    ctx.quadraticCurveTo(60, canvas.height - 130, 150, canvas.height - 90);
    ctx.quadraticCurveTo(250, canvas.height - 140, canvas.width, canvas.height - 80);
    ctx.lineTo(canvas.width, canvas.height);
    ctx.closePath();
    ctx.fill();
    
    ctx.fillStyle = '#3f919a';
    for (let i = 0; i < canvas.width; i += 25) {
      ctx.beginPath(); ctx.arc(i, canvas.height - 85, 12, 0, Math.PI, true); ctx.fill();
    }

    // 4. TẦNG RỪNG GẦN (Màu xanh lục đậm hơn, tạo chiều sâu thung lũng rộng mở)
    ctx.fillStyle = '#337146';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    ctx.quadraticCurveTo(90, canvas.height - 80, 200, canvas.height - 50);
    ctx.quadraticCurveTo(310, canvas.height - 90, canvas.width, canvas.height - 40);
    ctx.lineTo(canvas.width, canvas.height);
    ctx.closePath();
    ctx.fill();
    
    ctx.fillStyle = '#2b633c';
    let offset = (frameCount * 0.3) % 20;
    for (let i = -20; i < canvas.width + 20; i += 20) {
      ctx.beginPath(); ctx.arc(i - offset, canvas.height - 45, 14, 0, Math.PI, true); ctx.fill();
    }
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
    
    // Vẽ phông nền cảnh rừng đại ngàn kì vĩ trước
    drawBeautifulForestScene();

    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

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

    // VẼ CHÚ CHIM FLAPPY BIRD CHUẨN VECTOR SẮC NÉT (ĐÃ FIX LỖI HÀM VẼ CÁNH CHIM)
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
// SỬA LỖI TẠI ĐÂY: Dùng hàm vẽ hình tròn truyền thống cực kỳ an toàn cho cánh chim
ctx.fillStyle = '#fff9c4';
ctx.beginPath();
ctx.arc(-6, 2, 5, 0, Math.PI * 2);
ctx.fill();
ctx.stroke();
ctx.restore();
requestAnimationFrame(gameLoop);
}
function gameOver() {
gameRunning = false;
document.querySelector('#start-screen .overlay-title').innerText = "SCORE KỶ LỤC: " + score;
document.querySelector('#start-screen .btn-main').innerText = "THỬ LẠI NGAY";
startScreen.style.display = 'flex';
}
"""
components.html(game_html, height=540, scrolling=False)

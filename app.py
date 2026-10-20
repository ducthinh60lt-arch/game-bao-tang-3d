import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Chơi Flappy Bird Online — Miễn Phí, Không Cần Tải",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Siêu Game Flappy Bird Đồ Họa Đẹp")
st.markdown(
    "**Cập nhật mới:** \n"
    "1. **Sửa lỗi va chạm:** Sửa góc khuất vô hình, chim bo sát ranh giới ống nước không còn chết oan nữa.\n"
    "2. **Nâng cấp đồ họa:** Thêm hình nền thành phố, mây trời và hiệu ứng chim xoay đầu cực mượt!"
)

# 2. Mã nguồn ứng dụng Game Flappy Bird nâng cấp đồ họa Pixel Art và thuật toán va chạm tròn
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
  #score-board { font-size: 36px; font-weight: bold; color: #fff; text-shadow: 2px 2px 0px #000; font-family: monospace; }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  
  /* Giao diện màn hình mở đầu */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #4ec0ca; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 34px; font-weight: bold; color: #fff; margin-bottom: 25px; text-shadow: 3px 3px 0px #000; letter-spacing: 1px; font-family: monospace; }
  .btn-main { width: 85%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #f59e0b; border: 3px solid #fff; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
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
  let audioCtx = null;

  // Cấu trúc vật lý của chú chim
  const bird = {
    x: 70,
    y: 200,
    radius: 12,    // Dùng bán kính quét vòng tròn để sửa lỗi chết oan
    gravity: 0.20, // Chỉnh nhẹ để bay lượn mượt mà hơn
    velocity: 0,
    jump: -4.6,
    angle: 0       // Góc xoay đầu của chú chim
  };

  let pipes = [];
  const pipeWidth = 65;
  const pipeGap = 150;   // Khoảng trống rộng rãi dễ chơi
  const pipeSpeed = 1.8; // Tốc độ ống trượt chậm rãi vừa phải
  let frameCount = 0;

  // Hiệu ứng âm thanh cánh đập bíp bíp
  function playJumpSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(450, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(750, audioCtx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
      osc.start(); osc.stop(audioCtx.currentTime + 0.08);
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
    bird.angle = 0;
    pipes = [];
    score = 0;
    scoreEl.innerText = score;
    frameCount = 0;
  }

  // HÀM VẼ NỀN THÀNH PHỐ PIXEL ART ĐẸP MẮT
  function drawBeautifulBackground() {
    // 1. Màu trời Gradient mượt
    ctx.fillStyle = '#4ec0ca';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Vẽ dãy tòa nhà chung cư mờ phía xa (Thành phố ban ngày)
    ctx.fillStyle = '#48b0ba';
    ctx.fillRect(0, canvas.height - 140, canvas.width, 60);
    ctx.fillStyle = '#3da3ad';
    // Tạo hình răng cưa giả lập các khối nhà cao tầng
    for (let i = 0; i < canvas.width; i += 30) {
      let h = (i % 20 === 0) ? 70 : 50;
      ctx.fillRect(i, canvas.height - h - 80, 22, h);
    }

    // 3. Vẽ dải cây xanh / công viên cây cỏ rậm rạp
    ctx.fillStyle = '#73bf2e';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 20);
    ctx.fillStyle = '#9ece37';
    for (let i = 0; i < canvas.width; i += 15) {
      ctx.beginPath();
      ctx.arc(i, canvas.height - 80, 10, 0, Math.PI * 2);
      ctx.fill();
    }

    // 4. Mặt đất phẳng chuyển động
    ctx.fillStyle = '#ded895';
    ctx.fillRect(0, canvas.height - 70, canvas.width, 70);
    ctx.fillStyle = '#dfd385';
    ctx.fillRect(0, canvas.height - 70, canvas.width, 6);
  }

  function gameLoop() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Vẽ nền cảnh quan trước
    drawBeautifulBackground();

    // Tính toán góc nghiêng đầu của chim dựa theo vận tốc rơi
    bird.velocity += bird.gravity;
    bird.y += bird.velocity;
    
    if (bird.velocity < 0) {
      bird.angle = -0.3; // Ngẩng đầu lên khi vỗ cánh bay
    } else if (bird.velocity > 2) {
      bird.angle = Math.min(0.8, bird.angle + 0.05); // Chúc đầu xuống khi rơi tự do
    }

    // VẼ CHÚ CHIM FLAPPY BIRD CHUẨN ĐỒ HỌA
    ctx.save();
    ctx.translate(bird.x, bird.y);
    ctx.rotate(bird.angle);

    // Thân chim hình tròn vàng có viền đen sắc nét
    ctx.fillStyle = '#f8d018';
    ctx.beginPath();
    ctx.arc(0, 0, bird.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Vẽ cánh chim màu trắng ở thân
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.ellipse(-6, 2, 6, 4, Math.PI/6, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Mắt tròn to viền đen
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(5, -4, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    // Con ngươi mắt
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(6, -4, 1.8, 0, Math.PI * 2);
    ctx.fill();

    // Mỏ cam dày nhô về phía trước
    ctx.fillStyle = '#f85818';
    ctx.beginPath();
    ctx.moveTo(8, -2);
    ctx.lineTo(16, 2);
    ctx.lineTo(6, 6);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.restore();

    // Thua cuộc nếu đập đất hoặc vượt trần
    if (bird.y + bird.radius >= canvas.height - 70 || bird.y - bird.radius <= 0) {
      gameOver();
      return;
    }

    // Xử lý tạo lập các Ống Nước 3D tinh tế
    if (frameCount % 110 === 0) {
      const minHeight = 60;
      const maxHeight = (canvas.height - 70) - pipeGap - minHeight;
      const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
      
      pipes.push({
        x: canvas.width,
        top: topHeight,
        bottom: (canvas.height - 70) - topHeight - pipeGap,
        passed: false
      });
    }
    frameCount++;

    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i];
      p.x -= pipeSpeed;

      // ĐỔ MÀU ỐNG NƯỚC PIXEL 3D (Xanh lục đậm nhạt kết hợp đổ bóng dọc thân)
      // Ống phía trên
      let gradTop = ctx.createLinearGradient(p.x, 0, p.x + pipeWidth, 0);
      gradTop.addColorStop(0, '#53a018');
      gradTop.addColorStop(0.3, '#73c737');
      gradTop.addColorStop(0.8, '#a3e757');
      gradTop.addColorStop(1, '#438010');
      
      ctx.fillStyle = gradTop;
      ctx.fillRect(p.x, 0, pipeWidth, p.top);
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 2.5;
      ctx.strokeRect(p.x, -2, pipeWidth, p.top + 2);
      // Gờ vành miệng ống trên
      ctx.fillRect(p.x - 3, p.top - 20, pipeWidth + 6, 20);
      ctx.strokeRect(p.x - 3, p.top - 20, pipeWidth + 6, 20);

      // Ống phía dưới
      let bottomY = (canvas.height - 70) - p.bottom;
      let gradBot = ctx.createLinearGradient(p.x, bottomY, p.x + pipeWidth, bottomY);
      gradBot.addColorStop(0, '#53a018');
      gradBot.addColorStop(0.3, '#73c737');
      gradBot.addColorStop(0.8, '#a3e757');
      gradBot.addColorStop(1, '#438010');

      ctx.fillStyle = gradBot;
      ctx.fillRect(p.x, bottomY, pipeWidth, p.bottom);
      ctx.strokeRect(p.x, bottomY, pipeWidth, p.bottom + 2);
      // Gờ vành miệng ống dưới
      ctx.fillRect(p.x - 3, bottomY, pipeWidth + 6, 20);
      ctx.strokeRect(p.x - 3, bottomY, pipeWidth + 6, 20);

      // SỬA LỖI VA CHẠM: Tính toán va chạm giữa tâm hình tròn (Chim) và hình chữ nhật (Ống)
      if (checkCircleRectCollision(bird.x, bird.y, bird.radius, p.x, 0, pipeWidth, p.top) ||
          checkCircleRectCollision(bird.x, bird.y, bird.radius, p.x - 3, p.top - 20, pipeWidth + 6, 20) ||
           SherwoodCollision(bird.x, bird.y, bird.radius, p.x, bottomY, pipeWidth, p.bottom) ||
          checkCircleRectCollision(bird.x, bird.y, bird.radius, p.x - 3, bottomY, pipeWidth + 6, 20)) {
        gameOver();
        return;
      }

      // Vượt ống ghi điểm mượt
components.html(game_html, height=540, scrolling=False)


import streamlit as st
import streamlit.components.v1 as components

# CẤU HÌNH TRANG STREAMLIT NỀN TẢNG
st.set_page_config(
    page_title="Flappy Bird: Đại Ngàn Kỳ Vĩ",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Flappy Bird: Thung Lũng Đại Ngàn")
st.markdown(
    "**Cách chơi:** Click chuột trái vào khung game để giúp chim vỗ cánh đập liên tục và bay lên!"
)

# KHỐI CODE TRÒ CHƠI HOÀN CHỈNH ĐÃ TÍCH HỢP HIỆU ỨNG VÕ CÁNH VÀ LÀM RÕ MỎ CHIM
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: #0f172a; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 400px; margin: 0 auto; background: #1e293b; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); position: relative; overflow: hidden; height: 530px; }
  #score-board { position: absolute; top: 15px; left: 0; right: 0; font-size: 38px; font-weight: 900; color: #fff; text-shadow: 2px 2px 8px #000; font-family: sans-serif; z-index: 10; pointer-events: none; }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  .overlay { position: absolute; inset: 0; background: linear-gradient(135deg, #2e5a1c, #4ec0ca); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: sans-serif; }
  .overlay-title { font-size: 34px; font-weight: 900; color: #fff; margin-bottom: 25px; text-shadow: 3px 3px 0px #1b3411; }
  .btn-main { width: 80%; padding: 14px; font-size: 18px; font-weight: bold; color: white; background: linear-gradient(to bottom, #f59e0b, #d97706); border: 2px solid #fff; border-radius: 12px; cursor: pointer; }
</style>
</head>
<body>

<div id="container">
  <div id="start-screen" class="overlay">
    <div class="overlay-title">FLAPPY FOREST</div>
    <button class="btn-main" onclick="startGame()">BẮT ĐẦU CHƠI</button>
  </div>
  <div id="score-board">0</div>
  <canvas id="gameCanvas" width="400" height="530"></canvas>
</div>

<script>
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const scoreEl = document.getElementById('score-board');
  const startScreen = document.getElementById('start-screen');

  let gameRunning = false, score = 0, audioCtx = null, frameCount = 0, pipes = [];
  const bird = { x: 70, y: 200, width: 30, height: 24, gravity: 0.15, velocity: 0, jump: -3.7 };
  const pipeWidth = 58, pipeGap = 175, pipeSpeed = 1.4;

  function playJumpSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.type = 'sine'; osc.frequency.setValueAtTime(420, audioCtx.currentTime); 
      osc.frequency.exponentialRampToValueAtTime(850, audioCtx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.12, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
      osc.start(); osc.stop(audioCtx.currentTime + 0.08);
    } catch (e) {}
  }

  function startGame() { startScreen.style.display = 'none'; bird.y = 200; bird.velocity = 0; pipes = []; score = 0; scoreEl.innerText = score; frameCount = 0; gameRunning = true; gameLoop(); }
  canvas.addEventListener('mousedown', () => { if (gameRunning) { bird.velocity = bird.jump; playJumpSound(); } });

  function drawScene() {
    let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    skyGrad.addColorStop(0, '#2b8a94'); skyGrad.addColorStop(0.4, '#4ec0ca'); skyGrad.addColorStop(1, '#fffcd1');
    ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#489da6'; ctx.beginPath(); ctx.moveTo(0, canvas.height); ctx.quadraticCurveTo(60, canvas.height - 130, 150, canvas.height - 90); ctx.quadraticCurveTo(250, canvas.height - 140, canvas.width, canvas.height - 80); ctx.lineTo(canvas.width, canvas.height); ctx.fill();
    ctx.fillStyle = '#337146'; ctx.beginPath(); ctx.moveTo(0, canvas.height); ctx.quadraticCurveTo(90, canvas.height - 80, 200, canvas.height - 50); ctx.quadraticCurveTo(310, canvas.height - 90, canvas.width, canvas.height - 40); ctx.lineTo(canvas.width, canvas.height); ctx.fill();
  }

  function drawTree(px, py, pw, ph, isTop) {
    let trunkGrad = ctx.createLinearGradient(px, 0, px + pw, 0);
    trunkGrad.addColorStop(0, '#4a3329'); trunkGrad.addColorStop(0.5, '#8d6e63'); trunkGrad.addColorStop(1, '#3e2723');
    ctx.fillStyle = trunkGrad; ctx.fillRect(px, py, pw, ph);
    let leafY = isTop ? py + ph : py;
    let leafGrad = ctx.createRadialGradient(px + pw/2, leafY, 5, px + pw/2, leafY, 32);
    leafGrad.addColorStop(0, '#4caf50'); leafGrad.addColorStop(1, '#1b5e20');
    ctx.fillStyle = leafGrad; ctx.beginPath(); ctx.arc(px + pw/2, leafY, 32, 0, Math.PI * 2); ctx.fill();
  }

  function gameLoop() {
    if (!gameRunning) return;
    drawScene();
    bird.velocity += bird.gravity; bird.y += bird.velocity;
    if (bird.y + bird.height >= canvas.height || bird.y <= 0) { gameRunning = false; document.querySelector('#start-screen .overlay-title').innerText = "SCORE: " + score; startScreen.style.display = 'flex'; return; }
    if (frameCount % 135 === 0) { const minH = 60; const maxH = canvas.height - pipeGap - minH; const topH = Math.floor(Math.random() * (maxH - minH + 1)) + minH; pipes.push({ x: canvas.width, top: topH, bottom: canvas.height - topH - pipeGap, passed: false }); }
    frameCount++;
    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i]; p.x -= pipeSpeed;
      drawTree(p.x, 0, pipeWidth, p.top, true);
      let botY = canvas.height - p.bottom; drawTree(p.x, botY, pipeWidth, p.bottom, false);
      if (bird.x + 3 < p.x + pipeWidth && bird.x + bird.width - 3 > p.x && (bird.y + 3 < p.top || bird.y + bird.height - 3 > botY)) { gameRunning = false; document.querySelector('#start-screen .overlay-title').innerText = "SCORE: " + score; startScreen.style.display = 'flex'; return; }
      if (!p.passed && p.x + pipeWidth < bird.x) { p.passed = true; score++; scoreEl.innerText = score; }
      if (p.x + pipeWidth + 40 < 0) pipes.splice(i, 1);
    }
    
    // VẼ CHÚ CHIM SẮC NÉT + HIỆU ỨNG VỖ CÁNH DỰA VÀO MATH.SIN
    ctx.save(); 
    ctx.translate(bird.x + bird.width/2, bird.y + bird.height/2); 
    ctx.rotate(Math.max(-0.2, Math.min(0.5, bird.velocity * 0.08)));
    
    // Thân chim tròn vàng rực
    let bGrad = ctx.createRadialGradient(-2, -2, 2, 0, 0, bird.width/2); 
    bGrad.addColorStop(0, '#fff176'); bGrad.addColorStop(1, '#f4511e'); 
    ctx.fillStyle = bGrad; ctx.beginPath(); ctx.arc(0, 0, bird.width/2, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.stroke();
    
    // Mắt chim rõ nét hơn
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(6, -4, 5.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(7, -4, 2.2, 0, Math.PI * 2); ctx.fill();
    
    // NÂNG CẤP: Làm rõ mỏ chim đỏ cam nổi bật vươn dài ra trước
    ctx.fillStyle = '#f85818'; ctx.beginPath(); 
    ctx.moveTo(9, -3); 
    ctx.lineTo(20, 1); 
    ctx.lineTo(7, 6); 
    ctx.closePath(); ctx.fill(); ctx.stroke();
    
    // NÂNG CẤP: Hiệu ứng đập cánh liên tục lên xuống sống động
    let wingOscillation = Math.sin(frameCount * 0.4) * 3; // Cánh co giãn nhịp nhàng
    ctx.fillStyle = '#fff9c4'; ctx.beginPath(); 
    ctx.arc(-6, 2 + wingOscillation / 2, 5 + wingOscillation / 3, 0, Math.PI * 2); 
    ctx.fill(); ctx.stroke();
    
    ctx.restore();
    requestAnimationFrame(gameLoop);
  }
</script>
</body>
</html>
"""

components.html(game_html, height=540, scrolling=False)

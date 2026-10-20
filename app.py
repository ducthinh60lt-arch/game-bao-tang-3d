import streamlit as st
import streamlit.components.v1 as components

game_html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: #0f172a; text-align: center; user-select: none; }
  #container { max-width: 400px; margin: 0 auto; background: #1e293b; height: 530px; position: relative; overflow: hidden; }
  #score-board { position: absolute; top: 15px; left: 0; right: 0; font-size: 38px; font-weight: 900; color: #fff; text-shadow: 2px 2px 8px #000; font-family: sans-serif; z-index: 10; pointer-events: none; }
  canvas { display: block; width: 100%; height: 100%; cursor: pointer; }
  .overlay { position: absolute; inset: 0; background: linear-gradient(135deg, #1b3411, #4ec0ca); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: sans-serif; }
  .overlay-title { font-size: 34px; font-weight: 900; color: #fff; margin-bottom: 25px; text-shadow: 3px 3px 0px #0e1f05; }
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
  const pipeWidth = 80, pipeGap = 175, pipeSpeed = 1.4;
  let bokehParticles = [];
  for (let i = 0; i < 15; i++) {
    bokehParticles.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, radius: Math.random() * 6 + 2, speed: Math.random() * 0.3 + 0.1, alpha: Math.random() * 0.4 + 0.1 });
  }
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
  function drawBeautifulScene() {
    let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    skyGrad.addColorStop(0, '#21717a'); skyGrad.addColorStop(0.3, '#3ba2ad'); skyGrad.addColorStop(0.6, '#7accc2'); skyGrad.addColorStop(1, '#fffae0');
    ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, canvas.height);
    let sunGrad = ctx.createRadialGradient(40, 40, 0, 40, 40, 120);
    sunGrad.addColorStop(0, 'rgba(255, 255, 255, 1)'); sunGrad.addColorStop(0.2, 'rgba(255, 249, 196, 0.8)'); sunGrad.addColorStop(0.6, 'rgba(255, 224, 130, 0.3)'); sunGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = sunGrad; ctx.beginPath(); ctx.arc(40, 40, 120, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(255, 255, 255, 0.75)'; drawCloud(100, 80, 20); drawCloud(290, 60, 26);
    ctx.fillStyle = '#41939c'; ctx.beginPath(); ctx.moveTo(0, canvas.height); ctx.quadraticCurveTo(60, canvas.height - 140, 150, canvas.height - 95); ctx.quadraticCurveTo(250, canvas.height - 150, canvas.width, canvas.height - 85); ctx.lineTo(canvas.width, canvas.height); ctx.fill();
    ctx.fillStyle = '#37878e'; for (let i = 0; i < canvas.width; i += 25) { ctx.beginPath(); ctx.arc(i, canvas.height - 90, 12, 0, Math.PI, true); ctx.fill(); }
    ctx.fillStyle = '#2c693a'; ctx.beginPath(); ctx.moveTo(0, canvas.height); ctx.quadraticCurveTo(90, canvas.height - 90, 200, canvas.height - 55); ctx.quadraticCurveTo(310, canvas.height - 100, canvas.width, canvas.height - 45); ctx.lineTo(canvas.width, canvas.height); ctx.fill();
    ctx.fillStyle = '#235732'; let offset = (frameCount * 0.3) % 20; for (let i = -20; i < canvas.width + 20; i += 20) { ctx.beginPath(); ctx.arc(i - offset, canvas.height - 50, 14, 0, Math.PI, true); ctx.fill(); }
    bokehParticles.forEach(p => { p.y -= p.speed; if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width; } ctx.fillStyle = `rgba(255, 253, 231, ${p.alpha})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fill(); });
  }
  function drawCloud(x, y, r) {
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.arc(x + r * 0.6, y - r * 0.3, r * 0.8, 0, Math.PI * 2); ctx.arc(x + r * 1.2, y, r * 0.6, 0, Math.PI * 2); ctx.fill();
  }
  function drawBeautifulPremiumTree(px, py, pw, ph, isTop) {
    ctx.save();
    let trunkGrad = ctx.createLinearGradient(px + pw*0.3, 0, px + pw*0.7, 0);
    trunkGrad.addColorStop(0, '#3e2723'); trunkGrad.addColorStop(0.5, '#6d4c41'); trunkGrad.addColorStop(1, '#2d1510');
    ctx.fillStyle = trunkGrad; ctx.fillRect(px + pw * 0.35, py, pw * 0.3, ph);
    let leafY = isTop ? py + ph : py, branchDir = isTop ? -1 : 1;
    ctx.fillStyle = '#3e2723';
    ctx.beginPath(); ctx.moveTo(px + pw * 0.5, leafY); ctx.lineTo(px + pw * 0.08, leafY + 28 * branchDir); ctx.lineTo(px + pw * 0.18, leafY + 34 * branchDir); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(px + pw * 0.5, leafY); ctx.lineTo(px + pw * 0.92, leafY + 28 * branchDir); ctx.lineTo(px + pw * 0.82, leafY + 34 * branchDir); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#142d0c'; ctx.beginPath(); ctx.arc(px + pw * 0.15, leafY, 34, 0, Math.PI * 2); ctx.arc(px + pw * 0.5, leafY - 6 * branchDir, 45, 0, Math.PI * 2); ctx.arc(px + pw * 0.85, leafY, 34, 0, Math.PI * 2); ctx.fill();
    let leafGrad = ctx.createRadialGradient(px + pw*0.5, leafY, 5, px + pw*0.5, leafY, 40);
    leafGrad.addColorStop(0, '#55bb22'); leafGrad.addColorStop(1, '#255e13');
    ctx.fillStyle = leafGrad; ctx.beginPath(); ctx.arc(px + pw * 0.22, leafY + 2 * branchDir, 28, 0, Math.PI * 2); ctx.arc(px + pw * 0.5, leafY - 2 * branchDir, 40, 0, Math.PI * 2); ctx.arc(px + pw * 0.78, leafY + 2 * branchDir, 28, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#99e03d'; ctx.beginPath(); ctx.arc(px + pw * 0.32, leafY - 14 * branchDir, 16, 0, Math.PI * 2); ctx.arc(px + pw * 0.56, leafY - 18 * branchDir, 20, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }
  function gameLoop() {
    if (!gameRunning) return;
    drawBeautifulScene();
    bird.velocity += bird.gravity; bird.y += bird.velocity;
    if (bird.y + bird.height >= canvas.height || bird.y <= 0) { gameRunning = false; document.querySelector('#start-screen .overlay-title').innerText = "SCORE: " + score; startScreen.style.display = 'flex'; return; }
    if (frameCount % 135 === 0) { const minH = 60; const maxH = canvas.height - pipeGap - minH; const topH = Math.floor(Math.random() * (maxH - minH + 1)) + minH; pipes.push({ x: canvas.width, top: topH, bottom: canvas.height - topH - pipeGap, passed: false }); }
    frameCount++;
    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i]; p.x -= pipeSpeed;
      drawBeautifulPremiumTree(p.x, 0, pipeWidth, p.top, true);
      let botY = canvas.height - p.bottom; drawBeautifulPremiumTree(p.x, botY, pipeWidth, p.bottom, false);
      if (bird.x + 3 < p.x + pipeWidth && bird.x + bird.width - 3 > p.x && (bird.y + 3 < p.top || bird.y + bird.height - 3 > botY)) { gameRunning = false; document.querySelector('#start-screen .overlay-title').innerText = "SCORE: " + score; startScreen.style.display = 'flex'; return; }
      if (!p.passed && p.x + pipeWidth < bird.x) { p.passed = true; score++; scoreEl.innerText = score; }
      if (p.x + pipeWidth + 50 < 0) pipes.splice(i, 1);
    }
    ctx.save(); ctx.translate(bird.x + bird.width/2, bird.y + bird.height/2); ctx.rotate(Math.max(-0.2, Math.min(0.5, bird.velocity * 0.08)));
    let bGrad = ctx.createRadialGradient(-2, -2, 2, 0, 0, bird.width/2); bGrad.addColorStop(0, '#fff176'); bGrad.addColorStop(1, '#f4511e'); ctx.fillStyle = bGrad; ctx.beginPath(); ctx.arc(0, 0, bird.width/2, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(5, -4, 5.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(6, -4, 2.2, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#f85818'; ctx.beginPath(); ctx.moveTo(9, -3); ctx.lineTo(20, 1); ctx.lineTo(7, 6); ctx.closePath(); ctx.fill(); ctx.stroke();
    let wingOscillation = Math.sin(frameCount * 0.4) * 3; ctx.fillStyle = '#fff9c4'; ctx.beginPath(); ctx.arc(-6, 2 + wingOscillation / 2, 5 + wingOscillation / 3, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.restore();
    requestAnimationFrame(gameLoop);
  }
</script>
</body>
</html>
"""

components.html(game_html, height=540, scrolling=False)

import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game Chim Nhảy - Flappy Bird Pro",
    page_icon="🐦",
    layout="centered",
)

st.title("🐦 Game Chim Nhảy (Flappy Bird)")
st.markdown(
    "**Cách chơi:** \n"
    "1. Bấm nút **BẮT ĐẦU CHƠI** ở màn hình mở đầu để kích hoạt game và nhạc nền.\n"
    "2. **Click chuột trái vào bất kỳ đâu trên khung game** để điều khiển chú chim vỗ cánh bay lên.\n"
    "3. Giúp chim vượt qua các khoảng trống giữa các đường ống nước để ghi điểm!"
)

# 2. Mã nguồn ứng dụng Game Chim Nhảy tích hợp hệ thống Vật lý + Nhạc nền + Cài đặt
game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
  body { margin: 0; background: #0f172a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; user-select: none; padding-top: 10px; }
  #container { max-width: 400px; margin: 0 auto; background: #1e293b; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; overflow: hidden; height: 530px; }
  
  /* Thanh đầu mục thông số & nút cài đặt */
  #header-bar { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }
  #score-board { font-size: 24px; font-weight: bold; color: #fff; text-shadow: 1px 1px 3px rgba(0,0,0,0.8); }
  #btn-settings { background: rgba(51, 65, 85, 0.8); border: none; color: white; font-size: 22px; cursor: pointer; padding: 4px 10px; border-radius: 6px; backdrop-filter: blur(4px); }

  /* Khung vẽ Canvas chứa toàn bộ chuyển động game */
  canvas { display: block; background: #70c5ce; width: 100%; height: 100%; cursor: pointer; }

  /* Màn hình chờ mở đầu & Cửa sổ Cài đặt */
  .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.95); z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box; }
  .overlay-title { font-size: 28px; font-weight: bold; color: #f59e0b; margin-bottom: 25px; text-transform: uppercase; }
  
  .setting-row { width: 85%; margin-bottom: 20px; text-align: left; }
  .setting-label { font-size: 14px; color: #94a3b8; margin-bottom: 6px; font-weight: bold; }
  
  select { width: 100%; padding: 10px; border-radius: 6px; background: #334155; border: 2px solid #475569; color: white; font-size: 15px; outline: none; cursor: pointer; }
  .btn-main { width: 85%; padding: 12px; font-size: 18px; font-weight: bold; color: white; background: #10b981; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s; margin-top: 10px; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }
  .btn-main:hover { background: #059669; }
  .btn-close { background: #ef4444 !important; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3) !important; }
  .btn-close:hover { background: #dc2626 !important; }
</style>
</head>
<body>

<div id="container">
  <!-- MÀN HÌNH KHỞI ĐẦU CHÀO MỪNG -->
  <div id="start-screen" class="overlay">
    <div class="overlay-title">🐦 CHIM NHẢY PRO</div>
    <div class="setting-row">
      <div class="setting-label">Chọn nhạc nền khởi động:</div>
      <select id="start-music-select">
        <option value="https://mixkit.co">Chill Game Level (Mặc định)</option>
        <option value="https://mixkit.co">Dreaming Big (Nhẹ nhàng)</option>
        <option value="https://mixkit.co">Tech House (Sôi động)</option>
      </select>
    </div>
    <button class="btn-main" onclick="startGame()">BẮT ĐẦU CHƠI</button>
  </div>

  <!-- MENU CÀI ĐẶT TRONG LÚC CHƠI -->
  <div id="settings-screen" class="overlay" style="display: none;">
    <div class="overlay-title">⚙️ CÀI ĐẶT GAME</div>
    <div class="setting-row">
      <div class="setting-label">Trạng thái nhạc:</div>
      <select id="music-toggle" onchange="toggleMusicState()">
        <option value="on">Đang Bật (On)</option>
        <option value="off">Tắt Nhạc (Off)</option>
      </select>
    </div>
    <div class="setting-row">
      <div class="setting-label">Thay đổi bài hát:</div>
      <select id="game-music-select" onchange="changeTrack(this.value)">
        <option value="https://mixkit.co">Chill Game Level</option>
        <option value="https://mixkit.co">Dreaming Big</option>
        <option value="https://mixkit.co">Tech House</option>
      </select>
    </div>
    <button class="btn-main btn-close" onclick="closeSettings()">QUAY LẠI CHƠI</button>
  </div>

  <!-- KHU VỰC ĐỒ HỌA GAME CHÍNH -->
  <div id="header-bar">
    <div id="score-board">Điểm: <span id="score">0</span></div>
    <button id="btn-settings" onclick="openSettings()">⚙️</button>
  </div>
  
  <canvas id="gameCanvas" width="400" height="530"></canvas>
</div>

<!-- Hệ thống phát âm thanh ẩn -->
<audio id="bg-audio" loop></audio>

<script>
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const scoreEl = document.getElementById('score');
  const startScreen = document.getElementById('start-screen');
  const settingsScreen = document.getElementById('settings-screen');
  const audioPlayer = document.getElementById('bg-audio');

  // Trạng thái vận hành
  let gameRunning = false;
  let score = 0;
  let isMusicPlaying = true;

  // Thuộc tính vật lý của chú chim
  const bird = {
    x: 50,
    y: 200,
    width: 34,
    height: 24,
    gravity: 0.25,  // Tốc độ rơi tự do
    velocity: 0,
    jump: -5.5      // Độ cao vút lên khi click nhảy
  };

  // Mảng lưu danh sách các đường ống nước
  let pipes = [];
  const pipeWidth = 60;
  const pipeGap = 120; // Khoảng cách khe hở để chim chui qua
  const pipeSpeed = 2; // Tốc độ di chuyển của ống từ phải qua trái
  let frameCount = 0;

  // Kích hoạt khi nhấn bắt đầu chơi
  function startGame() {
    const startSelect = document.getElementById('start-music-select');
    audioPlayer.src = startSelect.value;
    document.getElementById('game-music-select').value = startSelect.value;
    
    // Tự động phát nhạc nhờ tương tác nút bấm của người dùng
    audioPlayer.play().catch(err => console.log("Lệnh phát tự động bị chặn: ", err));
    
    startScreen.style.display = 'none';
    resetGame();
    gameRunning = true;
    gameLoop();
  }

  // Quản lý bảng cài đặt ⚙️
  function openSettings() { gameRunning = false; settingsScreen.style.display = 'flex'; }
  function closeSettings() { settingsScreen.style.display = 'none'; gameRunning = true; gameLoop(); }

  function toggleMusicState() {
    const state = document.getElementById('music-toggle').value;
    if (state === 'off') { audioPlayer.pause(); isMusicPlaying = false; } 
    else { audioPlayer.play(); isMusicPlaying = true; }
  }

  function changeTrack(url) {
    audioPlayer.src = url;
    if (isMusicPlaying) audioPlayer.play();
  }

  // Sự kiện nhấp chuột trái vào màn hình để CHIM NHẢY LÊN
  canvas.addEventListener('click', () => {
    if (!gameRunning) return;
    bird.velocity = bird.jump; // Làm vận tốc âm để bay ngược lên trên
  });

  function resetGame() {
    bird.y = 200;
    bird.velocity = 0;
    pipes = [];
    score = 0;
    scoreEl.innerText = score;
    frameCount = 0;
  }

  // Vòng lặp tính toán đồ họa liên tục
  function gameLoop() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Cập nhật cơ chế vật lý của chú Chim
    bird.velocity += bird.gravity;
    bird.y += bird.velocity;

    // Vẽ chú chim (Hình tròn màu vàng ngộ nghĩnh)
    ctx.fillStyle = '#f59e0b';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2, bird.y + bird.height/2, bird.width/2, 0, Math.PI * 2);
    ctx.fill();
    // Vẽ mắt chim
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.arc(bird.x + bird.width/2 + 6, bird.y + bird.height/2 - 4, 2, 0, Math.PI * 2);
    ctx.fill();
    // Vẽ mỏ chim màu đỏ
    ctx.fillStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(bird.x + bird.width, bird.y + bird.height/2 - 2);
    ctx.lineTo(bird.x + bird.width + 8, bird.y + bird.height/2 + 2);
    ctx.lineTo(bird.x + bird.width, bird.y + bird.height/2 + 6);
    ctx.fill();

    // Kiểm tra chạm sàn hoặc chạm trần nhà
    if (bird.y + bird.height >= canvas.height || bird.y <= 0) {
      gameOver();
      return;
    }

    // 2. Xử lý xuất hiện và di chuyển các Cột Ống Nước
    if (frameCount % 100 === 0) {
      // Chiều cao ngẫu nhiên của ống nước trên
      const minHeight = 40;
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

    // Vẽ và kiểm tra va chạm từng cặp ống nước
    for (let i = pipes.length - 1; i >= 0; i--) {
      let p = pipes[i];
      p.x -= pipeSpeed; // Di chuyển ống sang bên trái

      ctx.fillStyle = '#10b981'; // Màu xanh lá cho ống nước
      
      // Vẽ ống nước phía trên
      ctx.fillRect(p.x, 0, pipeWidth, p.top);
      ctx.strokeStyle = '#047857';
      ctx.strokeRect(p.x, 0, pipeWidth, p.top);

      // Vẽ ống nước phía dưới
      ctx.fillRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom);
      ctx.strokeRect(p.x, canvas.height - p.bottom, pipeWidth, p.bottom);

// Thuật toán kiểm tra va chạm hình học (Collision Detection)
if (
bird.x < p.x + pipeWidth &&
bird.x + bird.width > p.x &&
(bird.y < p.top || bird.y + bird.height > canvas.height - p.bottom)
) {
gameOver();
return;
// Tính điểm khi chim vượt qua ống thành công
if (!p.passed && p.x + pipeWidth < bird.x) {
p.passed = true;
score++;
scoreEl.innerText = score;
// Xóa ống khỏi mảng khi đã trượt ra ngoài màn hình để giải phóng RAM
if (p.x + pipeWidth < 0) {
pipes.splice(i, 1);
}
}
requestAnimationFrame(gameLoop);
}
function gameOver() {
gameRunning = false;
// Đưa người chơi trở lại màn hình mở đầu khi thua cuộc
document.querySelector('#start-screen .overlay-title').innerText = "BẠN ĐÃ THUA! SCORE: " + score;
document.querySelector('#start-screen .btn-main').innerText = "CHƠI LẠI";
startScreen.style.display = 'flex';
}
"""
components.html(game_html, height=540, scrolling=False)

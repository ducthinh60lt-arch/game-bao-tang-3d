import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D - 7 Kiệt Tác",
    page_icon="🎮",
    layout="wide",
)

st.title("🎮 Hành Trình Bảo Tàng 3D – 7 Kiệt Tác")
st.markdown(
    "Dùng **W/A/S/D** hoặc **phím mũi tên** để di chuyển, "
    "kéo chuột trái để xoay góc nhìn. Đến gần tranh rồi nhấn chuột "
    "để chuyển sang tác phẩm tiếp theo. Nhấn **BẬT NHẠC** để bật nhạc."
)

game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html, body { margin:0; width:100%; height:100%; overflow:hidden; background:#020204; color:#fff; font-family:Arial,sans-serif; }
  #game { position:relative; width:100%; height:600px; overflow:hidden; background:#020204; }
  canvas { display:block; width:100%; height:100%; }
  #music-btn { position:absolute; z-index:5; top:14px; left:14px; padding:10px 16px; border:0; border-radius:6px; background:#d4af37; color:#111; font-weight:bold; cursor:pointer; }
  #help { position:absolute; z-index:4; top:14px; right:14px; max-width:250px; padding:10px 12px; background:#08080ddd; border:1px solid #806c2c; border-radius:8px; font-size:12px; line-height:1.5; }
  #info { position:absolute; z-index:4; left:50%; bottom:18px; transform:translateX(-50%); width:max-content; max-width:82%; box-sizing:border-box; text-align:center; padding:13px 22px; background:#050508e8; border:1px solid #d4af37; border-radius:10px; pointer-events:none; }
  #title { color:#e5c65b; font-size:20px; font-weight:bold; margin-bottom:5px; }
  #meta { color:#eee; font-size:13px; }
  #error { display:none; position:absolute; z-index:8; inset:65px 12px auto; padding:12px; background:#581b1b; border:1px solid #ff7777; border-radius:8px; }
  @media(max-width:600px) { #game { height:500px; } #help { top:64px; left:12px; right:auto; } #info { max-width:94%; padding:10px 12px; } #title {font-size:16px;} }
</style>
<script src="https://jsdelivr.net"></script>
<script src="https://jsdelivr.net"></script>
<script src="https://jsdelivr.net"></script>
</head>
<body>
<div id="game">
  <button id="music-btn" type="button">🎵 BẬT NHẠC NỀN</button>
  <div id="help">W/A/S/D hoặc phím mũi tên: di chuyển<br>Kéo chuột: xoay góc nhìn<br>Đến gần tranh rồi nhấp chuột: chuyển tranh</div>
  <div id="error"></div>
  <div id="info"><div id="title">Đang dựng bảo tàng 3D…</div><div id="meta">Đang khởi tạo không gian triển lãm</div></div>
</div>
<script>
(() => {
  const root = document.getElementById('game');
  const errorBox = document.getElementById('error');
  const titleUI = document.getElementById('title');
  const metaUI = document.getElementById('meta');
  const musicBtn = document.getElementById('music-btn');

  function showError(message) {
    errorBox.style.display = 'block';
    errorBox.textContent = 'Không thể khởi tạo game: ' + message;
  }

  if (!window.THREE || !THREE.OrbitControls || !window.TWEEN) {
    showError('Không tải được thư viện 3D từ CDN.');
    return;
  }

  const artList = [
    {title:'Đêm đầy sao', meta:'Vincent van Gogh · Trường phái Ấn tượng', color:0x1b2f56, accent:0xf3cb46},
    {title:'Mona Lisa', meta:'Leonardo da Vinci · Thời kỳ Phục Hưng', color:0x393e2b, accent:0xa68a56},
    {title:'Lady with an Ermine', meta:'Leonardo da Vinci · Chân dung Phục Hưng', color:0x4d3327, accent:0xcbb082},
    {title:'The Scream', meta:'Edvard Munch · Trường phái Biểu hiện', color:0x7e3517, accent:0xdf9836},
    {title:'The Last Supper', meta:'Leonardo da Vinci · Bữa ăn tối cuối cùng', color:0x3c3025, accent:0xbd9a2b},
    {title:'Girl with a Pearl Earring', meta:'Johannes Vermeer · Hội họa Hà Lan', color:0x163549, accent:0xcaa36d},
    {title:'Adam and Eve', meta:'Albrecht Dürer · Nghệ thuật Phục Hưng', color:0x3f492b, accent:0xaa986b}
  ];

  let scene, camera, renderer, controls, currentIndex = 0, transitioning = false;
  let artworkGroup;
  const keys = Object.create(null);
  const speed = 0.12;

  let audioCtx = null, oscillator = null, gainNode = null, musicPlaying = false;
  musicBtn.addEventListener('click', () => {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      gainNode = audioCtx.createGain();
      gainNode.gain.setValueAtTime(0.04, audioCtx.currentTime);
      gainNode.connect(audioCtx.destination);
    }
    if (!musicPlaying) {
      oscillator = audioCtx.createOscillator();
      oscillator.type = 'triangle';
      oscillator.frequency.setValueAtTime(293.66, audioCtx.currentTime); // Âm giai Re dịu nhẹ
      oscillator.connect(gainNode);
      oscillator.start();
      musicPlaying = true;
      musicBtn.textContent = "⏸ TẮT NHẠC NỀN";
    } else {
      oscillator.stop();
      musicPlaying = false;
      musicBtn.textContent = "🎵 BẬT NHẠC NỀN";
    }
  });

  try {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x06060a);
    scene.fog = new THREE.Fog(0x06060a, 15, 40);

    camera = new THREE.PerspectiveCamera(60, root.clientWidth / root.clientHeight, 0.1, 100);
    camera.position.set(0, 2.2, 9);

    renderer = new THREE.WebGLRenderer({antialias:true, powerPreference:'high-performance'});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setSize(root.clientWidth, root.clientHeight);
    root.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.enablePan = false;
    controls.minDistance = 2;
    controls.maxDistance = 14;
    controls.maxPolarAngle = Math.PI * 0.48;
    controls.target.set(0, 2.2, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x24170f, 1.1));
    const mainLight = new THREE.PointLight(0xffe0b3, 1.5, 30);
    mainLight.position.set(0, 6, 2);
    scene.add(mainLight);

    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(40, 40),
      new THREE.MeshStandardMaterial({color:0x221a14, roughness:0.9})
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    const wallMat = new THREE.MeshStandardMaterial({color:0x121215, roughness:0.95});
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(36, 10, 0.5), wallMat);
    backWall.position.set(0, 5, -10);
    scene.add(backWall);

    artworkGroup = new THREE.Group();
    scene.add(artworkGroup);

    function makeArtwork(index) {
      while (artworkGroup.children.length) {
        const child = artworkGroup.children.pop();
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
      }
      const art = artList[index];
      titleUI.textContent = art.title;
      metaUI.textContent = art.meta;

      const frame = new THREE.Mesh(
        new THREE.BoxGeometry(5.4, 3.9, 0.2),
        new THREE.MeshStandardMaterial({color:0xd4af37, metalness:0.7, roughness:0.3})
      );
      frame.position.set(0, 4.0, -9.7);
      artworkGroup.add(frame);

      const canvas = document.createElement('canvas');
      canvas.width = 512; canvas.height = 384;
      const ctx = canvas.getContext('2d');
      const grad = ctx.createLinearGradient(0,0,512,384);
      grad.addColorStop(0, '#' + art.color.toString(16).padStart(6,'0'));
      grad.addColorStop(1, '#' + art.accent.toString(16).padStart(6,'0'));
      ctx.fillStyle = grad; ctx.fillRect(0,0,512,384);
      
      ctx.globalAlpha = 0.35;
      for(let i=0; i<50; i++){
        ctx.fillStyle = i%2 ? '#fff' : '#000';
        ctx.beginPath();
        ctx.arc((i*43+index*79)%512, (i*29+index*61)%384, (i%10)+4, 0, Math.PI*2);
        ctx.fill();
      }
      ctx.globalAlpha = 1.0;
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 22px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(art.title, 256, 192);

      const texture = new THREE.CanvasTexture(canvas);
      const picture = new THREE.Mesh(
        new THREE.PlaneGeometry(5.1, 3.6),
        new THREE.MeshBasicMaterial({map: texture})
      );
      picture.position.set(0, 4.0, -9.58);
      artworkGroup.add(picture);
    }

    makeArtwork(currentIndex);

    window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
    window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

    window.addEventListener('click', (e) => {
      if (e.target.id === 'music-btn' || transitioning) return;
      const dist = camera.position.distanceTo(new THREE.Vector3(0, 2.2, -9.5));
      if (dist < 6.0) {
        transitioning = true;
        currentIndex = (currentIndex + 1) % artList.length;
        new TWEEN.Tween(camera.position)
          .to({z: 8, x: 0}, 750)
          .easing(TWEEN.Easing.Quadratic.Out)
          .onComplete(() => {
            makeArtwork(currentIndex);
            transitioning = false;
          })
          .start();
      }
    });

    function animate() {
      requestAnimationFrame(animate);
      TWEEN.update();

      const forward = new THREE.Vector3();
      camera.getWorldDirection(forward);
      forward.y = 0;
      forward.normalize();

      const side = new THREE.Vector3();
      side.crossVectors(camera.up, forward).normalize();

      if (keys['w'] || keys['arrowup']) camera.position.addScaledVector(forward, speed);
      if (keys['s'] || keys['arrowdown']) camera.position.addScaledVector(forward, -speed);
      if (keys['a'] || keys['arrowleft']) camera.position.addScaledVector(side, speed);
      if (keys['d'] || keys['arrowright']) camera.position.addScaledVector(side, -speed);

      camera.position.x = Math.max(-12, Math.min(12, camera.position.x));
      camera.position.z = Math.max(-7, Math.min(12, camera.position.z));

      controls.update();
      renderer.render(scene, camera);
    }
requestAnimationFrame(animate);
window.addEventListener('resize', () => {
camera.aspect = root.clientWidth / root.clientHeight;
camera.updateProjectionMatrix();
renderer.setSize(root.clientWidth, root.clientHeight);
});
} catch (err) {
showError(err.message);
}
})();



"""
components.html(game_html, height=620, scrolling=False)

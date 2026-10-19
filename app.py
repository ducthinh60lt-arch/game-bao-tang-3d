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
  #game { position:relative; width:100%; height:680px; overflow:hidden; background:#020204; }
  canvas { display:block; width:100%; height:100%; }
  #music-btn { position:absolute; z-index:5; top:14px; left:14px; padding:10px 16px; border:0; border-radius:6px; background:#d4af37; color:#111; font-weight:bold; cursor:pointer; }
  #help { position:absolute; z-index:4; top:14px; right:14px; max-width:250px; padding:10px 12px; background:#08080ddd; border:1px solid #806c2c; border-radius:8px; font-size:12px; line-height:1.5; }
  #info { position:absolute; z-index:4; left:50%; bottom:18px; transform:translateX(-50%); width:max-content; max-width:82%; box-sizing:border-box; text-align:center; padding:13px 22px; background:#050508e8; border:1px solid #d4af37; border-radius:10px; pointer-events:none; }
  #title { color:#e5c65b; font-size:20px; font-weight:bold; margin-bottom:5px; }
  #meta { color:#eee; font-size:13px; }
  #error { display:none; position:absolute; z-index:8; inset:65px 12px auto; padding:12px; background:#581b1b; border:1px solid #ff7777; border-radius:8px; }
  @media(max-width:600px) { #game { height:620px; } #help { top:64px; left:12px; right:auto; } #info { max-width:94%; padding:10px 12px; } #title {font-size:16px;} }
</style>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tweenjs/tween.js@18.6.4/dist/tween.umd.js"></script>
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
  function showError(message) {
    errorBox.style.display = 'block';
    errorBox.textContent = 'Không thể khởi tạo game: ' + message + '. Hãy kiểm tra kết nối mạng hoặc tải lại trang.';
  }
  if (!window.THREE || !THREE.OrbitControls || !window.TWEEN) {
    showError('Không tải được thư viện 3D');
    return;
  }

  const artList = [
  {title:'Đêm đầy sao', meta:'Vincent van Gogh · Bảo tàng nghệ thuật', color:0x2d5eaa, accent:0xf2d35e},
    {title:'Mona Lisa', meta:'Leonardo da Vinci · Thời kỳ Phục Hưng', color:0x4a6844, accent:0xc7a66b},
    {title:'Lady with an Ermine', meta:'Leonardo da Vinci · Chân dung Phục Hưng', color:0x6c493b, accent:0xe0c7a0},
    {title:'The Scream', meta:'Edvard Munch · Trường phái Biểu hiện', color:0x9c4b2e, accent:0xf2b44d},
    {title:'The Last Supper', meta:'Leonardo da Vinci · Bữa ăn tối cuối cùng', color:0x493b30, accent:0xd4af37},
    {title:'Girl with a Pearl Earring', meta:'Johannes Vermeer · Hội họa Hà Lan', color:0x244e67, accent:0xe9d7b0},
    {title:'Adam and Eve', meta:'Albrecht Dürer · Nghệ thuật Phục Hưng', color:0x53643d, accent:0xc7b58b}
  ];

  let scene, camera, renderer, controls, currentIndex = 0, transitioning = false;
  let artworkGroup;
  const keys = Object.create(null);
  const speed = 0.12;

  try {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x08080d);
    scene.fog = new THREE.Fog(0x08080d, 18, 48);

    camera = new THREE.PerspectiveCamera(65, root.clientWidth / root.clientHeight, 0.1, 100);
    camera.position.set(0, 2.3, 10);

    renderer = new THREE.WebGLRenderer({antialias:true, powerPreference:'high-performance'});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.7));
    renderer.setSize(root.clientWidth, root.clientHeight);
    root.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.07;
    controls.enablePan = false;
    controls.minDistance = 2;
    controls.maxDistance = 18;
    controls.maxPolarAngle = Math.PI * 0.49;
    controls.target.set(0, 2.2, 0);

    scene.add(new THREE.HemisphereLight(0xbfcfff, 0x24170f, 1.25));
    const mainLight = new THREE.PointLight(0xffdca0, 2.0, 35);
    mainLight.position.set(0, 7, 4);
    scene.add(mainLight);


    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(38, 38),
      new THREE.MeshStandardMaterial({color:0x29221d, roughness:0.92})
    );
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = 0;
    scene.add(floor);

    // Tường cuối phòng và hai tường bên
    const wallMat = new THREE.MeshStandardMaterial({color:0x17171e, roughness:0.95});
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(36, 9, 0.4), wallMat);
    backWall.position.set(0, 4.5, -13);
    scene.add(backWall);
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, 9, 27), wallMat);
    leftWall.position.set(-18, 4.5, 0);
    scene.add(leftWall);
    const rightWall = leftWall.clone();
    rightWall.position.x = 18;
    scene.add(rightWall);

    // Đèn trần trang trí
    for (let x=-12; x<=12; x+=6) {
      const lamp = new THREE.PointLight(0xffd38a, 1.3, 12);
      lamp.position.set(x, 7.5, -5);
      scene.add(lamp);
      const bulb = new THREE.Mesh(
        new THREE.SphereGeometry(0.12, 12, 8),
        new THREE.MeshBasicMaterial({color:0xffe2a0})
      );
      bulb.position.copy(lamp.position);
      scene.add(bulb);
    }
    artworkGroup = new THREE.Group();
    scene.add(artworkGroup);

    function makeArtwork(index) {
      while (artworkGroup.children.length) {
        const child = artworkGroup.children.pop();
        if (child.geometry) child.geometry.dispose();
        if (child.material) {
          if (Array.isArray(child.material)) child.material.forEach(m=>m.dispose());
          else child.material.dispose();
        }
      }
      const art = artList[index];
      const frame = new THREE.Mesh(
        new THREE.BoxGeometry(5.4, 3.9, 0.25),
        new THREE.MeshStandardMaterial({color:0xc5a04b, metalness:0.65, roughness:0.32})
      );
      frame.position.set(0, 4.1, -12.55);
      artworkGroup.add(frame);

      const canvas = document.createElement('canvas');
      canvas.width = 600; canvas.height = 420;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#' + art.color.toString(16).padStart(6,'0');
      ctx.fillRect(0,0,600,420);
      // Tạo hình minh họa nghệ thuật bằng các mảng màu, không phụ thuộc URL ảnh ngoài
      const grad = ctx.createLinearGradient(0,0,600,420);
      grad.addColorStop(0, '#' + art.color.toString(16).padStart(6,'0'));
      grad.addColorStop(1, '#' + art.accent.toString(16).padStart(6,'0'));
      ctx.fillStyle = grad; ctx.fillRect(0,0,600,420);
      ctx.globalAlpha = 0.75;
      for(let i=0;i<120;i++){
        ctx.fillStyle = i%2 ? '#fff0b5' : '#101522';
        ctx.beginPath();
        const x = (i*137 + index*43)%600, y=(i*71 + index*29)%420;
        ctx.arc(x,y, (i%7)+2, 0, Math.PI*2); ctx.fill();
      }
      ctx.globalAlpha = 1;
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 28px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(art.title, 300, 380);
      const texture = new THREE.CanvasTexture(canvas);
      const picture = new THREE.Mesh(
        new THREE.PlaneGeometry(5.05, 3.55),
        new THREE.MeshBasicMaterial({map:texture})
      );
      picture.position.set(0,4.1,-12.38);
      artworkGroup.add(picture);

      document.getElementById('title').textContent = art.title;
      document.getElementById('meta').textContent = art.meta + ' · Nhấp khi đứng gần để xem tác phẩm tiếp theo';
      const glow = new THREE.PointLight(art.accent, 1.0, 9);
      glow.position.set(0,5.2,-9.8);
      artworkGroup.add(glow);
    }
    makeArtwork(currentIndex);

    // Bố trí các cột nhỏ hai bên hành lang
    for (const side of [-1,1]) {
      for (let z=-10; z<=8; z+=6) {
        const column = new THREE.Mesh(
          new THREE.BoxGeometry(0.65,3.2,0.65),
          new THREE.MeshStandardMaterial({color:0x5a4936, roughness:0.75})
        );
        column.position.set(side*8,1.6,z);
        scene.add(column);
      }
    }

    // Âm thanh tự tạo bằng Web Audio, không cần URL nhạc ngoài
     let audioCtx = null, masterGain = null, musicTimer = null, noteIndex = 0;
    const notes = [261.63,329.63,392.00,329.63,293.66,349.23,440.00,349.23];
    function startMusic() {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) {
        document.getElementById('music-btn').textContent = 'Trình duyệt không hỗ trợ nhạc';
        return;
      }
      if (!audioCtx) {
        audioCtx = new AudioContextClass();
        masterGain = audioCtx.createGain();
        masterGain.gain.value = 0.045;
        masterGain.connect(audioCtx.destination);
      }
      audioCtx.resume();
      if (musicTimer) {
        clearInterval(musicTimer);
        musicTimer = null;
        document.getElementById('music-btn').textContent = '🎵 BẬT NHẠC NỀN';
        return;
      }
      musicTimer = setInterval(() => {
        if (!audioCtx || audioCtx.state !== 'running') return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.value = notes[noteIndex % notes.length];
        noteIndex++;
        gain.gain.setValueAtTime(0.0001, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.25, audioCtx.currentTime + 0.08);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.65);
        osc.connect(gain); gain.connect(masterGain);
        osc.start(); osc.stop(audioCtx.currentTime + 0.7);
      }, 520);
      document.getElementById('music-btn').textContent = '⏸️ TẠM DỪNG NHẠC';
    }
    document.getElementById('music-btn').addEventListener('click', startMusic);

// Bấm tranh chỉ khi không kéo chuột và đang ở gần phòng tranh
    let pointerDown = null;
    renderer.domElement.addEventListener('pointerdown', e => {
      pointerDown = {x:e.clientX, y:e.clientY};
    });
    renderer.domElement.addEventListener('pointerup', e => {
      if (!pointerDown) return;
      const distance = Math.hypot(e.clientX-pointerDown.x, e.clientY-pointerDown.y);
      pointerDown = null;
      if (distance > 5 || transitioning) return;
      const distanceToArtwork = Math.hypot(camera.position.x, camera.position.z - (-10.5));
      if (distanceToArtwork > 11) {
        document.getElementById('title').textContent = 'Bạn đang đứng quá xa bức tranh';
        document.getElementById('meta').textContent = 'Tiến lại gần bức tranh rồi nhấp chuột để chuyển tác phẩm.';
        return;
      }
      transitioning = true;
      const next = (currentIndex + 1) % artList.length;
      const oldPos = artworkGroup.position.clone();
      new TWEEN.Tween(artworkGroup.scale)
        .to({x:0.05,y:0.05,z:0.05},350)
        .easing(TWEEN.Easing.Quadratic.In)
        .onComplete(() => {
          currentIndex = next;
          makeArtwork(currentIndex);
          artworkGroup.scale.set(0.05,0.05,0.05);
          new TWEEN.Tween(artworkGroup.scale)
            .to({x:1,y:1,z:1},500)
            .easing(TWEEN.Easing.Back.Out)
            .onComplete(() => { transitioning = false; });
          artworkGroup.position.copy(oldPos);
        }).start();
    });

    window.addEventListener('keydown', e => {
      if (e.target && ['INPUT','TEXTAREA'].includes(e.target.tagName)) return;
      if (e.code in keys) keys[e.code] = true;
      if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code)) e.preventDefault();
    });
    window.addEventListener('keyup', e => { if (e.code in keys) keys[e.code] = false; });
    window.addEventListener('blur', () => { Object.keys(keys).forEach(k=>keys[k]=false); });

    function animate() {
      requestAnimationFrame(animate);
      TWEEN.update();
      controls.update();
      const forward = new THREE.Vector3();
      camera.getWorldDirection(forward);
      forward.y = 0; forward.normalize();
      const right = new THREE.Vector3().crossVectors(forward, camera.up).normalize().negate();
      if (keys.KeyW || keys.ArrowUp) { camera.position.addScaledVector(forward,speed); controls.target.addScaledVector(forward,speed); }
      if (keys.KeyS || keys.ArrowDown) { camera.position.addScaledVector(forward,-speed); controls.target.addScaledVector(forward,-speed); }
      if (keys.KeyA || keys.ArrowLeft) { camera.position.addScaledVector(right,-speed); controls.target.addScaledVector(right,-speed); }
      if (keys.KeyD || keys.ArrowRight) { camera.position.addScaledVector(right,speed); controls.target.addScaledVector(right,speed); }
      camera.position.x = THREE.MathUtils.clamp(camera.position.x,-15,15);
      camera.position.z = THREE.MathUtils.clamp(camera.position.z,-11.2,16);
      controls.target.x = THREE.MathUtils.clamp(controls.target.x,-15,15);
      controls.target.z = THREE.MathUtils.clamp(controls.target.z,-12,15);
      renderer.render(scene,camera);
    }
    animate();

    function resize() {
      const width = root.clientWidth, height = root.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width,height);
    }
    window.addEventListener('resize',resize);
  } catch (err) {
    console.error(err);
    showError(err && err.message ? err.message : String(err));
  }
})();
</script>
</body>
</html>
"""

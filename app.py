import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit hiển thị tràn viền tối đa cho game 3D
st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D - 7 Kiệt Tác",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Game Nhập Vai: Bảo Tàng 3D & 7 Kiệt Tác Nghệ Thuật")
st.write("🕹️ **Cách điều khiển:** Bấm nút **BẬT NHẠC** trước để kích hoạt bài **Great Little Things**. Sử dụng các phím **W, A, S, D (hoặc Mũi tên)** để di chuyển bước đi tự do trong phòng. **Nhấn giữ chuột trái và kéo** để xoay hướng nhìn camera 360 độ nhìn ngắm không gian. Tiến lại gần tranh và **Bấm chuột trái** (không kéo) để kích hoạt hiệu ứng rã hạt màu trong 5 giây!")

# Mã HTML + JavaScript dựng toàn bộ cơ chế game di chuyển tự do, hạt màu toán học lập thể và nhạc nền
game_walkthrough_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #020204; font-family: sans-serif; }
        canvas { width: 100vw; height: 650px; display: block; }
        #info-overlay {
            position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%);
            color: #ffffff; text-align: center; background: rgba(5, 5, 8, 0.85);
            padding: 15px 35px; border-radius: 12px; border: 1px solid #d4af37;
            pointer-events: none; max-width: 80%; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
            transition: opacity 0.5s; opacity: 1;
        }
        h2 { margin: 0 0 5px 0; color: #d4af37; font-size: 22px; }
        p { margin: 0; font-size: 14px; color: #ddd; }
        #music-btn {
            position: absolute; top: 15px; left: 15px;
            background: #d4af37; color: #000; border: none; padding: 10px 20px;
            font-weight: bold; border-radius: 5px; cursor: pointer; z-index: 10;
            box-shadow: 0 0 10px rgba(212,175,55,0.4);
        }
    </style>
    <script src="https://cloudflare.com"></script>
    <script src="https://jsdelivr.net"></script>
    <script src="https://cloudflare.com"></script>
</head>
<body>

    <button id="music-btn" onclick="toggleMusic()">🎵 BẬT NHẠC NỀN</button>

    <audio id="bg-music" loop>
        <source src="https://catbox.moe" type="audio/mpeg">
    </audio>

    <div id="info-overlay">
        <h2 id="art-title">Không gian nghệ thuật 3D đã sẵn sàng!</h2>
        <p id="art-meta">Sử dụng các phím W, A, S, D để bước đi tiến vào phòng triển lãm</p>
    </div>

    <script>
        const audio = document.getElementById('bg-music');
        audio.volume = 0.5;

        function toggleMusic() {
            if (audio.paused) {
                audio.play();
                document.getElementById('music-btn').innerText = "⏸️ TẠM DỪNG NHẠC";
            } else {
                audio.pause();
                document.getElementById('music-btn').innerText = "🎵 BẬT NHẠC NỀN";
            }
        }

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020204);
        scene.fog = new THREE.FogExp2(0x020204, 0.03);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / 650, 0.1, 1000);
        camera.position.set(0, 2, 14);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, 650);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.enablePan = false; 
        controls.maxPolarAngle = Math.PI / 2 - 0.02; 
        controls.minDistance = 1;
        controls.maxDistance = 25;

        let keys = { KeyW: false, KeyS: false, KeyA: false, KeyD: false, ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false };
        window.addEventListener('keydown', (e) => { if (e.code in keys) keys[e.code] = true; });
        window.addEventListener('keyup', (e) => { if (e.code in keys) keys[e.code] = false; });

        const floorGeo = new THREE.PlaneGeometry(60, 60);
        const floorMat = new THREE.MeshBasicMaterial({ color: 0x110906 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2; scene.add(floor);

        const wallGeo = new THREE.PlaneGeometry(40, 12);
        const wallMat = new THREE.MeshBasicMaterial({ color: 0x05060a });
        const wall = new THREE.Mesh(wallGeo, wallMat);
        wall.position.set(0, 6, -2.1); scene.add(wall);

        const artList = [
            { id: "starry", title: "Đêm đầy sao (The Starry Night - Biến tấu)", meta: "Vincent van Gogh | Các hạt sáng xanh dương và vàng cuộn xoáy lộng lẫy", type: "swirl", r: 0.1, g: 0.3, b: 0.8 },
            { id: "monalisa", title: "Mona Lisa", meta: "Leonardo da Vinci | Tông màu nâu vàng cổ điển Phục Hưng huyền bí", type: "portrait", r: 0.4, g: 0.3, b: 0.1 },
            { id: "lady", title: "Lady with an Ermine", meta: "Leonardo da Vinci | Sắc tối quyền lực kết hợp các dải hạt trắng thanh cao", type: "stripe", r: 0.5, g: 0.4, b: 0.3 },
            { id: "scream", title: "Skrik (The Scream - Tiếng thét)", meta: "Edvard Munch | Sắc cam rực lửa và đỏ lo âu cuộn sóng", type: "wave", r: 0.9, g: 0.3, b: 0.1 },
            { id: "lastsupper", title: "The Last Supper (Bữa ăn tối cuối cùng)", meta: "Leonardo da Vinci | Kiệt tác đặt tại chiều sâu xa nhất và mang tông màu tối trang nghiêm", type: "supper", r: 0.2, g: 0.15, b: 0.1 },
            { id: "pearlear", title: "Girl with a Pearl Earring (Thiếu nữ đeo hoa tai ngọc trai)", meta: "Johannes Vermeer | Sắc ngọc bảo phối dải lụa vàng óng ánh", type: "portrait", r: 0.1, g: 0.5, b: 0.6 },
            { id: "adameve", title: "Adam and Eve (Adam và Eva)", meta: "Albrecht Dürer | Tranh khắc tỷ lệ cơ thể hoàn mỹ với tông xám trắng cổ kính", type: "stripe", r: 0.4, g: 0.4, b: 0.4 }
        ];

        let currentArtIndex = 0;
        const particleCount = 45000;
        let particleSystem;
        let isTransitioning = false;
        const w = 250; const h = 180;

        function generateProceduralColors(type, baseR, baseG, baseB, i) {
            const pX = i % w; const pY = Math.floor(i / h);
            const nX = pX / w; const nY = pY / h;
            let r = baseR, g = baseG, b = baseB;

            if (type === "swirl") {
                let angle = Math.atan2(nY - 0.5, nX - 0.5);
                let dist = Math.sqrt((nX - 0.5)**2 + (nY - 0.5)**2);
                r += Math.sin(angle * 5 + dist * 10) * 0.2;
                g += Math.cos(angle * 3) * 0.2;
                b += Math.sin(dist * 5) * 0.2;
            } else if (type === "wave") {
                r += Math.sin(nX * 12) * 0.25;
                g += Math.cos(nY * 10) * 0.15;
            } else if (type === "portrait") {
                let dist = Math.sqrt((nX - 0.5)**2 + (nY - 0.4)**2);
                if (dist < 0.23) { r += 0.25; g += 0.15; b -= 0.1; } 
            } else if (type === "stripe") {
                let factor = (pX % 12 === 0 || pY % 12 === 0) ? 0.3 : -0.05;
                r += factor; g += factor; b += factor;
            }
            return { r: Math.max(0, Math.min(1, r)), g: Math.max(0, Math.min(1, g)), b: Math.max(0, Math.min(1, b)) };
        }

        function initParticles() {
            const geometry = new THREE.BufferGeometry();
            const pPositions = new Float32Array(particleCount * 3);
            const pColors = new Float32Array(particleCount * 3);
            const firstArt = artList[0];

            for (let i = 0; i < particleCount; i++) {
                const pX = i % w; const pY = Math.floor(i / w);
                pPositions[i * 3] = ((pX / w) - 0.5) * 6.5;
                pPositions[i * 3 + 1] = (-(pY / h) + 0.5) * 4.5 + 4.5;
                pPositions[i * 3 + 2] = -1.9;

                let c = generateProceduralColors(firstArt.type, firstArt.r, firstArt.g, firstArt.b, i);
                pColors[i * 3] = c.r; pColors[i * 3 + 1] = c.g; pColors[i * 3 + 2] = c.b;
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(pColors, 3));

            const canvasP = document.createElement('canvas'); canvasP.width = 16; canvasP.height = 16;
            const g = canvasP.getContext('2d').createRadialGradient(8, 8, 0, 8, 8, 8);
            g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(1, 'rgba(255,255,255,0)');
            canvasP.getContext('2d').fillStyle = g; canvasP.getContext('2d').fillRect(0,0,16,16);

            const material = new THREE.PointsMaterial({
                size: 0.045, map: new THREE.CanvasTexture(canvasP),
                vertexColors: true, transparent: true, opacity: 0.95,
                blending: THREE.AdditiveBlending, depthWrite: false
            });

            particleSystem = new THREE.Points(geometry, material);
            scene.add(particleSystem);
            
            document.getElementById('art-title').innerText = artList[0].title;
            document.getElementById('art-meta').innerText = artList[0].meta;
        }

        initParticles();

        function triggerParticleTransition() {
            if (isTransitioning || !particleSystem) return;
            isTransitioning = true;

            const nextIndex = (currentArtIndex + 1) % artList.length;
            const nextArt = artList[nextIndex];
            document.getElementById('info-overlay').style.opacity = 0;

            const posAttr = particleSystem.geometry.attributes.position;

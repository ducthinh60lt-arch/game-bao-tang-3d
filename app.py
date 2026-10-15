import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit hiển thị tràn viền tối đa cho game
st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D - 7 Kiệt Tác",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Game Nhập Vai: Bảo Tàng 3D & 7 Kiệt Tác Nghệ Thuật")
st.write("🕹️ **Cách điều khiển:** Bấm nút **BẬT NHẠC** trước để kích hoạt bài **Great Little Things**. Sử dụng **W, A, S, D (hoặc Mũi tên)** để di chuyển bước đi. **Nhấn giữ chuột trái và kéo** để xoay hướng nhìn 360 độ. Tiến lại gần tranh và **Bấm chuột trái** (không kéo) để rã hạt màu!")

# Mã HTML + JavaScript dựng toàn bộ cơ chế game di chuyển tự do, hạt màu và nhạc nền
game_walkthrough_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #020204; font-family: sans-serif; }
        canvas { width: 100vw; height: 650px; display: block; }
        
        /* Bảng hiển thị thông tin tác phẩm nghệ thuật */
        #info-overlay {
            position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%);
            color: #ffffff; text-align: center; background: rgba(5, 5, 8, 0.85);
            padding: 15px 35px; border-radius: 12px; border: 1px solid #d4af37;
            pointer-events: none; max-width: 80%; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
            transition: opacity 0.5s; opacity: 1;
        }
        h2 { margin: 0 0 5px 0; color: #d4af37; font-size: 22px; }
        p { margin: 0; font-size: 14px; color: #ddd; }
        
        /* Nút bật tắt nhạc riêng biệt ở góc trên */
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
        <h2 id="art-title">Đang quét tia sáng dựng tranh...</h2>
        <p id="art-meta">Sử dụng các phím W, A, S, D để rảo bước chân tham quan sảnh bảo tàng</p>
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

        // 1. Cấu hình không gian phòng sảnh bảo tàng
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020204);
        scene.fog = new THREE.FogExp2(0x020204, 0.03);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / 650, 0.1, 1000);
        // Điểm xuất phát của nhân vật
        camera.position.set(0, 2, 14);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, 650);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        // 2. Sử dụng OrbitControls tùy biến góc nhìn kéo thả chuột mượt mà chạy tốt online
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.enablePan = false; // Khóa di chuột tịnh tiến, chỉ giữ xoay đầu nhìn xung quanh
        controls.maxPolarAngle = Math.PI / 2 - 0.02; // Không cho camera chúc xuống sàn
        controls.minDistance = 1;
        controls.maxDistance = 25;

        // Trạng thái các phím bước đi W, A, S, D
        let keys = { KeyW: false, KeyS: false, KeyA: false, KeyD: false, ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false };

        window.addEventListener('keydown', (e) => { if (e.code in keys) keys[e.code] = true; });
        window.addEventListener('keyup', (e) => { if (e.code in keys) keys[e.code] = false; });

        // 3. Dựng cấu trúc Sàn nhà sảnh bảo tàng
        const floorGeo = new THREE.PlaneGeometry(50, 50);
        const floorMat = new THREE.MeshBasicMaterial({ color: 0x110906 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2; scene.add(floor);

        // 4. Danh sách bộ sưu tập triển lãm 7 kiệt tác
        const artList = [
            { id: "starry", title: "Đêm đầy sao (The Starry Night - Biến tấu)", meta: "Vincent van Gogh | Bản phối cánh đồng hoa rực rỡ", url: "https://unsplash.com" },
            { id: "monalisa", title: "Mona Lisa", meta: "Leonardo da Vinci | Kiệt tác thời Phục Hưng gốc", url: "https://wikimedia.org" },
            { id: "lady", title: "Lady with an Ermine", meta: "Leonardo da Vinci | Chi tiết bảo tàng Krakow", url: "https://wikimedia.org" },
            { id: "scream", title: "Skrik (The Scream)", meta: "Edvard Munch | Kiệt tác trường phái biểu hiện", url: "https://wikimedia.org" },
            { id: "lastsupper", title: "The Last Supper (Bữa ăn tối cuối cùng) - Ẩn Hiện Thâm Sâu", meta: "Leonardo da Vinci | Đặt tại không gian xa nhất & mang sắc độ tối huyền bí", url: "https://wikimedia.org" },
{ id: "pearlear", title: "Girl with a Pearl Earring (Thiếu nữ đeo hoa tai ngọc trai)", meta: "Johannes Vermeer | Kiệt tác hội họa Hà Lan thế kỷ 17", url: "https://wikimedia.org" },
            { id: "adameve", title: "Adam and Eve (Adam và Eva)", meta: "Albrecht Dürer | Tác phẩm tranh khắc Phục Hưng năm 1507", url: "https://wikimedia.org" }
        ];

        let currentArtIndex = 0;
        const particleCount = 55000;
        let particleSystem;
        let artDataCache = [];
        let isTransitioning = false;
        const w = 250; const h = 220;

        let loadedCount = 0;
        artList.forEach((art, index) => {
            const img = new Image(); img.crossOrigin = "Anonymous"; img.src = art.url;
            img.onload = function() {
                const canvas = document.createElement('canvas'); canvas.width = w; canvas.height = h;
                const canvasCtx = canvas.getContext('2d'); canvasCtx.drawImage(img, 0, 0, w, h);
                artDataCache[index] = canvasCtx.getImageData(0, 0, w, h).data;
                if (++loadedCount === artList.length) initParticles();
            };
        });

        function initParticles() {
            const geometry = new THREE.BufferGeometry();
            const pPositions = new Float32Array(particleCount * 3);
            const pColors = new Float32Array(particleCount * 3);
            const initialData = artDataCache[0];

            for (let i = 0; i < particleCount; i++) {
                const pX = i % w; const pY = Math.floor(i / w);
                const idx = (pY * w + pX) * 4;

                pPositions[i * 3] = ((pX / w) - 0.5) * 6.5;
                pPositions[i * 3 + 1] = (-(pY / h) + 0.5) * 4.5 + 4.5;
                pPositions[i * 3 + 2] = -1.9;

                pColors[i * 3] = initialData[idx] / 255;
                pColors[i * 3 + 1] = initialData[idx + 1] / 255;
                pColors[i * 3 + 2] = initialData[idx + 2] / 255;
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
// 5. Thuật toán rã hạt khuyết loang lổ đồng bộ 5 giây
function triggerParticleTransition() {
if (isTransitioning || !particleSystem) return;
isTransitioning = true;
const nextIndex = (currentArtIndex + 1) % artList.length;
const nextArt = artList[nextIndex];
const newData = artDataCache[nextIndex];
document.getElementById('info-overlay').style.opacity = 0;
const posAttr = particleSystem.geometry.attributes.position;
const colorAttr = particleSystem.geometry.attributes.color;
let indices = Array.from({length: particleCount}, (_, i) => i);
for (let i = indices.length - 1; i > 0; i--) {
const j = Math.floor(Math.random() * (i + 1));
[indices[i], indices[j]] = [indices[j], indices[i]];
}
const totalDuration = 5000;
indices.forEach((i, order) => {
const delay = (order / particleCount) * 1500;
const travelTime = totalDuration - delay;
const pX = i % w; const pY = Math.floor(i / w);
const nIdx = (pY * w + pX) * 4;
let targetZ = -1.9;
let scaleFactor = 6.5;
if (nextArt.id === "lastsupper") {
targetZ = -6.0; // Đẩy xa The Last Supper vào cuối sảnh tối
scaleFactor = 11.0;
}
const targetX = ((pX / w) - 0.5) * scaleFactor;
const targetY = (-(pY / h) + 0.5) * 4.5 + 4.5;
const burstX = posAttr.array[i * 3] + (Math.random() - 0.5) * 5.5;
const burstY = posAttr.array[i * 3 + 1] + (Math.random() - 0.5) * 5.5;
const burstZ = posAttr.array[i * 3 + 2] + (Math.random()) * 8.5;
new TWEEN.Tween(posAttr.array)
.to({ [i * 3]: burstX, [i * 3 + 1]: burstY, [i * 3 + 2]: burstZ }, travelTime * 0.3)
.easing(TWEEN.Easing.Quadratic.Out)
.delay(delay)
.chain(
new TWEEN.Tween(posAttr.array)
.to({ [i * 3]: targetX, [i * 3 + 1]: targetY, [i * 3 + 2]: targetZ }, travelTime * 0.7)
.easing(TWEEN.Easing.Cubic.InOut)
)
.start();
let brightnessDivider = (nextArt.id === "lastsupper") ? 2.5 : 1.0; // Giảm độ sáng làm tối The Last Supper
new TWEEN.Tween(colorAttr.array)
.to({
[i * 3]: (newData[nIdx] / 255) / brightnessDivider,
[i * 3 + 1]: (newData[nIdx + 1] / 255) / brightnessDivider,
[i * 3 + 2]: (newData[nIdx + 2] / 255) / brightnessDivider
}, travelTime)
.delay(delay)
.start();
});
setTimeout(() => {
currentArtIndex = nextIndex;
document.getElementById('art-title').innerText = artList[currentArtIndex].title;
document.getElementById('art-meta').innerText = artList[currentArtIndex].meta;
document.getElementById('info-overlay').style.opacity = 1;
isTransitioning = false;
}, totalDuration);
}
// Click chuột trái gọn gàng không kéo rê để chuyển tranh (kiểm tra khoảng cách với tranh)
let isMouseDown = false, mouseMoveDistance = 0;
window.addEventListener('mousedown', () => { isMouseDown = true; mouseMoveDistance = 0; });
window.addEventListener('mousemove', () => { if (isMouseDown) mouseMoveDistance++; });
window.addEventListener('mouseup', () => {
isMouseDown = false;
if (mouseMoveDistance < 5) { // Người dùng nhấp chuột chứ không phải đang kéo xoay camera
let currentArt = artList[currentArtIndex];
let maxClickDistance = (currentArt.id === "lastsupper") ? 14 : 9;
// Đo cự ly camera tới tâm tranh
if (camera.position.z < maxClickDistance) {
triggerParticleTransition();
} else {
document.getElementById('art-title').innerText = "⚠️ Bạn đang đứng quá xa bức tranh!";
document.getElementById('art-meta').innerText = "Hãy giữ phím W để tiến bộ chân lại gần bức tường treo tranh hơn.";
}
}
});
// 6. Vòng lặp chuyển động Game Loop cập nhật bước chân W, A, S, D
const speed = 0.15;
function animate() {
requestAnimationFrame(animate);
TWEEN.update();
controls.update();
// Tính toán hướng vector camera để di chuyển nhân vật tiến lùi theo đúng hướng đang nhìn
const forward = new THREE.Vector3();
camera.getWorldDirection(forward);
forward.y = 0; forward.normalize(); // Chỉ đi trên mặt phẳng sàn
const right = new THREE.Vector3();
right.crossVectors(forward, camera.up).normalize().negate();
if (keys.KeyW || keys.ArrowUp) { camera.position.addScaledVector(forward, speed); controls.target.addScaledVector(forward, speed); }
if (keys.KeyS || keys.ArrowDown) { camera.position.addScaledVector(forward, -speed); controls.target.addScaledVector(forward, -speed); }
if (keys.KeyA || keys.ArrowLeft) { camera.position.addScaledVector(right, -speed); controls.target.addScaledVector(right, -speed); }
if (keys.KeyD || keys.ArrowRight) { camera.position.addScaledVector(right, speed); controls.target.addScaledVector(right, speed); }
// Giới hạn biên bản đồ bảo tàng không cho đi lạc khỏi sảnh
let frontWallLimit = (artList[currentArtIndex].id === "lastsupper") ? -4.5 : -0.5;
if (camera.position.z < frontWallLimit) { camera.position.z = frontWallLimit; controls.target.z = frontWallLimit - 5; }
if (camera.position.z > 20) { camera.position.z = 20; controls.target.z = 15; }
if (camera.position.x < -15) { camera.position.x = -15; controls.target.x = -15; }
if (camera.position.x > 15) { camera.position.x = 15; controls.target.x = 15; }
if (particleSystem) {
particleSystem.geometry.attributes.position.needsUpdate = true;
particleSystem.geometry.attributes.color.needsUpdate = true;
}
renderer.render(scene, camera);
}
animate();
window.addEventListener('resize', () => {
camera.aspect = window.innerWidth / 650; camera.updateProjectionMatrix();
renderer.setSize(window.innerWidth, 650);
});



"""

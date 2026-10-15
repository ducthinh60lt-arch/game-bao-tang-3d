import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit hiển thị tràn viền tối đa cho game
st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D - 7 Kiệt Tác",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Game Nhập Vai: Bảo Tàng 3D & 7 Kiệt Tác Nghệ Thuật")
st.write("🕹️ **Cách điều khiển:** Bấm chuột vào màn hình game để khóa chuột và kích hoạt nhạc nền **Great Little Things**. Dùng **W, A, S, D (hoặc Mũi tên)** để bước đi. Đến gần tranh và **Bấm chuột trái** để rã hạt màu!")

# Mã HTML + JavaScript dựng toàn bộ cơ chế game di chuyển, hạt màu và nhạc nền phát tự động
game_walkthrough_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #030305; font-family: sans-serif; }
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
        
        /* Tâm ngắm giữa màn hình bắn tia tương tác */
        #crosshair {
            position: absolute; top: 50%; left: 50%;
            width: 8px; height: 8px; background: rgba(255,255,255,0.5);
            border-radius: 50%; transform: translate(-50%, -50%);
            pointer-events: none; border: 1px solid rgba(0,0,0,0.5);
        }
        
        /* Hướng dẫn khi chưa khóa chuột */
        #blocker {
            position: absolute; width: 100vw; height: 650px;
            background-color: rgba(0,0,0,0.85); display: flex;
            justify-content: center; align-items: center;
            color: #ffffff; font-size: 20px; cursor: pointer; text-align: center;
        }
    </style>
    <script src="https://cloudflare.com"></script>
    <script src="https://jsdelivr.net"></script>
    <script src="https://cloudflare.com"></script>
</head>
<body>

    <!-- Khởi tạo thẻ phát nhạc ngầm Audio HTML5 bài Great Little Things (Loop vô tận) -->
    <audio id="bg-music" loop>
        <source src="https://catbox.moe" type="audio/mpeg">
    </audio>

    <div id="blocker">
        <div>
            <span style="font-size: 40px; color: #d4af37; font-weight: bold; text-shadow: 0 0 10px rgba(212,175,55,0.5);">🏛️ BẤM VÀO ĐÂY ĐỂ BẬT NHẠC & CHƠI GAME</span><br/><br/>
🎵 Nhạc nền đang chờ kích hoạt: <b>Great Little Things (HauXenz)</b><br/><br/>
            Sử dụng phím di chuyển: <b>W, A, S, D</b> hoặc <b>Mũi tên</b><br/>
            Nhìn xung quanh: <b>Di chuyển chuột</b><br/>
            Số lượng tác phẩm triển lãm: <b>7 Kiệt tác hội họa</b><br/>
            Nhấn phím <b>ESC</b> để tạm dừng/thoát khóa chuột.
        </div>
    </div>
    
    <div id="crosshair"></div>

    <div id="info-overlay">
        <h2 id="art-title">Hãy bước đi từ cửa vào để tham quan sảnh tranh...</h2>
        <p id="art-meta">Giữ phím W để tiến bộ lại gần khung tranh treo chính diện</p>
    </div>

    <script>
        const audio = document.getElementById('bg-music');
        audio.volume = 0.5;

        // 1. Cấu hình không gian phòng sảnh bảo tàng
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020203);
        scene.fog = new THREE.FogExp2(0x020203, 0.03); // Tăng sương mù tạo chiều sâu tối cho sảnh xa

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / 650, 0.1, 1000);
        camera.position.set(0, 2, 14);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, 650);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        // 2. Cài đặt hệ thống điều khiển góc nhìn thứ nhất (First Person PointerLock)
        const controls = new THREE.PointerLockControls(camera, document.body);
        const blocker = document.getElementById('blocker');
        
        blocker.addEventListener('click', () => { 
            controls.lock(); 
            audio.play().catch(err => console.log("Trình duyệt chặn âm thanh:", err));
        });
        
        controls.addEventListener('lock', () => { blocker.style.display = 'none'; });
        controls.addEventListener('unlock', () => { blocker.style.display = 'flex'; });

        let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
        const velocity = new THREE.Vector3();
        const direction = new THREE.Vector3();

        document.addEventListener('keydown', (e) => {
            switch (e.code) {
                case 'KeyW': case 'ArrowUp': moveForward = true; break;
                case 'KeyS': case 'ArrowDown': moveBackward = true; break;
                case 'KeyA': case 'ArrowLeft': moveLeft = true; break;
                case 'KeyD': case 'ArrowRight': moveRight = true; break;
            }
        });

        document.addEventListener('keyup', (e) => {
            switch (e.code) {
                case 'KeyW': case 'ArrowUp': moveForward = false; break;
                case 'KeyS': case 'ArrowDown': moveBackward = false; break;
case 'KeyA': case 'ArrowLeft': moveLeft = false; break;
                case 'KeyD': case 'ArrowRight': moveRight = false; break;
            }
        });

        // 3. Dựng Sàn và Tường bảo tàng bao quanh nhân vật
        const floorGeo = new THREE.PlaneGeometry(40, 40);
        const floorMat = new THREE.MeshBasicMaterial({ color: 0x110a08 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2; scene.add(floor);

        const wallGeo = new THREE.PlaneGeometry(40, 10);
        const wallMat = new THREE.MeshBasicMaterial({ color: 0x06080c });
        const frontWall = new THREE.Mesh(wallGeo, wallMat); frontWall.position.set(0, 5, -2); scene.add(frontWall);

        // 4. Khởi tạo danh sách 7 bức tranh độ phân giải cao
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
            const initialData = artDataCache;
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
// 5. Cơ chế chuyển tranh rã hạt mang màu khuyết dần đồng bộ trong đúng 5 giây
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
// TÍNH TOÁN VỊ TRÍ ĐÍCH Z: Nếu là The Last Supper thì đẩy lùi sâu hẳn về z = -6.0 (Xa nhất)
let targetZ = -1.9;
let scaleFactor = 6.5; // Kích thước bề ngang thông thường
if (nextArt.id === "lastsupper") {
targetZ = -6.0;      // Đẩy lùi sâu vào bóng tối sảnh bảo tàng
scaleFactor = 11.0;  // Tăng kích thước bao phủ để đứng từ xa vẫn nhìn thấy quy mô khổ rộng
}
const targetX = ((pX / w) - 0.5) * scaleFactor;
const targetY = (-(pY / h) + 0.5) * 4.5 + 4.5;
// Tạo hiệu ứng hạt nổ tung sượt qua tầm mắt camera người chơi
const burstX = posAttr.array[i * 3] + (Math.random() - 0.5) * 6.0;
const burstY = posAttr.array[i * 3 + 1] + (Math.random() - 0.5) * 6.0;
const burstZ = posAttr.array[i * 3 + 2] + (Math.random()) * 9.0;
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
// TÍNH TOÁN ĐỘ TÔ/TỐI MÀU SẮC: Nếu là The Last Supper thì giảm độ sáng hạt đi 2.5 lần để tạo không khí u tối
let brightnessDivider = 1.0;
if (nextArt.id === "lastsupper") {
brightnessDivider = 2.5; // Tô tối bức tranh thâm sâu thầm lặng
}
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
// Click chuột kiểm tra cự ly gần tường để kích hoạt rã hạt
document.addEventListener('click', () => {
if (controls.isLocked) {
// Tùy biến cự ly kích hoạt: Nếu đang ở bức tranh xa (Last Supper), cho phép đứng xa (z < 12) vẫn bấm kích hoạt được
let currentArt = artList[currentArtIndex];
let maxClickDistance = (currentArt.id === "lastsupper") ? 12 : 8;
if (camera.position.z < maxClickDistance) {
triggerParticleTransition();
} else {
document.getElementById('art-title').innerText = "⚠️ Bạn đang đứng quá xa tầm tương tác!";
document.getElementById('art-meta').innerText = "Hãy sử dụng phím W tiến lại gần sảnh tranh để thực hiện quét hạt ánh sáng.";
}
}
});
// 6. Vòng lặp Game Loop cập nhật bước chân nhân vật
const clock = new THREE.Clock();
function animate() {
requestAnimationFrame(animate);
TWEEN.update();
if (controls.isLocked) {
const delta = clock.getDelta();
velocity.x -= velocity.x * 10.0 * delta;
velocity.z -= velocity.z * 10.0 * delta;
direction.z = Number(moveForward) - Number(moveBackward);
direction.x = Number(moveRight) - Number(moveLeft);
direction.normalize();
if (moveForward || moveBackward) velocity.z -= direction.z * 40.0 * delta;
if (moveLeft || moveRight) velocity.x -= direction.x * 40.0 * delta;
controls.moveRight(-velocity.x * delta);
controls.moveForward(-velocity.z * delta);
// Giới hạn biên phòng sảnh bảo tàng (Mở rộng chặn tường lùi sâu z = -4.5 cho bức tranh xa)
let fontWallLimit = (artList[currentArtIndex].id === "lastsupper") ? -4.5 : -0.5;
if (camera.position.z < fontWallLimit) camera.position.z = fontWallLimit;
if (camera.position.z > 18) camera.position.z = 18;
if (camera.position.x < -15) camera.position.x = -15;
if (camera.position.x > 15) camera.position.x = 15;
}
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

import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit hiển thị tràn viền tối đa cho game
st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D - Great Little Things",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Game Nhập Vai: Bảo Tàng 3D & Nhạc Nền Great Little Things")
st.write("🕹️ **Cách điều khiển:** Bấm chuột vào màn hình game để khóa chuột và kích hoạt nhạc nền. Dùng **W, A, S, D (hoặc Mũi tên)** để bước đi. Đến gần tranh và **Bấm chuột trái** để rã hạt màu trong 5 giây!")

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
        <source src="https://soundhelix.com" type="audio/mpeg">
    </audio>

    <div id="blocker">
        <div>
            <span style="font-size: 40px; color: #d4af37; font-weight: bold; text-shadow: 0 0 10px rgba(212,175,55,0.5);">🏛️ BẤM VÀO ĐÂY ĐỂ BẬT NHẠC & CHƠI GAME</span><br/><br/>
🎵 Nhạc nền đang chờ kích hoạt: <b>Great Little Things (HauXenz)</b><br/><br/>
            Sử dụng phím di chuyển: <b>W, A, S, D</b> hoặc <b>Mũi tên</b><br/>
            Nhìn xung quanh: <b>Di chuyển chuột</b><br/>
            Nhấn phím <b>ESC</b> để tạm dừng/thoát khóa chuột.
        </div>
    </div>
    
    <div id="crosshair"></div>

    <div id="info-overlay">
        <h2 id="art-title">Hãy bước đi từ cửa vào để tham quan sảnh tranh...</h2>
        <p id="art-meta">Giữ phím W để tiến bộ lại gần khung tranh treo chính diện</p>
    </div>

    <script>
        // Thiết lập link Audio thực tế bài Great Little Things từ kho lưu trữ đám mây
        const audio = document.getElementById('bg-music');
        // Nạp luồng âm thanh gốc bản Khèn Bè của HauXenz
        audio.src = "https://catbox.moe"; 
        audio.volume = 0.5; // Đặt âm lượng 50% vừa vặn lofi nghe chill

        // 1. Cấu hình không gian phòng sảnh bảo tàng
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x040406);
        scene.fog = new THREE.FogExp2(0x040406, 0.025);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / 650, 0.1, 1000);
        camera.position.set(0, 2, 14); // Nhân vật đứng ở sảnh cửa ra vào

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, 650);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        // 2. Cài đặt hệ thống điều khiển góc nhìn thứ nhất (First Person PointerLock)
        const controls = new THREE.PointerLockControls(camera, document.body);
        const blocker = document.getElementById('blocker');
        
        blocker.addEventListener('click', () => { 
            controls.lock(); 
            // Kích hoạt phát nhạc ngay khi người dùng click tương tác màn hình
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
        const floorMat = new THREE.MeshBasicMaterial({ color: 0x150e0a });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2; scene.add(floor);

        const wallGeo = new THREE.PlaneGeometry(40, 10);
        const wallMat = new THREE.MeshBasicMaterial({ color: 0x0c0e14 });
        const frontWall = new THREE.Mesh(wallGeo, wallMat); frontWall.position.set(0, 5, -2); scene.add(frontWall);

        // 4. Khởi tạo cấu trúc 45.000 Hạt màu rã tranh đồng bộ 5s
        const artList = [
            { title: "Đêm đầy sao (The Starry Night - Biến tấu)", meta: "Vincent van Gogh | Bản phối cánh đồng hoa rực rỡ", url: "https://unsplash.com" },
            { title: "Mona Lisa", meta: "Leonardo da Vinci | Kiệt tác thời Phục Hưng gốc", url: "https://wikimedia.org" },
            { title: "Lady with an Ermine", meta: "Leonardo da Vinci | Chi tiết bảo tàng Krakow", url: "https://wikimedia.org" },
            { title: "Skrik (The Scream)", meta: "Edvard Munch | Kiệt tác trường phái biểu hiện", url: "https://wikimedia.org" }
        ];

        let currentArtIndex = 0;
        const particleCount = 45000;
        let particleSystem;
        let artDataCache = [];
        let isTransitioning = false;
        const w = 240; const h = 187;

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

                pPositions[i * 3] = ((pX / w) - 0.5) * 6;
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
size: 0.05, map: new THREE.CanvasTexture(canvasP),
vertexColors: true, transparent: true, opacity: 0.95,
blending: THREE.AdditiveBlending, depthWrite: false
});
particleSystem = new THREE.Points(geometry, material);
scene.add(particleSystem);
// Cập nhật text ban đầu sau khi tải xong hạt
document.getElementById('art-title').innerText = artList[0].title;
document.getElementById('art-meta').innerText = artList[0].meta;
}
// 5. Cơ chế chuyển tranh rã hạt khuyết dần mang màu trong đúng 5 giây
function triggerParticleTransition() {
if (isTransitioning || !particleSystem) return;
isTransitioning = true;
const nextIndex = (currentArtIndex + 1) % artList.length;
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
const targetX = ((pX / w) - 0.5) * 6;
const targetY = (-(pY / h) + 0.5) * 4.5 + 4.5;
const targetZ = -1.9;
// Các hạt màu nổ tung bắn xéo góc tỏa ra sảnh rồi hút về tranh mới
const burstX = posAttr.array[i * 3] + (Math.random() - 0.5) * 5.5;
const burstY = posAttr.array[i * 3 + 1] + (Math.random() - 0.5) * 5.5;
const burstZ = posAttr.array[i * 3 + 2] + (Math.random()) * 8.5; // Chảy tràn ra không gian sảnh
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
new TWEEN.Tween(colorAttr.array)
.to({
[i * 3]: newData[nIdx] / 255,
[i * 3 + 1]: newData[nIdx + 1] / 255,
[i * 3 + 2]: newData[nIdx + 2] / 255
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
if (camera.position.z < 8) {
triggerParticleTransition();
} else {
document.getElementById('art-title').innerText = "⚠️ Bạn đang đứng quá xa bức tranh!";
document.getElementById('art-meta').innerText = "Hãy giữ phím W để rảo bước chân lại sát bức tường treo tranh hơn.";
}
}
});
// 6. Vòng lặp Game Loop cập nhật chuyển động đi bộ của người chơi
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
// Giới hạn biên không gian bảo tàng tránh rơi khỏi map
if (camera.position.z < -0.5) camera.position.z = -0.5;
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

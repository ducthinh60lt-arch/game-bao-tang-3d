import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit hiển thị tràn viền
st.set_page_config(
    page_title="Viện Bảo Tàng 3D Thần Kỳ",
    page_icon="✨",
    layout="wide"
)

st.title("🏛️ Phòng Triển Lãm Ảo 3D & Hiệu Ứng Hạt Thần Kỳ")
st.write("👉 **Hãy bấm chuột vào vùng không gian hoặc bức tranh:** Các hạt ánh sáng sẽ bung tỏa toàn màn hình rồi tụ lại thành kiệt tác nghệ thuật tiếp theo!")

# Mã HTML + JavaScript xử lý hiệu ứng hạt và Camera 360
particle_gallery_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #050508; font-family: sans-serif; }
        canvas { width: 100vw; height: 600px; display: block; }
        #info-overlay {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            color: #ffffff; text-align: center; background: rgba(0,0,0,0.7);
            padding: 15px 30px; border-radius: 10px; border: 1px solid #d4af37;
            pointer-events: none; max-width: 80%; transition: all 0.5s;
        }
        h2 { margin: 0 0 5px 0; color: #d4af37; font-size: 20px; }
        p { margin: 0; font-size: 14px; color: #ccc; }
    </style>
    <script src="https://cloudflare.com"></script>
    <script src="https://jsdelivr.net"></script>
    <script src="https://cloudflare.com"></script>
</head>
<body>

    <div id="info-overlay">
        <h2 id="art-title">Đang khởi tạo không gian nghệ thuật...</h2>
        <p id="art-meta"></p>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050508, 0.03);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / 600, 0.1, 1000);
        camera.position.set(0, 0, 8);

        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        renderer.setSize(window.innerWidth, 600);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.5;

        const artList = [
            {
                title: "Đêm đầy sao (Biến tấu cánh đồng hoa)",
                meta: "Vincent van Gogh | Sáng tạo lại dựa trên nguyên bản 1889",
                url: "https://unsplash.com"
            },
            {
                title: "Mona Lisa",
                meta: "Leonardo da Vinci | Khoảng năm 1503",
                url: "https://wikimedia.org"
            },
            {
                title: "Lady with an Ermine",
                meta: "Leonardo da Vinci | Khoảng năm 1489–1490",
                url: "https://wikimedia.org"
            },
            {
                title: "Skrik (The Scream)",
                meta: "Edvard Munch | Năm 1893",
                url: "https://wikimedia.org"
            }
        ];

        let currentArtIndex = 0;
        const particleCount = 15000;
        let particleSystem;
        let positions = new Float32Array(particleCount * 3);
        let colors = new Float32Array(particleCount * 3);

        const geometry = new THREE.BufferGeometry();
        
        const canvasParticle = document.createElement('canvas');
        canvasParticle.width = 16; canvasParticle.height = 16;
        const ctx = canvasParticle.getContext('2d');
        const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
        gradient.addColorStop(0, 'rgba(255,255,255,1)');
        gradient.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = gradient; ctx.fillRect(0, 0, 16, 16);
        const pTexture = new THREE.CanvasTexture(canvasParticle);

        const material = new THREE.PointsMaterial({
            size: 0.06,
            map: pTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.85,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
            colors[i * 3] = 1; colors[i * 3 + 1] = 1; colors[i * 3 + 2] = 1;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        particleSystem = new THREE.Points(geometry, material);
        scene.add(particleSystem);

        function loadArtToParticles(index) {
            const art = artList[index];
            document.getElementById('art-title').innerText = art.title;
            document.getElementById('art-meta').innerText = art.meta;

            const img = new Image();
            img.crossOrigin = "Anonymous";
            img.src = art.url;
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const w = 120; const h = 90;
                canvas.width = w; canvas.height = h;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, w, h);
                const imgData = ctx.getImageData(0, 0, w, h).data;

                const posAttribute = particleSystem.geometry.attributes.position;
                const colorAttribute = particleSystem.geometry.attributes.color;

                for (let i = 0; i < particleCount; i++) {
                    const pX = Math.floor(Math.random() * w);
                    const pY = Math.floor(Math.random() * h);
                    const pixelIndex = (pY * w + pX) * 4;

                    const targetX = ((pX / w) - 0.5) * 5;
                    const targetY = (-(pY / h) + 0.5) * 3.8;
                    const targetZ = 0;

                    let explodeX = posAttribute.array[i * 3] + (Math.random() - 0.5) * 8;
                    let explodeY = posAttribute.array[i * 3 + 1] + (Math.random() - 0.5) * 8;
                    let explodeZ = posAttribute.array[i * 3 + 2] + (Math.random() - 0.5) * 8;

                    new TWEEN.Tween(posAttribute.array)
                        .to({ [i * 3]: explodeX, [i * 3 + 1]: explodeY, [i * 3 + 2]: explodeZ }, 600)
                        .easing(TWEEN.Easing.Quadratic.Out)
                        .chain(
                            new TWEEN.Tween(posAttribute.array)
                                .to({ [i * 3]: targetX, [i * 3 + 1]: targetY, [i * 3 + 2]: targetZ }, 2200)
                                .easing(TWEEN.Easing.Cubic.InOut)
                        )
                        .start();

                    new TWEEN.Tween(colorAttribute.array)
                        .to({
                            [i * 3]: imgData[pixelIndex] / 255,
                            [i * 3 + 1]: imgData[pixelIndex + 1] / 255,
                            [i * 3 + 2]: imgData[pixelIndex + 2] / 255
                        }, 2000)
                        .start();
                }
            };
        }

        setTimeout(() => { loadArtToParticles(0); }, 500);

        window.addEventListener('click', () => {
            currentArtIndex = (currentArtIndex + 1) % artList.length;
            loadArtToParticles(currentArtIndex);
        });

        function animate(time) {
            requestAnimationFrame(animate);
            TWEEN.update();
            controls.update();
            
            if(particleSystem) {
                particleSystem.geometry.attributes.position.needsUpdate = true;
                particleSystem.geometry.attributes.color.needsUpdate = true;
            }
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / 600;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 600);
        });
    </script>
</body>
</html>
"""

components.html(particle_gallery_code, height=620, scrolling=False)
st.divider()
st.info("💡 **Mẹo trải nghiệm:** Bạn có thể nhấn giữ chuột trái kéo để điều khiển camera xoay vòng quanh luồng hạt 3D từ mọi góc độ khi tranh đang thành hình.")

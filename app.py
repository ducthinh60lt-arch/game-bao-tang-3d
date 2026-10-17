  // Không khóa chuột ngay trên nút; người chơi nhấp vào khung game để bắt đầu nhìn.
});

renderer.domElement.addEventListener("click", () => {
  if (started && !controls.isLocked) controls.lock();
});

controls.addEventListener("lock", () => {
  if (started) say("Dùng WASD để đi, rê chuột để nhìn. Nhắm vào tranh và nhấp chuột khi đứng gần.");
});
controls.addEventListener("unlock", () => {
  if (started) say("Chuột đã được thả. Nhấp vào khung game để tiếp tục.");
});

const raycaster = new THREE.Raycaster();
raycaster.params.Points.threshold = .3;
renderer.domElement.addEventListener("pointerdown", event => {
  if (!started || !controls.isLocked || transitionRunning) return;
  // Nhấp chuột khi đang điều khiển góc nhìn không phải lúc nào cũng tạo click,
  // nên việc chọn tranh dùng ray từ tâm màn hình trong sự kiện click.
});
renderer.domElement.addEventListener("click", event => {
  if (!started || !controls.isLocked || transitionRunning) return;
  raycaster.setFromCamera(new THREE.Vector2(0,0), camera);
  const hits = raycaster.intersectObjects(paintings.map(p=>p.particles), false);
  if (!hits.length) return;
  const painting = paintings.find(p=>p.particles===hits[0].object);
  if (!painting) return;

  const distance = camera.position.distanceTo(painting.group.position);
  if (distance > 10.5) {
    say("Đứng xa quá! Hãy tiến lại gần bức tranh rồi nhấp.");
    return;
  }

  transitionRunning = true;
  updateInfo(painting.data);
  say("Bức tranh đang rã thành những hạt màu...");
  const arr = painting.geometry.attributes.position.array;
  const target = painting.targets;
  const start = arr.slice();
  const t0 = performance.now();
  const duration = 2600;

  function dissolve(now) {
    const t = Math.min(1,(now-t0)/duration);
    const spread = Math.sin(Math.PI*t);
    for (let i=0; i<painting.count; i++) {
      const j=i*3;
      const phase=i*12.9898;
      arr[j] = THREE.MathUtils.lerp(start[j],target[j],t) + Math.sin(phase+t*18)*spread*.9;
      arr[j+1] = THREE.MathUtils.lerp(start[j+1],target[j+1],t) + Math.cos(phase*.7+t*16)*spread*.9;
      arr[j+2] = THREE.MathUtils.lerp(start[j+2],target[j+2],t) + Math.sin(phase*.3+t*20)*spread*2.2;
    }
    painting.geometry.attributes.position.needsUpdate = true;
    painting.particles.material.opacity = .25 + .75*Math.abs(2*t-1);
    if (t<1) requestAnimationFrame(dissolve);
    else {
      arr.set(target);
      painting.geometry.attributes.position.needsUpdate = true;
      painting.particles.material.opacity=1;
      transitionRunning=false;
      say("Các hạt màu đã tái hợp thành tác phẩm. Hãy tiếp tục khám phá!");
    }
  }
  requestAnimationFrame(dissolve);
});

document.getElementById("music").addEventListener("click", async () => {
  const audio = document.getElementById("audio");
  const button = document.getElementById("music");
  try {
    if (audio.paused) {
      await audio.play();
      button.textContent = "Ⅱ TẠM DỪNG NHẠC";
    } else {
      audio.pause();
      button.textContent = "♫ BẬT NHẠC";
    }
  } catch (err) {
    say("Chưa phát được nhạc: hãy thay URL mẫu bằng đường dẫn trực tiếp tới file MP3 hợp pháp.");
  }
});

const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), .05);
  if (started && controls.isLocked && !transitionRunning) {
    const speed=5.0*dt;
    if (keys.KeyW || keys.ArrowUp) controls.moveForward(speed);
    if (keys.KeyS || keys.ArrowDown) controls.moveForward(-speed);
    if (keys.KeyA || keys.ArrowLeft) controls.moveRight(-speed);
    if (keys.KeyD || keys.ArrowRight) controls.moveRight(speed);
    const p=controls.getObject().position;
    p.x=THREE.MathUtils.clamp(p.x,-14.5,14.5);
    p.z=THREE.MathUtils.clamp(p.z,-24.5,20.5);
    p.y=1.7;
  }
  renderer.render(scene,camera);
}
animate();
</script>
</div>
</body>
</html>
"""

components.html(game_html, height=735, scrolling=False)


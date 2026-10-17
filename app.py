import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hành Trình Bảo Tàng 3D",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Hành Trình Bảo Tàng 3D")
st.write(
    "Bắt đầu từ cổng bảo tàng, khám phá 7 kiệt tác nghệ thuật. "
    "Đến gần một bức tranh và nhấp chuột để khám phá thế giới hạt màu."
)

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
html,body {
    margin:0; padding:0; overflow:hidden;
    background:#080706; font-family:Arial,sans-serif;
}
#game { width:100%; height:720px; display:block; }
#intro {
    position:absolute; inset:0; z-index:10;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    text-align:center; color:#f8e8bd;
    background:radial-gradient(ellipse,#49351e,#080706 75%);
}
#intro h1 { font-size:clamp(28px,5vw,54px); margin:10px; }
#intro p { max-width:600px; line-height:1.8; padding:0 20px; }
button {
    background:#d7b46a; color:#1a1208;
    border:1px solid #f6e1a6; padding:13px 23px;
    border-radius:5px; font-weight:bold; cursor:pointer;
}
#hud {
    position:absolute; top:12px; left:12px; z-index:5;
    color:#f8e8bd; background:#100d0bd9;
    padding:12px 16px; border:1px solid #8f713d;
    border-radius:6px; max-width:330px;
}
#hud h3 { margin:0 0 7px; color:#e5c276; }
#hint { font-size:13px; line-height:1.6; }
#music {
    position:absolute; top:12px; right:12px; z-index:6;
}
#crosshair {
    position:absolute; left:50%; top:50%; z-index:4;
    transform:translate(-50%,-50%);
    color:#ffe4a0; pointer-events:none; font-size:22px;
}
#toast {
    position:absolute; bottom:20px; left:50%;
    transform:translateX(-50%); z-index:5;
    color:#ffe7b0; background:#100d0be8;
    border:1px solid #8f713d; border-radius:6px;
    padding:12px 18px; text-align:center;
}
</style>
</head>
<body>

<div id="intro">
    <div style="font-size:54px">🏛️</div>
    <h1>HÀNH TRÌNH BẢO TÀNG</h1>
    <p>
      Bước qua cánh cổng, tiến vào không gian nghệ thuật,
      khám phá bảy kiệt tác vượt thời gian.
      Mỗi bức tranh đều ẩn chứa một thế giới màu sắc đang chờ được đánh thức.
    </p>
    <button id="start">BẮT ĐẦU HÀNH TRÌNH</button>
    <p style="font-size:12px;color:#c6b18c">
      W A S D: di chuyển · Chuột: xoay nhìn · Nhấp tranh: khám phá
    </p>
</div>

<div id="hud">
  <h3 id="title">Bảo tàng nghệ thuật</h3>
  <div id="description">Chào mừng đến với hành trình.</div>
  <p id="hint">WASD để đi · Chuột để nhìn · Nhấp tranh khi ở gần</p>
</div>

<button id="music">♫ BẬT NHẠC</button>
<div id="crosshair">+</div>
<div id="toast">Hãy tiến vào bảo tàng và khám phá các kiệt tác.</div>

<audio id="audio" loop preload="none">
  <source src="YOUR_DIRECT_GREAT_LITTLE_THINGS_AUDIO_URL.mp3"
          type="audio/mpeg">
</audio>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { PointerLockControls } from
'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/PointerLockControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x090807);
scene.fog = new THREE.Fog(0x090807, 24, 65);

const camera = new THREE.PerspectiveCamera(
    70, innerWidth / 720, 0.1, 150
);
camera.position.set(0, 1.7, 19);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,720);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
document.body.appendChild(renderer.domElement);
renderer.domElement.id = "game";

scene.add(new THREE.HemisphereLight(0xffe7c2,0x25202b,2.0));

const controls = new PointerLockControls(camera,renderer.domElement);
scene.add(controls.getObject());

const mats = {
  wall: new THREE.MeshStandardMaterial({
    color:0x24201c, roughness:0.9
  }),
  floor: new THREE.MeshStandardMaterial({
    color:0x39291e, roughness:0.5
  }),
  gold: new THREE.MeshStandardMaterial({
    color:0xb79550, metalness:0.65, roughness:0.3
  }),
  dark: new THREE.MeshStandardMaterial({
    color:0x100e0c, roughness:0.8
  })
};

function box(w,h,d,mat,x,y,z) {
  const m = new THREE.Mesh(
    new THREE.BoxGeometry(w,h,d),mat
  );
  m.position.set(x,y,z);
  scene.add(m);
  return m;
}

// Phòng triển lãm rộng, cổng vào ở phía z dương.
box(32,0.5,48,mats.floor,0,-0.3,-2);
box(32,12,0.6,mats.wall,0,5.7,-26);
box(0.6,12,48,mats.wall,-16,5.7,-2);
box(0.6,12,48,mats.wall,16,5.7,-2);

// Cổng vào ở chính giữa tường phía trước.
box(5,0.5,0.8,mats.gold,0,4.3,21.5);
box(0.45,4.5,0.8,mats.gold,-2.5,2.0,21.5);
box(0.45,4.5,0.8,mats.gold,2.5,2.0,21.5);

// Khung tranh và ánh sáng.
const artList = [
  {
    title:"Đêm đầy sao — The Starry Night",
    artist:"Vincent van Gogh",
    description:"Bầu trời đêm xoáy cuộn trong sắc xanh và vàng.",
    color:[0.15,0.45,1], type:0, x:-10, z:5, scale:1
  },
  {
    title:"Mona Lisa",
    artist:"Leonardo da Vinci",
    description:"Nụ cười bí ẩn của hội họa Phục Hưng.",
    color:[0.62,0.38,0.12], type:1, x:0, z:5, scale:1
  },
  {
    title:"Thiếu nữ đeo hoa tai ngọc trai",
    artist:"Johannes Vermeer",
    description:"Ánh sáng dịu và sắc xanh sâu lắng.",
    color:[0.12,0.55,0.7], type:2, x:10, z:5, scale:1
  },
  {
    title:"Tiếng thét — The Scream",
    artist:"Edvard Munch",
    description:"Những dải cam đỏ cuộn thành cảm xúc mãnh liệt.",
    color:[1,0.2,0.06], type:3, x:-10, z:-8, scale:1
  },
  {
    title:"Lady with an Ermine",
    artist:"Leonardo da Vinci",
    description:"Chân dung cổ điển với tông nâu và trắng.",
    color:[0.65,0.48,0.3], type:4, x:10, z:-8, scale:1
  },
  {
    title:"Adam và Eva",
    artist:"Albrecht Dürer",
    description:"Tác phẩm khắc cổ điển với tương phản mạnh.",
    color:[0.68,0.65,0.55], type:5, x:-10, z:-19, scale:1
  },
  {
    title:"Bữa tối cuối cùng — The Last Supper",
    artist:"Leonardo da Vinci",
    description:"Kiệt tác hội họa tường: bố cục rộng lớn, ánh sáng vàng trang nghiêm.",
    color:[0.8,0.48,0.2], type:6, x:0, z:-25.45, scale:2.35
  }
];

const artworks = [];
const artWidth = 4.4;
const artHeight = 2.8;

function proceduralColor(type,u,v,base) {
  let r=base[0],g=base[1],b=base[2];
  const wave=Math.sin(u*22+Math.sin(v*11)*2);
  const bands=Math.sin((u+v)*35);
  if(type===0) {
    r+=0.15*Math.sin(u*35+v*7);
    g+=0.18*Math.sin(v*24+u*12);
    b+=0.24*Math.cos(u*20-v*17);
  } else if(type===1) {
    const face=Math.exp(-((u-.52)**2+(v-.45)**2)*24);
    r+=face*.24; g+=face*.14; b+=face*.06;
  } else if(type===2) {
    r+=wave*.08; g+=bands*.09; b+=.1;
  } else if(type===3) {
    r+=.2*Math.sin(v*25); g+=.12*Math.cos(u*15);
  } else if(type===4) {
    const stripe=Math.sin(u*60)>0 ? .12:-.08;
    r+=stripe;g+=stripe;b+=stripe;
  } else if(type===5) {
    const stripe=Math.sin(u*75+v*15)*.1;
    r+=stripe;g+=stripe;b+=stripe;
  } else {
    r+=.13*Math.sin(u*27+v*8);
    g+=.12*Math.cos(v*23);
    b+=.07*Math.sin(u*17-v*12);
  }
  return [
    THREE.MathUtils.clamp(r,0,1),
    THREE.MathUtils.clamp(g,0,1),
    THREE.MathUtils.clamp(b,0,1)
  ];
}

for(const a of artList) {
  const s=a.scale;
  const group=new THREE.Group();
  group.position.set(a.x,3.8,a.z);
  scene.add(group);

  // Khung lớn riêng cho Bữa tối cuối cùng.
  const w=artWidth*s, h=artHeight*s;
  const frameMat=new THREE.MeshStandardMaterial({
    color:a.type===6?0xd7b15d:0x9b783d,
    metalness:.6,roughness:.32,
    emissive:a.type===6?0x4c2706:0x100a02,
    emissiveIntensity:a.type===6?.35:.1
  });

  const frameDepth=.24;
  const frameSize=.18*s;
  const panel=new THREE.Mesh(
    new THREE.PlaneGeometry(w,h),
    new THREE.MeshBasicMaterial({color:0x17110b})
  );
  panel.position.z=.02;
  group.add(panel);

  const top=box(w+frameSize*2,frameSize,frameDepth,
    frameMat,0,0,0);
  top.position.set(0,h/2+frameSize/2,0);
  group.add(top); top.position.set(0,h/2+frameSize/2,0);

  const bottom=new THREE.Mesh(
    new THREE.BoxGeometry(w+frameSize*2,frameSize,frameDepth),
    frameMat
  );
  bottom.position.set(0,-h/2-frameSize/2,0);group.add(bottom);

  for(const side of [-1,1]) {
    const rail=new THREE.Mesh(
      new THREE.BoxGeometry(frameSize,h,frameDepth),frameMat
    );
    rail.position.set(side*(w/2+frameSize/2),0,0);
    group.add(rail);
  }

  // Hạt màu tạo nên mặt tranh.
  const count=a.type===6?26000:9000;
  const positions=new Float32Array(count*3);
  const colors=new Float32Array(count*3);
  const targets=new Float32Array(count*3);

  for(let i=0;i<count;i++) {
    const u=Math.random(),v=Math.random();
    const c=proceduralColor(a.type,u,v,a.color);
    const j=i*3;
    targets[j]=(u-.5)*w;
    targets[j+1]=(v-.5)*h;
    targets[j+2]=.12;
    positions[j]=targets[j]+(Math.random()-.5)*.15;
    positions[j+1]=targets[j+1]+(Math.random()-.5)*.15;
    positions[j+2]=.12;
    colors[j]=c[0];colors[j+1]=c[1];colors[j+2]=c[2];
  }

  const geo=new THREE.BufferGeometry();
  geo.setAttribute("position",new THREE.BufferAttribute(positions,3));
  geo.setAttribute("color",new THREE.BufferAttribute(colors,3));
  geo.userData.targets=targets;

  const particleMat=new THREE.PointsMaterial({
    size:a.type===6?.045:.035,
    vertexColors:true,transparent:true,opacity:1,
    depthWrite:false,blending:THREE.AdditiveBlending
  });
  const particles=new THREE.Points(geo,particleMat);
  group.add(particles);

  const light=new THREE.PointLight(
    a.type===6?0xffd18a:0xffe0ad,
    a.type===6?100:22,
    a.type===6?24:10
  );
  light.position.set(a.x,5.8,a.z+1.7);
  scene.add(light);

  artworks.push({
    data:a,group,particles,geo,colors,targets,
    count,active:false,transition:0
  });
}

// Tường đầu phòng: Bữa tối cuối cùng nằm đối diện cổng vào.
const endGlow=new THREE.PointLight(0xffb94f,40,25);
endGlow.position.set(0,5,-20);
scene.add(endGlow);

// Tranh chọn bằng tia từ camera.
const raycaster=new THREE.Raycaster();
raycaster.params.Points.threshold=.28;
let selected=null;
let inMuseum=false;
let busy=false;

function setMessage(t) {
  document.getElementById("toast").textContent=t;
}

function updateHUD(a) {
  document.getElementById("title").textContent=a.title;
  document.getElementById("description").textContent=
    a.artist+" — "+a.description;
}

function distanceToArtwork(a) {
  return camera.position.distanceTo(a.group.position);
}

function clickArtwork() {
  if(!inMuseum || busy) return;

  raycaster.setFromCamera(new THREE.Vector2(0,0),camera);
  const hits=raycaster.intersectObjects(
    artworks.map(a=>a.particles),false
  );

  if(!hits.length) {
    setMessage("Hãy ngắm thẳng vào vùng tranh rồi nhấp chuột.");
    return;
  }

  const item=artworks.find(a=>a.particles===hits[0].object);
  if(!item || distanceToArtwork(item)>10) {
    setMessage("Hãy tiến lại gần bức tranh trước khi khám phá.");
    return;
  }

  selected=item;
  updateHUD(item.data);
  busy=true;
  setMessage("Bức tranh đang tan thành hàng nghìn hạt màu...");

  const p=item.geo.attributes.position.array;
  const targets=item.targets;
  const starts=p.slice();
  const count=item.count;
  const duration=3000;
  const start=performance.now();

  function animateDissolve(now) {
    const t=Math.min(1,(now-start)/duration);
    for(let i=0;i<count;i++) {
      const j=i*3;
      const burst=1+Math.random()*.03;
      const fade=1-t;
      p[j]=starts[j]+Math.sin(i*1.7+t*7)*.8*t;
      p[j+1]=starts[j+1]+Math.cos(i*.7+t*8)*.8*t;
      p[j+2]=starts[j+2]+Math.sin(i*.3+t*9)*2*t;
      if(t>.72) {
        const k=(t-.72)/.28;
        p[j]=THREE.MathUtils.lerp(p[j],targets[j]+
          (Math.random()-.5)*.5,k*.1);
        p[j+1]=THREE.MathUtils.lerp(p[j+1],targets[j+1]+
          (Math.random()-.5)*.5,k*.1);
        p[j+2]=THREE.MathUtils.lerp(p[j+2],targets[j+2],k*.1);
      }
    }
    item.geo.attributes.position.needsUpdate=true;
    item.particles.material.opacity=fade;
    if(t<1) requestAnimationFrame(animateDissolve);
    else {
      item.particles.material.opacity=1;
      item.geo.attributes.position.array.set(targets);
      item.geo.attributes.position.needsUpdate=true;
      busy=false;
      setMessage("Những hạt màu đã tái hợp thành hình ảnh của tác phẩm.");
    }
  }
  requestAnimationFrame(animateDissolve);
}

renderer.domElement.addEventListener("click",clickArtwork);

const keys={};
addEventListener("keydown",e=>{keys[e.code]=true;});
addEventListener("keyup",e=>{keys[e.code]=false;});

document.getElementById("start").addEventListener("click",()=>{
  document.getElementById("intro").style.display="none";
  inMuseum=true;
  camera.position.set(0,1.7,19);
  controls.lock();
  setMessage("Chào mừng! Hãy bước vào phòng triển lãm.");
});

controls.addEventListener("unlock",()=>{
  if(inMuseum) setMessage("Nhấp vào màn hình game để tiếp tục tham quan.");
});

document.getElementById("music").addEventListener("click",async()=>{
  const audio=document.getElementById("audio");
  try {
    if(audio.paused) {
      await audio.play();
      document.getElementById("music").textContent="Ⅱ TẠM DỪNG NHẠC";
    } else {
      audio.pause();
      document.getElementById("music").textContent="♫ BẬT NHẠC";
    }
  } catch(e) {
    setMessage("Hãy thay đường dẫn âm thanh bằng URL trực tiếp tới file MP3.");
  }
});

const clock=new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),.05);

  if(controls.isLocked && inMuseum && !busy) {
    const speed=5*dt;
    if(keys.KeyW||keys.ArrowUp) controls.moveForward(speed);
    if(keys.KeyS||keys.ArrowDown) controls.moveForward(-speed);
    if(keys.KeyA||keys.ArrowLeft) controls.moveRight(-speed);
    if(keys.KeyD||keys.ArrowRight) controls.moveRight(speed);

    const p=controls.getObject().position;
    p.x=THREE.MathUtils.clamp(p.x,-14.5,14.5);
    p.z=THREE.MathUtils.clamp(p.z,-24.5,20);
    p.y=1.7;
  }

  // Tác phẩm cuối cùng luôn nổi bật nhất ở bức tường đối diện cổng.
  renderer.render(scene,camera);
}
animate();

addEventListener("resize",()=>{
  camera.aspect=innerWidth/720;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,720);
});
</script>
</body>
</html>
"""

components.html(game_html, height=730, scrolling=False)

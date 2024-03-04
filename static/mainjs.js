import * as datGui from "https://cdn.skypack.dev/dat.gui@0.7.7";
// document.addEventListener('DOMContentLoaded', function () {
//     anime({
//         targets: '.animated-footer',
//         translateY: [50, 0],
//         opacity: [0, 1],
//         easing: 'easeInOutQuad',
//         duration: 1000,
//         delay: 500
//     });
// });
document.addEventListener('DOMContentLoaded', function () {
    const misNumberInput = document.getElementById('misNumber');
    const branchInput = document.getElementById('Branch');
    const yearInput = document.getElementById('year');

    misNumberInput.addEventListener('input', function () {
        const misNumber = parseInt(this.value);
        if (misNumber.toString().startsWith('612203')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>C.S</h3>';
        }
        
        else if (misNumber.toString().startsWith('612201')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>CIVIL</h3>';
        } 
        else if (misNumber.toString().startsWith('612201')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>CIVIL</h3>';
        } 
        else if (misNumber.toString().startsWith('612201')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>CIVIL</h3>';
        } 
        else if (misNumber.toString().startsWith('612201')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>CIVIL</h3>';
        } 
        else if (misNumber.toString().startsWith('612201')) {
            yearInput.innerHTML = '<h3>YEAR:</h3><h3>S.Y</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3><h3>CIVIL</h3>';
        } else {
            yearInput.innerHTML = '<h3>YEAR:</h3>';
            branchInput.innerHTML = '<h3>BRANCH:</h3>';
        }
    });
});

const state = {
  fps: 60,
  color: "#0f0",
  charset: "0123456789ABCDEF",
  size: 10
};

const gui = new datGui.GUI();
const fpsCtrl = gui.add(state, "fps").min(1).max(120).step(1);
gui.addColor(state, "color");
gui.add(state, "charset");
const sizeCtrl = gui.add(state, "size").min(1).max(120).step(1);

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let w, h, p;
const resize = () => {
  w = canvas.width = innerWidth;
  h = canvas.height = innerHeight;

  p = Array(Math.ceil(w / state.size)).fill(0);
};
window.addEventListener("resize", resize);
sizeCtrl.onFinishChange((s) => resize())
resize();

const random = (items) => items[Math.floor(Math.random() * items.length)];

const draw = () => {
  ctx.fillStyle = "rgba(0,0,0,.05)";
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = state.color;

  ctx.font = state.size + 'px sans-serif'
  for (let i = 0; i < p.length; i++) {
    let v = p[i];
    ctx.fillText(random(state.charset), i * state.size, v);
    p[i] = v >= h || v >= 10000 * Math.random() ? 0 : v + state.size;
  }
};

let interval = setInterval(draw, 1000 / state.fps);
fpsCtrl.onFinishChange((fps) => {
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(draw, 1000 / fps);
});

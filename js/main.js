import * as THREE from 'three';
import { loadPointCloud } from './pointcloud.js';
import { initMenu } from './menu.js';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let pointsMesh = null;

const camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 6;
camera.position.x = 2;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const bgColor = getComputedStyle(document.documentElement).getPropertyValue('--color-bg').trim();
renderer.setClearColor(bgColor);
document.body.appendChild(renderer.domElement);

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    if (pointsMesh && pointsMesh.material.uniforms) {
        pointsMesh.material.uniforms.uPixelRatio.value = Math.min(window.devicePixelRatio, 2);
    }
});

const scene = new THREE.Scene();

const mouse = { x: 0, y: 0 };

if (!reducedMotion) {
    window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = (e.clientY / window.innerHeight) * 2 - 1;
    });
}

loadPointCloud(scene, (pts) => {
    pointsMesh = pts;
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('is-hidden');
        setTimeout(() => loading.remove(), 600);
    }
});

function animate() {
    requestAnimationFrame(animate);

    if (!reducedMotion) {
        const targetX = mouse.x * 1.5;
        const targetY = mouse.y * 1.5;
        camera.position.x += (targetX - camera.position.x) * 0.02;
        camera.position.y += (targetY - camera.position.y) * 0.02;
    }
    camera.lookAt(0, 0, 0);

    if (pointsMesh) {
        if (!reducedMotion) {
            pointsMesh.rotation.y += 0.0002;
        }
        if (!reducedMotion && pointsMesh.material.uniforms) {
            pointsMesh.material.uniforms.uTime.value = performance.now() * 0.001;
        }
    }

    renderer.render(scene, camera);
}

animate();

initMenu();

const sections = document.querySelectorAll('.section');
const sectionObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });

sections.forEach(section => {
    sectionObserver.observe(section);
});

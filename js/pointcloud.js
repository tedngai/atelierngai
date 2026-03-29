import * as THREE from 'three';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';

const vertexShader = `
  uniform float uTime;
  uniform float uPixelRatio;

  attribute float aRandom;

  varying vec3 vColor;

  void main() {
    vec3 pos = position;

    float isJitter = step(0.7, aRandom);
    float speed = 0.8 + aRandom * 2.0;
    float amp = 0.02 + aRandom * 0.04;
    float phase = aRandom * 100.0;

    pos.x += sin(uTime * speed + phase) * amp * isJitter;
    pos.y += cos(uTime * speed * 0.8 + phase + 1.0) * amp * isJitter;
    pos.z += sin(uTime * speed * 0.6 + phase + 2.0) * amp * 0.5 * isJitter;

    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPosition;
    gl_PointSize = (0.4 * uPixelRatio) * (100.0 / -mvPosition.z);

    vColor = color;
  }
`;

const fragmentShader = `
  varying vec3 vColor;

  void main() {
    float dist = length(gl_PointCoord - vec2(0.5));
    if (dist > 0.5) discard;
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
    gl_FragColor = vec4(vColor, alpha * 0.85);
  }
`;

function seededRandom(seed) {
  let s = seed;
  return function () {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

export function loadPointCloud(scene, onLoaded) {
  const loader = new PLYLoader();

  loader.load(
    'assets/pointcloud/scene.ply',
    function (geometry) {
      const count = geometry.attributes.position.count;
      const aRandom = new Float32Array(count);
      const rand = seededRandom(42);

      for (let i = 0; i < count; i++) {
        aRandom[i] = rand();
      }

      geometry.setAttribute('aRandom', new THREE.BufferAttribute(aRandom, 1));

      const material = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms: {
          uTime: { value: 0 },
          uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
        },
        vertexColors: true,
        transparent: true,
        depthWrite: false
      });

      const points = new THREE.Points(geometry, material);
      scene.add(points);

      if (onLoaded) {
        onLoaded(points);
      }
    },
    function (xhr) {
      if (xhr.total > 0) {
        const percent = (xhr.loaded / xhr.total * 100).toFixed(1);
        console.log('Point cloud loading: ' + percent + '%');
      }
    },
    function (error) {
      console.error('Error loading point cloud:', error);
    }
  );
}

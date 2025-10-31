// SpiralOS HUD Loader v1.0
// Author: Carey G. Butler / Heurist GmbH
// License: MIT
// Description: Visualizes the SpiralOS Epistemic Lattice (E*, µ, CI, ℍ, ℋ, M, Ψ)
// using Three.js + YAML schema graph

import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.159.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.159.0/examples/jsm/controls/OrbitControls.js';
import * as jsyaml from 'https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/+esm';

async function loadHUD() {
  // Load hud.json
  const hudUrl = './hud.json';
  const hudResponse = await fetch(hudUrl);
  const hud = await hudResponse.json();

  // Load schema-graph.yaml
  const schemaResp = await fetch('../schema/schema-graph.yaml');
  const schemaText = await schemaResp.text();
  const schema = jsyaml.load(schemaText);

  // Setup Three.js scene
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 8;

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Lighting
  const light = new THREE.PointLight(0x4ec8ff, 1.2, 100);
  light.position.set(10, 10, 10);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x222222));

  // Geometry and Materials
  const sphereGeom = new THREE.SphereGeometry(0.2, 32, 32);
  const lineMat = new THREE.LineBasicMaterial({ color: 0x555555 });
  const nodes = {};

  // Create nodes
  schema.nodes.forEach((node, i) => {
    const mat = new THREE.MeshPhongMaterial({ color: 0x4ec8ff });
    const mesh = new THREE.Mesh(sphereGeom, mat);

    const angle = i * 0.9;
    mesh.position.set(Math.cos(angle) * 3, Math.sin(angle) * 3, Math.sin(i * 0.5) * 2);
    mesh.userData = node;

    scene.add(mesh);
    nodes[node.id] = mesh;
  });

  // Connect relations
  schema.relations.forEach((rel) => {
    const from = nodes[rel.from];
    const to = nodes[rel.to];
    if (from && to) {
      const geometry = new THREE.BufferGeometry().setFromPoints([from.position, to.position]);
      const line = new THREE.Line(geometry, lineMat);
      scene.add(line);
    }
  });

  // Tooltip overlay
  const tooltip = document.createElement('div');
  tooltip.style.position = 'absolute';
  tooltip.style.color = '#4ec8ff';
  tooltip.style.fontFamily = 'monospace';
  tooltip.style.fontSize = '14px';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.padding = '4px 8px';
  tooltip.style.border = '1px solid #4ec8ff';
  tooltip.style.background = 'rgba(0,0,0,0.75)';
  tooltip.style.borderRadius = '6px';
  tooltip.style.display = 'none';
  document.body.appendChild(tooltip);

  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  }
  window.addEventListener('mousemove', onMouseMove, false);

  // Spiral Time animation
  function animate(time) {
    requestAnimationFrame(animate);

    scene.rotation.y = Math.sin(time * 0.0002) * 0.3;
    controls.update();

    // Hover detection
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(Object.values(nodes));

    if (intersects.length > 0) {
      const obj = intersects[0].object;
      tooltip.innerHTML = `<b>${obj.userData.name}</b><br>${obj.userData.description}`;
      tooltip.style.left = event.clientX + 12 + 'px';
      tooltip.style.top = event.clientY + 12 + 'px';
      tooltip.style.display = 'block';
      obj.material.color.set(0xffffff);
    } else {
      tooltip.style.display = 'none';
      Object.values(nodes).forEach((n) => n.material.color.set(0x4ec8ff));
    }

    renderer.render(scene, camera);
  }

  animate();
}

window.addEventListener('load', loadHUD);

# Personal Site PRD — 3D Point Cloud Biography

## Overview

A personal portfolio/biography website inspired by the immersive design of [Penderecki's Garden](https://pendereckisgarden.pl/en/the-maestros-manor). Uses a personal 3D point cloud as the animated background, with clean HTML/CSS overlays for biographical content. Simpler, no audio/map/multi-chapter 3D navigation — just a beautiful 3D backdrop with scrollable content sections and a hamburger menu overlay.

**Tech Stack:** Three.js + vanilla HTML/CSS/JS (no frameworks)

---

## Phase 1 — Project Scaffolding & 3D Foundation

**Goal:** Get the point cloud rendering in a browser window.

### Tasks
- [ ] **1.1** Initialize project structure
  ```
  /ted_personal_site
  ├── index.html
  ├── css/
  │   └── styles.css
  ├── js/
  │   ├── main.js          # Entry point, init Three.js scene
  │   ├── pointcloud.js    # Load & render point cloud
  │   └── menu.js          # Hamburger menu logic
  ├── assets/
  │   └── pointcloud/      # .ply / .pcd / .xyz files
  └── PRD.md
  ```
- [ ] **1.2** Set up Three.js scene (camera, renderer, resize handler)
- [ ] **1.3** Load point cloud file into scene (use Three.js PCDLoader or PLYLoader)
- [ ] **1.4** Add slow auto-rotation to the point cloud (subtle, constant drift)
- [ ] **1.5** Add mouse/trackpad parallax — camera follows cursor slightly
- [ ] **1.6** Set background color + point material styling (size, color, opacity)

### Deliverable
A blank page with a rotating, interactive 3D point cloud filling the viewport.

---

## Phase 2 — Typography & Color System

**Goal:** Establish the visual language pulled from the reference site's aesthetic.

### Design Tokens
| Token                | Value              | Notes                              |
|----------------------|--------------------|------------------------------------|
| `--color-bg`         | `#372933`          | Deep burgundy/plum                 |
| `--color-text`       | `#e2d8ca`          | Warm beige                         |
| `--color-accent`     | `#ad9795`          | Dusty rose for highlights          |
| `--color-subtle`     | `rgba(226,216,202,0.4)` | Muted text for secondary info |
| `--font-sans`        | Inter or similar geometric sans | UI, body text        |
| `--font-serif`       | Playfair Display or similar serif | Headings            |

### Tasks
- [ ] **2.1** Import Google Fonts (Inter + Playfair Display as free alternatives)
- [ ] **2.2** Define CSS custom properties (color palette, font stacks)
- [ ] **2.3** Set base styles: `body` bg color, text color, font, line-height 1.5
- [ ] **2.4** Define heading scale (h1–h4) with serif font
- [ ] **2.5** Style selection highlight (`::selection`) with accent color
- [ ] **2.6** Add `mix-blend-mode` or opacity to ensure text is readable over point cloud

### Deliverable
Styled typography on top of the 3D canvas. Text is legible and matches the reference mood.

---

## Phase 3 — Hamburger Menu Overlay

**Goal:** Full-screen menu overlay matching the reference site's interaction pattern.

### Tasks
- [ ] **3.1** Build hamburger button (top-right corner, animated 3-line → X transition)
- [ ] **3.2** Create full-screen menu overlay (`position: fixed`, full viewport)
  - Semi-transparent dark background (blur backdrop if supported)
  - Centered vertical list of section links
  - Subtle social links at the bottom (GitHub, LinkedIn, email, etc.)
- [ ] **3.3** Animate menu open/close:
  - Hamburger lines morph to X
  - Overlay fades/slides in
  - Menu items appear with staggered delay (letter-by-letter or list-item fade)
- [ ] **3.4** Clicking a section link closes menu and scrolls to that section
- [ ] **3.5** Keyboard accessible: ESC to close, focus trap inside menu when open

### Deliverable
Fully functional hamburger menu with smooth animations and section navigation.

---

## Phase 4 — Content Sections (Scroll-Based)

**Goal:** Biographical content sections that scroll over the 3D canvas.

### Suggested Section Structure (flexible, rename/reorder as needed)
1. **Hero / Landing** — Name, tagline, scroll-down hint
2. **About** — Short bio paragraph
3. **Experience** — Work history, roles, highlights
4. **Projects** — Notable projects or work samples
5. **Contact** — Email, socials, or a simple form

### Tasks
- [ ] **4.1** Build HTML structure: each section as a full-viewport-height `<section>` with an `id`
- [ ] **4.2** Style sections: centered content, max-width container (~700–800px), vertical padding
- [ ] **4.3** Hero section:
  - Large serif name/title
  - One-line subtitle in sans-serif
  - Scroll-down arrow or "scroll" indicator (animated, like reference)
- [ ] **4.4** Section headings with numbered suffix (e.g., "About.01") echoing the reference style
- [ ] **4.5** Fade-in-on-scroll animation for section content (IntersectionObserver)
- [ ] **4.6** Horizontal rule styling between sub-sections (`border-bottom: 1px solid` with accent color)
- [ ] **4.7** Ensure content is readable over the 3D background (semi-transparent bg panel or text-shadow)

### Deliverable
Scrollable biography sections with fade-in animations, layered over the 3D point cloud.

---

## Phase 5 — Polish & Responsiveness

**Goal:** Production-ready, works on mobile and desktop.

### Tasks
- [ ] **5.1** Mobile responsive: stack layout, adjust font sizes, touch-friendly hamburger
- [ ] **5.2** Reduce point cloud complexity or point size on mobile for performance
- [ ] **5.3** Add `prefers-reduced-motion` media query — disable parallax and animations
- [ ] **5.4** Add favicon and meta tags (OG image, description, title)
- [ ] **5.5** Smooth scroll behavior (`scroll-behavior: smooth` or JS scroll-to)
- [ ] **5.6** Loading state — show bg color + name while Three.js initializes
- [ ] **5.7** Test cross-browser (Chrome, Firefox, Safari, mobile Safari)

### Deliverable
Responsive, accessible, production-ready personal site.

---

## Phase 6 — Optional Enhancements (Nice-to-Have)

- [ ] **6.1** Subtle particle color shift based on scroll position (e.g., warmer at top, cooler at bottom)
- [ ] **6.2** Custom cursor (small dot or crosshair over the canvas area)
- [ ] **6.3** Letter-by-letter title animation on hero (like reference site)
- [ ] **6.4** Dark/light toggle (high contrast mode, like reference accessibility button)
- [ ] **6.5** Deploy to GitHub Pages or Vercel

---

## Reference Design Elements to Keep

| Element                    | From Reference              | Your Version                          |
|----------------------------|-----------------------------|---------------------------------------|
| Color palette              | Burgundy + beige + rose     | Same                                  |
| Hamburger menu overlay     | Full-screen, animated       | Same interaction                      |
| Section numbering (.01)    | Per-chapter suffixes        | Per-section suffixes                  |
| Serif headings + sans body | Two-font system             | Same (free alternatives)              |
| Scroll-driven experience  | Full-viewport chapters      | Full-viewport sections                |
| 3D background              | WebGL particle system       | Your point cloud                      |
| Staggered text animation   | Letter-by-letter reveals    | Keep for hero, fade-in for sections   |

## Reference Design Elements to Drop

- WebGL shader-based particle system (replaced by point cloud loader)
- 3D hotspot navigation / map pins
- Audio/music players
- Labyrinth game
- Gyroscope parallax (keep simple mouse parallax instead)
- Multi-chapter 3D model switching
- Seasonal ambient sounds
- Newsletter form / Parsley.js validation
- Twig templates / server-side rendering

---

## Suggested Tech Dependencies

| Library             | Purpose                        | CDN/npm                          |
|---------------------|--------------------------------|----------------------------------|
| Three.js            | 3D rendering                   | `three` (npm) or CDN             |
| PLYLoader           | Load .ply point clouds         | `three/addons/loaders/PLYLoader` |
| PCDLoader           | Load .pcd point clouds         | `three/addons/loaders/PCDLoader` |
| OrbitControls       | Camera controls (optional)     | `three/addons/controls/OrbitControls` |
| Google Fonts        | Inter + Playfair Display       | `<link>` in HTML head            |

No other dependencies needed. Keep it minimal.

---

## Execution Order

```
Phase 1 (3D foundation)  →  Phase 2 (styling)  →  Phase 3 (menu)
                                                        ↓
                                              Phase 4 (content)
                                                        ↓
                                              Phase 5 (polish)
                                                        ↓
                                              Phase 6 (optional)
```

Start with Phase 1. Each phase builds on the previous. Ship after Phase 5.

import os
import urllib.parse
import random
import json

# --- CONFIGURATION ---
THUMBNAIL_DIR = 'photos-reduce'
FULL_RES_DIR = 'photos-1_5_resolution'
SITE_TITLE = "Richard's Photography"
FORMSPREE_URL = "https://formspree.io/f/mykybnrg" 
IMAGE_DATA_FILE = "images.json"

# --- SOCIAL LINKS ---
SOCIAL_LINKS = [
    {"icon": "fab fa-linkedin", "url": "https://www.linkedin.com/in/richard-yang-0b173a2aa/"},
    {"icon": "fab fa-instagram", "url": "https://www.instagram.com/richardyang02/"},
    {"icon": "fab fa-github", "url": "https://github.com/uso12"},
    {"icon": "fab fa-spotify", "url": "https://open.spotify.com/user/9528flmmasast6krr6mfnveq2?si=da2e3630e6f14d4a"},
    {"icon": "fas fa-envelope", "url": "mailto:richard20020122@gmail.com"}
]

# --- HTML HEADER TEMPLATE ---
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + SITE_TITLE + """</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&family=Great+Vibes&family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* --- GLOBAL & RESET --- */
        :root { --bg: #121212; --text: #e0e0e0; --accent: #ff7b00; --sidebar-w: 260px; }
        body { margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; background-color: var(--bg); color: var(--text); overflow-x: hidden; }
        * { box-sizing: border-box; }
        a { text-decoration: none; color: inherit; transition: 0.3s; }
        p { font-weight: 400; line-height: 1.8; color: #ccc; }
        
        body { -webkit-user-select: none; -moz-user-select: none; user-select: none; }

        /* --- SIDEBAR (DESKTOP) --- */
        .sidebar {
            width: var(--sidebar-w);
            background-color: rgba(17, 17, 17, 0.98);
            padding: 40px 30px;
            display: flex; flex-direction: column;
            position: fixed; top: 0; left: 0; height: 100vh;
            border-right: 1px solid #222;
            z-index: 1000;
        }
        
        /* LOGO STYLE: Cormorant Garamond */
        .logo { 
            font-family: 'Cormorant Garamond', serif;
            font-size: 28px; 
            color: #fff; 
            font-weight: 700; 
            margin-bottom: 40px; 
            border-bottom: 2px solid var(--accent); 
            padding-bottom: 10px; 
            display: inline-block; 
            letter-spacing: 1px; 
            text-transform: uppercase; 
        }
        
        .nav-links { display: flex; flex-direction: column; gap: 18px; }
        .nav-links a { color: #999; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }
        .nav-links a:hover { color: #fff; padding-left: 5px; }

        /* --- DROPDOWN SUBMENU STYLES --- */
        .dropdown-container { width: 100%; display: flex; flex-direction: column; }
        .dropdown-trigger { display: flex; justify-content: space-between; align-items: center; cursor: pointer; color: #999; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }
        .dropdown-trigger:hover { color: #fff; }
        
        .submenu { 
            display: none; 
            flex-direction: column; 
            gap: 12px; 
            margin-top: 15px; 
            margin-bottom: 5px;
            padding-left: 15px;
            border-left: 1px solid #333; 
        }
        .submenu.active { display: flex; }
        .submenu a { font-size: 11px; color: #666; font-weight: 600; }
        .submenu a:hover { color: var(--accent); }

        .menu-toggle { display: none; font-size: 24px; cursor: pointer; color: white; }

        /* --- MAIN CONTENT --- */
        .main-content { 
            margin-left: var(--sidebar-w); 
            width: calc(100% - var(--sidebar-w)); 
            position: relative;
        }

        /* --- HERO SECTION --- */
        .hero { 
            height: 100vh; 
            position: relative; 
            overflow: hidden; 
            display: flex; 
            justify-content: center;
            align-items: flex-end; 
            padding-bottom: 5vh; /* Lowered text position */
            background: #000; 
        }
        
        .slideshow-container { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            z-index: 1; 
            opacity: 0.8s; 
        } 
        
        .slide { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            opacity: 0; transition: opacity 2s ease-in-out; 
            display: flex; justify-content: center; align-items: center;
        }
        .slide.active { opacity: 1; }

        .slide-content-single { width: 100%; height: 100%; position: relative; }
        .slide-content-double { width: 100%; height: 100%; display: flex; }
        
        .double-half {
            width: 50%; height: 100%;
            position: relative;
            overflow: hidden;
            border-right: 1px solid rgba(0,0,0,0.5); 
        }
        .double-half:last-child { border-right: none; }

        .slide-bg-blur {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-size: cover; background-position: center;
            filter: blur(30px) brightness(0.5);
            transform: scale(1.1);
            z-index: 1;
        }
        .slide-img-contain {
            position: relative; z-index: 2;
            width: 100%; height: 100%;
            background-size: contain; 
            background-repeat: no-repeat;
            background-position: center; 
        }
        
        .hero-text { 
            position: relative; z-index: 3; text-align: center; pointer-events: none; padding: 0 15px; width: 100%; max-width: 1000px;
        }
        
        /* HERO TITLE: Great Vibes */
        .hero-title { 
            font-family: 'Great Vibes', cursive; 
            font-size: 6rem;
            text-transform: none; 
            letter-spacing: 2px; 
            margin: 0; color: #fff; font-weight: 400; 
            text-shadow: 0 4px 15px rgba(0,0,0,1); opacity: 0.9; line-height: 1.1;
        }

        .hero-subtitle { 
            font-size: 1.1rem; color: #ccc; margin-top: 15px; letter-spacing: 4px; font-weight: 500; text-transform: uppercase; opacity: 0.0;
        }

        /* --- GALLERY NAV --- */
        .gallery-nav { 
            position: sticky; top: 0; z-index: 900; 
            background: rgba(18, 18, 18, 0.95); backdrop-filter: blur(5px);
            border-bottom: 1px solid #333;
            display: flex; justify-content: center; padding: 15px 0;
            margin-bottom: 40px;
        }
        .gallery-nav a { 
            padding: 10px 30px; 
            color: #aaa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700;
        }
        .gallery-nav a:hover { color: var(--accent); }
        .nav-sep { color: #333; padding: 0 10px; }

        /* --- SECTIONS --- */
        section { padding: 40px; max-width: 1600px; margin: 0 auto; border-bottom: 1px solid #222; }
        .section-header { text-align: center; margin-bottom: 40px; padding-top: 40px; }
        .section-title { font-size: 2.5rem; font-weight: 800; text-transform: uppercase; letter-spacing: 5px; color: #fff; }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            grid-auto-rows: 10px;
        }
        .gallery-item { border-radius: 4px; overflow: hidden; background: #000; cursor: pointer; visibility: hidden; }
        .gallery-item img { width: 100%; display: block; transition: 0.5s; opacity: 0.9; }
        .gallery-item:hover img { transform: scale(1.05); opacity: 1; }

        .btn-wrapper { text-align: center; margin-top: 50px; }
        .view-more-btn {
            background: transparent; border: 2px solid rgba(255,255,255,0.2); color: #fff;
            padding: 15px 50px; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; font-weight: 700;
            cursor: pointer; transition: 0.3s; border-radius: 50px;
        }
        .view-more-btn:hover { background: #fff; color: #000; border-color: #fff; }

        .text-content { max-width: 700px; margin: 0 auto; text-align: center; line-height: 1.8; color: #ccc; }
        footer { padding: 50px 20px; text-align: center; background: #000; margin-top: 50px; display: flex; flex-direction: column; align-items: center; gap: 30px; }
        .socials { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; }
        .socials a { font-size: 1.2rem; color: #666; }

        /* --- MOBILE OPTIMIZATION --- */
        @media (max-width: 900px) {
            .sidebar { 
                position: fixed; width: 100%; height: 60px; 
                padding: 0 20px; 
                flex-direction: row; align-items: center; justify-content: space-between;
                border-bottom: 1px solid #333;
                background: rgba(18, 18, 18, 0.98);
            }
            .logo { margin-bottom: 0; border-bottom: none; font-size: 16px; letter-spacing: 0; }
            .menu-toggle { display: block; }
            
            .nav-links {
                position: fixed; top: 60px; left: 0; width: 100%; 
                background: #111; padding: 20px;
                display: none; 
                flex-direction: column; 
                align-items: flex-start; 
                border-bottom: 1px solid #333;
            }
            .nav-links.active { display: flex; }
            .nav-links > a, .dropdown-container { width: 100%; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 10px; }
            .dropdown-trigger { width: 100%; justify-content: space-between; }
            
            .socials { margin-top: 0; }
            .sidebar .socials { display: none; } 

            .main-content { margin-left: 0; width: 100%; }
            
            .hero-title { 
                font-size: 3rem;
                letter-spacing: 1px; line-height: 1.3; white-space: normal; 
            }
            .hero-subtitle { font-size: 0.75rem; letter-spacing: 2px; margin-top: 10px; }
            
            .gallery-nav { padding: 10px 0; }
            .gallery-nav a { 
                padding: 5px 8px; font-size: 0.7rem; letter-spacing: 1px; 
            }
            .nav-sep { padding: 0 2px; }

            .slide-content-double { flex-direction: column; }
            .double-half { width: 100%; height: 50%; border-right: none; border-bottom: 1px solid rgba(0,0,0,0.5); }
            .gallery-grid { grid-template-columns: 1fr; }
            section { padding: 40px 15px; } 
        }
        
        .lightbox { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.98); z-index: 2000; justify-content: center; align-items: center; }
        .lightbox img { max-width: 95%; max-height: 95vh; box-shadow: 0 0 40px rgba(0,0,0,0.5); }
        .close-btn { position: absolute; top: 30px; right: 30px; fill: white; width: 40px; height: 40px; cursor: pointer; background: rgba(255,255,255,0.1); border-radius: 50%; padding: 8px; }
    </style>
    <script>document.addEventListener('contextmenu', event => event.preventDefault());</script>
</head>
<body>
"""

def load_image_data(json_file):
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found. Please create it.")
        return {}, {}
    with open(json_file, 'r') as f:
        data = json.load(f)
    categories_js = {}
    additional_images_js = {}
    for category, content in data.items():
        categories_js[category] = content.get('base', [])
        additional_images_js[category] = content.get('additional', [])
    return categories_js, additional_images_js

def generate_site():
    categories_js_data, additional_images_js_data = load_image_data(IMAGE_DATA_FILE)
    
    slideshow_images = []
    for cat, images in categories_js_data.items():
        for img in images:
            path = os.path.join(THUMBNAIL_DIR, cat, img).replace('\\', '/')
            slideshow_images.append(path)

    cats_json = json.dumps(categories_js_data)
    adds_json = json.dumps(additional_images_js_data)
    bg_images_js = json.dumps(slideshow_images) 

    # Ensure UTF-8 for copyright symbol
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_head)

        # 1. SIDEBAR
        f.write(f"""
        <nav class="sidebar">
            <a href="#home" class="logo">{SITE_TITLE}</a>
            <div class="menu-toggle" onclick="toggleMenu()"><i class="fas fa-bars"></i></div>
            
            <div class="nav-links" id="navLinks">
                <a href="#home" onclick="toggleMenu()">Home</a>
                <div class="dropdown-container">
                    <div class="dropdown-trigger" onclick="toggleSubmenu()">
                        Galleries <i class="fas fa-caret-down" id="gal-caret"></i>
                    </div>
                    <div class="submenu" id="gal-submenu">
                        <a href="#street" onclick="toggleMenu()">Street</a>
                        <a href="#nature" onclick="toggleMenu()">Nature</a>
                        <a href="#portrait" onclick="toggleMenu()">Portrait</a>
                    </div>
                </div>
                <a href="#about" onclick="toggleMenu()">About</a>
                <a href="#contact" onclick="toggleMenu()">Contact</a>
            </div>
            
            <div style="margin-top:auto"></div>
        """)
        f.write("<div class='socials' style='justify-content: flex-start;'>")
        for link in SOCIAL_LINKS:
            target = 'target="_blank"' if "mailto" not in link['url'] else ''
            f.write(f"<a href='{link['url']}' {target}><i class='{link['icon']}'></i></a>")
        f.write("</div></nav>")

        # 2. MAIN CONTENT
        f.write('<div class="main-content">')

        # 3. HERO
        f.write(f"""
        <header class="hero" id="home">
            <div class="slideshow-container" id="hero-slides"></div>
            <div class="hero-text">
                <h1 class="hero-title">{SITE_TITLE}</h1>
                <p class="hero-subtitle">Street | Nature | Portrait</p>
            </div>
        </header>
        """)

        # 4. TOP NAV
        f.write("""
        <div id="galleries-start"></div>
        <nav class="gallery-nav">
            <a href="#street">Street</a>
            <span class="nav-sep">|</span>
            <a href="#nature">Nature</a>
            <span class="nav-sep">|</span>
            <a href="#portrait">Portrait</a>
        </nav>
        """)

        # 5. GALLERIES
        for cat in categories_js_data.keys():
            f.write(f"""
            <section id="{cat}">
                <div class="section-header"><h2 class="section-title">{cat}</h2></div>
                <div class="gallery-grid" id="grid-{cat}"></div>
                <div class="btn-wrapper">
                    <button class="view-more-btn" onclick="toggleSection('{cat}')" id="btn-{cat}">View More</button>
                </div>
            </section>
            """)

        # 6. ABOUT
        f.write("""
        <section id="about">
            <div class="section-header"><h2 class="section-title">About Me</h2></div>
            <div class="text-content">
                <p>I am a travel photographer driven by a curiosity for the world and the people who inhabit it. 
                My photography is more than just sightseeing; it is about capturing the distinct pulse of a place.</p>
                <p>Whether I am documenting the candid energy of street life, framing an intimate portrait that tells a silent story, 
                or witnessing the quiet majesty of nature, my goal remains the same: to freeze a fleeting moment that might otherwise be missed.</p>
            </div>
        </section>
        """)

        # 7. CONTACT
        f.write(f"""
        <section id="contact">
            <div class="section-header"><h2 class="section-title">Contact</h2></div>
            <div class="text-content">
                <p>Interested in prints or collaboration?</p>
                <form action="{FORMSPREE_URL}" method="POST" style="margin-top: 30px; text-align: left; display: flex; flex-direction: column; gap: 15px;">
                    <label style="color:#999; font-size: 12px; font-weight: bold; text-transform: uppercase;">Name</label>
                    <input type="text" name="name" placeholder="Your Name" required style="padding: 15px; background: #222; border: 1px solid #444; color: white; font-family: inherit;">
                    
                    <label style="color:#999; font-size: 12px; font-weight: bold; text-transform: uppercase;">Email</label>
                    <input type="email" name="email" placeholder="Your Email" required style="padding: 15px; background: #222; border: 1px solid #444; color: white; font-family: inherit;">
                    
                    <label style="color:#999; font-size: 12px; font-weight: bold; text-transform: uppercase;">Message</label>
                    <textarea name="message" rows="5" placeholder="Message" required minlength="10" style="padding: 15px; background: #222; border: 1px solid #444; color: white; font-family: inherit;"></textarea>
                    
                    <button type="submit" class="view-more-btn" style="background: var(--accent); border: none; margin-top:10px;">Send Message</button>
                </form>
            </div>
        </section>
        """)

        # 8. FOOTER WITH GLOBE WIDGET
        # NOTE: I have enabled pointer events again (removed pointer-events: none)
        # and kept 'https:' to ensure it loads on your local machine.
        f.write(f"""
        <footer>
            <div style="width: 250px; height: 250px; overflow: hidden; border-radius: 50%; box-shadow: 0 0 20px rgba(255,255,255,0.1); cursor: pointer;">
                <script type="text/javascript" id="mmvst_globe" src="https://mapmyvisitors.com/globe.js?d=OvRAWX3P9dxuVfxIndyu0KctuugYDxK7PnJ8iiIKGeE"></script>
            </div>
            
            <p>© 2025 {SITE_TITLE}</p>
        </footer>
        </div>
        """)

        # 9. SCRIPTS
        f.write(f"""
        <div class="lightbox" id="lightbox" onclick="closeLightbox()">
            <div class="close-btn"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></div>
            <img id="lightbox-img" src="">
        </div>

        <script>
            // --- UI FUNCTIONS ---
            function toggleMenu() {{
                const nav = document.getElementById('navLinks');
                nav.classList.toggle('active');
            }}

            function toggleSubmenu() {{
                const sub = document.getElementById('gal-submenu');
                const caret = document.getElementById('gal-caret');
                sub.classList.toggle('active');
                if(sub.classList.contains('active')) {{
                    caret.classList.remove('fa-caret-down');
                    caret.classList.add('fa-caret-up');
                }} else {{
                    caret.classList.remove('fa-caret-up');
                    caret.classList.add('fa-caret-down');
                }}
            }}

            // --- DATA ---
            const baseCategories = {cats_json};
            const additionalImages = {adds_json};
            const allBgImages = {bg_images_js};
            const thumbDir = "{THUMBNAIL_DIR}";
            const fullDir = "{FULL_RES_DIR}";
            let expandedState = {{ street: false, nature: false, portrait: false }};

            // --- INSTANT LOAD SLIDESHOW ENGINE ---
            const heroContainer = document.getElementById('hero-slides');
            
            function shuffle(array) {{
                for (let i = array.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }}
                return array;
            }}

            async function buildSlides(imagePaths) {{
                const portraits = [];
                const landscapes = [];

                // 1. Analyze Aspect Ratios
                await Promise.all(imagePaths.map(src => {{
                    return new Promise(resolve => {{
                        const img = new Image();
                        img.src = src;
                        img.onload = () => resolve({{ src, isPortrait: img.height > img.width }});
                        img.onerror = () => resolve(null);
                    }});
                }})).then(results => {{
                    results.forEach(res => {{
                        if (!res) return;
                        if (res.isPortrait) portraits.push(res.src);
                        else landscapes.push(res.src);
                    }});
                }});

                // 2. Pair/Build elements
                const newSlides = [];

                while(portraits.length >= 2) {{
                    const p1 = portraits.pop();
                    const p2 = portraits.pop();
                    const el = document.createElement('div');
                    el.className = 'slide';
                    el.innerHTML = `
                        <div class="slide-content-double">
                            <div class="double-half">
                                <div class="slide-bg-blur" style="background-image: url('${{p1}}');"></div>
                                <div class="slide-img-contain" style="background-image: url('${{p1}}');"></div>
                            </div>
                            <div class="double-half">
                                <div class="slide-bg-blur" style="background-image: url('${{p2}}');"></div>
                                <div class="slide-img-contain" style="background-image: url('${{p2}}');"></div>
                            </div>
                        </div>`;
                    newSlides.push(el);
                }}

                // If any portraits left, add to single
                while(portraits.length > 0) {{
                    const p1 = portraits.pop();
                    const el = document.createElement('div');
                    el.className = 'slide';
                    el.innerHTML = `
                        <div class="slide-content-single">
                            <div class="slide-bg-blur" style="background-image: url('${{p1}}');"></div>
                            <div class="slide-img-contain" style="background-image: url('${{p1}}');"></div>
                        </div>`;
                    newSlides.push(el);
                }}

                while(landscapes.length > 0) {{
                    const l1 = landscapes.pop();
                    const el = document.createElement('div');
                    el.className = 'slide';
                    el.innerHTML = `
                        <div class="slide-content-single">
                            <div class="slide-bg-blur" style="background-image: url('${{l1}}');"></div>
                            <div class="slide-img-contain" style="background-image: url('${{l1}}');"></div>
                        </div>`;
                    newSlides.push(el);
                }}
                
                return shuffle(newSlides);
            }}

            async function initSlideshow() {{
                const allShuffled = shuffle(allBgImages.slice());
                
                // --- STAGE 1: SUPER FAST LOAD (First 5 images only) ---
                const batch1 = allShuffled.slice(0, 5); 
                const batch2 = allShuffled.slice(5);

                const slides1 = await buildSlides(batch1);
                
                if (slides1.length > 0) {{
                    slides1.forEach((el, index) => {{
                        if (index === 0) el.classList.add('active'); 
                        heroContainer.appendChild(el);
                    }});
                }}

                // Start Rotating immediately
                let slideIndex = 0;
                setInterval(() => {{
                    const slides = document.querySelectorAll('.slide');
                    if(slides.length === 0) return;
                    slides[slideIndex].classList.remove('active');
                    slideIndex = (slideIndex + 1) % slides.length;
                    slides[slideIndex].classList.add('active');
                }}, 8000); 

                // --- STAGE 2: BACKGROUND LOAD (Wait 3 seconds) ---
                if (batch2.length > 0) {{
                    setTimeout(async () => {{
                        console.log("Loading remaining images in background...");
                        const slides2 = await buildSlides(batch2);
                        slides2.forEach(el => heroContainer.appendChild(el));
                    }}, 3000);
                }}
            }}

            initSlideshow();

            // --- GRID LOGIC ---
            function createItem(filename, category) {{
                let div = document.createElement('div');
                div.className = 'gallery-item';
                let img = document.createElement('img');
                let thumbPath = `${{thumbDir}}/${{category}}/${{filename}}`;
                let fullPath = `${{fullDir}}/${{category}}/${{filename}}`;
                img.src = thumbPath;
                img.loading = "lazy";
                div.onclick = () => openLightbox(fullPath);
                img.onload = () => resizeGridItem(div);
                div.appendChild(img);
                return div;
            }}

            function loadCategory(cat) {{
                let grid = document.getElementById(`grid-${{cat}}`);
                grid.innerHTML = ""; 
                let imagesToShow = baseCategories[cat];
                if (expandedState[cat]) {{ imagesToShow = imagesToShow.concat(additionalImages[cat]); }}
                if(imagesToShow) {{
                    imagesToShow.forEach(filename => {{ grid.appendChild(createItem(filename, cat)); }});
                }}
            }}

            function toggleSection(cat) {{
                expandedState[cat] = !expandedState[cat];
                let btn = document.getElementById(`btn-${{cat}}`);
                btn.innerText = expandedState[cat] ? "View Less" : "View More";
                loadCategory(cat);
            }}

            function resizeGridItem(item) {{
                let grid = item.parentElement;
                let rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
                let rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('gap'));
                let rowSpan = Math.ceil((item.querySelector('img').getBoundingClientRect().height + rowGap) / (rowHeight + rowGap));
                item.style.gridRowEnd = "span " + rowSpan;
                item.style.visibility = "visible";
            }}

            function resizeAll() {{
                let allItems = document.getElementsByClassName("gallery-item");
                for(let x=0; x<allItems.length;x++){{ resizeGridItem(allItems[x]); }}
            }}
            window.addEventListener("resize", resizeAll);
            Object.keys(baseCategories).forEach(cat => loadCategory(cat));

            function openLightbox(src) {{
                document.getElementById('lightbox-img').src = src;
                document.getElementById('lightbox').style.display = 'flex';
            }}
            function closeLightbox() {{
                document.getElementById('lightbox').style.display = 'none';
            }}
        </script>
        </body>
        </html>
        """)

    print("Success! Website generated.")

if __name__ == "__main__":
    generate_site()
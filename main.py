import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Yandex DC Drone Defense")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Защита ЦОД Яндекса: Оборона от БПЛА</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090e17;
            --card-bg: #131a26;
            --border: #222d3d;
            --red: #fc3f1d;
            --text: #f1f5f9;
            --text-dim: #94a3b8;
            --accent: #38bdf8;
            --yellow: #facc15;
            --green: #4ade80;
            --orange: #fb923c;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        html, body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        /* FULLSCREEN GAME SECTION (100vh) */
        #gameSection {
            position: relative;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #090e17;
            display: flex;
            flex-direction: column;
        }

        /* Top HUD */
        .hud-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(to bottom, rgba(9, 14, 23, 0.95), transparent);
            z-index: 5;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            pointer-events: none;
        }

        .hud-title-box {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-pill {
            background: rgba(252, 63, 29, 0.15);
            border: 1px solid rgba(252, 63, 29, 0.4);
            color: var(--red);
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            letter-spacing: 0.5px;
            transition: all 0.3s;
        }

        .brand-pill.pantsir {
            background: rgba(251, 146, 60, 0.2);
            border-color: var(--orange);
            color: var(--orange);
        }

        .hud-title {
            font-weight: 700;
            color: #fff;
            font-size: 15px;
        }

        .hud-stats {
            display: flex;
            align-items: center;
            gap: 22px;
        }

        .hp-bar-bg {
            width: 130px;
            height: 9px;
            background: #1e293b;
            border-radius: 5px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin: 0 6px;
        }

        .hp-bar-fill {
            width: 100%;
            height: 100%;
            background: var(--green);
            transition: width 0.2s;
        }

        .missile-pips {
            display: inline-flex;
            gap: 4px;
            vertical-align: middle;
            margin-left: 6px;
        }

        .missile-pip {
            width: 6px;
            height: 14px;
            background: var(--orange);
            border-radius: 2px;
            box-shadow: 0 0 5px rgba(251, 146, 60, 0.6);
            transition: opacity 0.2s;
        }

        .missile-pip.empty {
            background: rgba(255, 255, 255, 0.1);
            box-shadow: none;
        }

        /* CANVAS FULLSCREEN */
        #c {
            display: block;
            width: 100%;
            height: 100%;
            cursor: crosshair;
        }

        /* Bottom Controls Tip */
        .bottom-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 14px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(to top, rgba(9, 14, 23, 0.95), transparent);
            z-index: 5;
            font-size: 12px;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
            pointer-events: none;
        }

        .key {
            background: #1e293b;
            border: 1px solid #334155;
            color: #e2e8f0;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 11px;
            margin: 0 2px;
        }

        .scroll-down-btn {
            pointer-events: auto;
            color: var(--text-dim);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }

        .scroll-down-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.1);
        }

        /* LEVEL UP NOTIFICATION BANNER */
        .levelup-banner {
            position: absolute;
            top: 70px;
            left: 50%;
            transform: translateX(-50%) translateY(-20px);
            background: rgba(251, 146, 60, 0.92);
            color: #000;
            padding: 10px 24px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 800;
            font-size: 15px;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 30px rgba(251, 146, 60, 0.5);
            z-index: 8;
            opacity: 0;
            pointer-events: none;
            transition: all 0.4s cubic-bezier(0.1, 0.9, 0.2, 1);
        }

        .levelup-banner.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }

        /* OVERLAY: CLEAN BUTTON LIKE CHROME DINO */
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(9, 14, 23, 0.82);
            backdrop-filter: blur(4px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            z-index: 10;
        }

        .overlay.hidden {
            display: none;
        }

        .btn-play {
            background: var(--red);
            color: #fff;
            border: none;
            padding: 14px 38px;
            font-size: 17px;
            font-weight: 700;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: transform 0.15s, background 0.15s;
            box-shadow: 0 4px 20px rgba(252, 63, 29, 0.4);
        }

        .btn-play:hover {
            transform: scale(1.05);
            background: #e03212;
        }

        .overlay h2 {
            font-size: 28px;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .overlay p {
            color: var(--text-dim);
            font-size: 15px;
            margin-bottom: 24px;
            max-width: 480px;
            line-height: 1.5;
        }

        /* RULES SECTION (DOWN BELOW) */
        #rulesSection {
            padding: 60px 24px 80px;
            max-width: 1080px;
            margin: 0 auto;
        }

        .rules-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .rules-header .badge {
            display: inline-block;
            background: rgba(252, 63, 29, 0.1);
            color: var(--red);
            border: 1px solid rgba(252, 63, 29, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 10px;
        }

        .rules-header h2 {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .rules-header p {
            color: var(--text-dim);
            font-size: 15px;
        }

        .rules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .rule-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .rule-card h3 {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .rule-card .num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.05);
            color: var(--accent);
        }

        .rule-card p {
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.6;
        }

        .rule-card strong {
            color: #fff;
        }

        footer {
            margin-top: 60px;
            text-align: center;
            color: var(--text-dim);
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            border-top: 1px solid var(--border);
            padding-top: 24px;
        }
    </style>
</head>
<body>

    <!-- FULLSCREEN GAME VIEW -->
    <section id="gameSection">
        <!-- Top HUD -->
        <div class="hud-overlay">
            <div class="hud-title-box">
                <span class="brand-pill" id="turretBadge">ОБОРОННЫЙ ПУЛЕМЁТ</span>
                <span class="hud-title">Оборона ЦОД Яндекса</span>
            </div>

            <div class="hud-stats">
                <div>
                    Целостность:
                    <span class="hp-bar-bg"><div id="hpFill" class="hp-bar-fill"></div></span>
                    <strong id="hpText" style="color: #fff;">100%</strong>
                </div>

                <div id="missileBlock" style="opacity: 0.35;">
                    Ракеты:
                    <span class="missile-pips" id="missilePips"></span>
                    <strong id="missileText" style="color: var(--orange); margin-left: 6px;">0/4</strong>
                </div>

                <div>Сбито: <strong id="scoreText" style="color: var(--accent);">0</strong> <span id="unlockHint" style="font-size: 11px; color: var(--text-dim);">(до ракет: 20)</span></div>
                <div>РЭБ: <strong id="rebText" style="color: var(--yellow);">ГОТОВ</strong></div>
            </div>
        </div>

        <!-- Level up Banner -->
        <div id="levelupBanner" class="levelup-banner">
            🚀 20 ДРОНОВ СБИТО: РАЗВЁРНУТ КОМПЛЕКС ПВО! ДОСТУПНЫ САМОНАВОДЯЩИЕСЯ РАКЕТЫ (F / ПКМ)
        </div>

        <!-- CANVAS -->
        <canvas id="c"></canvas>

        <!-- Bottom Controls & Scroll Hint -->
        <div class="bottom-bar">
            <div id="controlsText">
                Огонь: <span class="key">ПРОБЕЛ</span> / <span class="key">ЛКМ</span> &nbsp;|&nbsp;
                ⚡ Взрывной РЭБ: <span class="key">E</span> &nbsp;|&nbsp;
                Наведение: <span class="key">←</span> <span class="key">→</span> / <span class="key">A</span> <span class="key">D</span> / Мышь
            </div>
            <a href="#rulesSection" class="scroll-down-btn">
                ↓ Прокрутить к правилам безопасности
            </a>
        </div>

        <!-- PLAY / RESTART OVERLAY -->
        <div id="playOverlay" class="overlay">
            <h2 id="ovTitle">Защита Дата-Центра</h2>
            <p id="ovDesc">
                Отразите налёт ударных дронов на инфраструктуру дата-центра.<br>
                Начните с пулемётной турели — сбейте 20 дронов, чтобы развернуть зенитный ракетный комплекс!
            </p>
            <button class="btn-play" onclick="startPlay()">▶ Играть</button>
        </div>
    </section>

    <!-- RULES SECTION (SCROLL DOWN) -->
    <section id="rulesSection">
        <div class="rules-header">
            <div class="badge">ПАМЯТКА БЕЗОПАСНОСТИ</div>
            <h2>Как защищён дата-центр и что делать при атаке БПЛА</h2>
            <p>Простые и понятные правила безопасности и порядок действий для сотрудников и посетителей</p>
        </div>

        <div class="rules-grid">
            <div class="rule-card" style="border-left: 3px solid var(--red);">
                <h3 style="color: var(--red);">🚨 ПРАВИЛА ПОВЕДЕНИЯ ПРИ АТАКЕ ДРОНОВ <span class="num">ДЕЙСТВИЯ</span></h3>
                <p>
                    • <strong>Внутри здания:</strong> немедленно отойдите от окон, витражей и стеклянных дверей. Спуститесь на нижние этажи или перейдите в коридоры без окон.<br>
                    • <strong>На улице:</strong> немедленно укройтесь в ближайшем капитальном здании или подземном укрытии. Не оставайтесь на открытых площадках.<br>
                    • <strong>При обнаружении дрона:</strong> не снимайте его на видео и не стойте рядом. Срочно отойдите на безопасное расстояние и сообщите охране (или по номеру 112).<br>
                    • <strong>Если дрон упал:</strong> категорически запрещено подходить, трогать или пинать обломки — они могут сдетонировать.
                </p>
            </div>

            <div class="rule-card">
                <h3>Защита от дронов с воздуха <span class="num">РУБЕЖ #0</span></h3>
                <p>
                    • <strong>Подавление связи (РЭБ):</strong> глушилки отключают управление беспилотниками и спутниковую навигацию, заставляя их падать.<br>
                    • <strong>Зенитные комплексы:</strong> обнаружение и перехват летящих дронов ракетами и автоматической стрельбой.<br>
                    • <strong>Защитные сетки:</strong> прочные металлические сетки над уличным оборудованием, чтобы сбитый дрон не упал на важные узлы.
                </p>
            </div>

            <div class="rule-card">
                <h3>Защита периметра и территории <span class="num">РУБЕЖ #1</span></h3>
                <p>
                    • <strong>Ограждение и датчики:</strong> по всему забору установлены камеры и датчики движения, которые сразу замечают чужих.<br>
                    • <strong>Дорожные барьеры:</strong> выдвижные стальные блокираторы на КПП, которые не дадут посторонней машине протаранить въезд.<br>
                    • <strong>Досмотр на входе:</strong> обязательная проверка всех въезжающих машин и проверка вносимого оборудования.
                </p>
            </div>

            <div class="rule-card">
                <h3>Вход только сотрудникам <span class="num">РУБЕЖ #2</span></h3>
                <p>
                    • <strong>Биометрия:</strong> доступ по отпечатку пальца или лицу, чужой или найденный пропуск использовать нельзя.<br>
                    • <strong>Турникеты с весовым контролем:</strong> двери пропускают строго по одному человеку, пройти вдвоём за один раз невозможно.<br>
                    • <strong>Разделение зон:</strong> каждый сотрудник может зайти только в те помещения, где ему разрешено работать.
                </p>
            </div>

            <div class="rule-card">
                <h3>Круглосуточная охрана и связь <span class="num">РУБЕЖ #3</span></h3>
                <p>
                    • <strong>Постоянный видеоконтроль:</strong> служба охраны видит всю территорию и коридоры 24 часа в сутки 7 дней в неделю.<br>
                    • <strong>Быстрое реагирование:</strong> при любой тревоге дежурные сразу вызывают полицию, спасателей и группы экстренной помощи.
                </p>
            </div>

            <div class="rule-card">
                <h3>Безопасность оборудования и данных <span class="num">РУБЕЖ #4</span></h3>
                <p>
                    • <strong>Защита шкафов:</strong> все серверы закрыты на индивидуальные замки в прочных шкафах.<br>
                    • <strong>Умное пожаротушение:</strong> в залах установлен безопасный для электроники газ, который тушит огонь без воды и пены.<br>
                    • <strong>Защищённые кабели:</strong> все провода и связь проложены глубоко под землёй по независимым путям.
                </p>
            </div>
        </div>

        <footer>
            ПАМЯТКА АНТИТЕРРОРИСТИЧЕСКОЙ БЕЗОПАСНОСТИ ДАТА-ЦЕНТРА • 2026
        </footer>
    </section>

    <!-- GAME SCRIPT -->
    <script>
        const c = document.getElementById("c");
        const ctx = c.getContext("2d");

        function resizeCanvas() {
            c.width = window.innerWidth;
            c.height = window.innerHeight;
            turret.x = c.width / 2;
            turret.y = c.height - 45;
        }
        window.addEventListener("resize", resizeCanvas);

        let active = false;
        let hp = 100;
        let score = 0;

        // Weapon Unlock State (Machinegun -> Pantsir after 20 kills)
        let isPantsirUnlocked = false;

        // Turret State
        const turret = {
            x: window.innerWidth / 2,
            y: window.innerHeight - 45,
            angle: -Math.PI / 2,
            radarAngle: 0
        };

        // Missiles (Pantsir 57E6 missiles)
        const maxMissiles = 4;
        let missilesCount = 0;
        let lastMissileRegen = Date.now();

        // Inputs
        let keys = { left: false, right: false };
        let mouseX = window.innerWidth / 2;
        let mouseY = 200;

        // Arrays
        let bullets = [];
        let missiles = [];
        let drones = [];
        let particles = [];
        let rebPulse = null;

        // REB Cooldown (15 sec)
        let rebReady = true;
        let rebTimer = 0;
        const rebCD = 15000;

        let lastFireTime = 0;

        function updateMissileUI() {
            const container = document.getElementById("missilePips");
            container.innerHTML = "";
            for (let i = 0; i < maxMissiles; i++) {
                const pip = document.createElement("div");
                pip.className = "missile-pip" + (i < missilesCount ? "" : " empty");
                container.appendChild(pip);
            }
            document.getElementById("missileText").innerText = isPantsirUnlocked ? `${missilesCount}/4` : "ЗАБЛОКИРОВАНО";
        }

        resizeCanvas();
        updateMissileUI();

        // Listeners
        window.addEventListener("keydown", (e) => {
            if (e.code === "ArrowLeft" || e.code === "KeyA") keys.left = true;
            if (e.code === "ArrowRight" || e.code === "KeyD") keys.right = true;
            if (e.code === "Space") {
                if (window.scrollY < window.innerHeight / 2) {
                    e.preventDefault();
                }
                if (!active) {
                    startPlay();
                } else {
                    fireCannon();
                }
            }
            if (e.code === "KeyF") {
                if (isPantsirUnlocked) fireMissile();
            }
            if (e.code === "KeyE") {
                useReb();
            }
        });

        window.addEventListener("keyup", (e) => {
            if (e.code === "ArrowLeft" || e.code === "KeyA") keys.left = false;
            if (e.code === "ArrowRight" || e.code === "KeyD") keys.right = false;
        });

        c.addEventListener("mousemove", (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            turret.angle = Math.atan2(mouseY - turret.y, mouseX - turret.x);
        });

        c.addEventListener("mousedown", (e) => {
            if (!active) return;
            if (e.button === 0) fireCannon();
            if (e.button === 2) {
                if (isPantsirUnlocked) fireMissile();
            }
        });

        c.addEventListener("contextmenu", (e) => e.preventDefault());

        function startPlay() {
            document.getElementById("playOverlay").classList.add("hidden");
            hp = 100;
            score = 0;
            isPantsirUnlocked = false;
            missilesCount = 0;
            bullets = [];
            missiles = [];
            drones = [];
            particles = [];
            rebPulse = null;
            rebReady = true;
            rebTimer = 0;
            active = true;

            document.getElementById("hpText").innerText = "100%";
            document.getElementById("hpFill").style.width = "100%";
            document.getElementById("scoreText").innerText = "0";
            document.getElementById("unlockHint").innerText = "(до Панциря: 20)";
            document.getElementById("unlockHint").style.display = "inline";
            document.getElementById("rebText").innerText = "ГОТОВ";
            document.getElementById("rebText").style.color = "var(--yellow)";

            document.getElementById("turretBadge").innerText = "ОБОРОННЫЙ ПУЛЕМЁТ";
            document.getElementById("turretBadge").className = "brand-pill";
            document.getElementById("missileBlock").style.opacity = "0.35";
            document.getElementById("controlsText").innerHTML = `Пулемёт: <span class="key">ПРОБЕЛ</span> / <span class="key">ЛКМ</span> &nbsp;|&nbsp; ⚡ Взрывной РЭБ: <span class="key">E</span> &nbsp;|&nbsp; Наведение: <span class="key">←</span> <span class="key">→</span> / <span class="key">A</span> <span class="key">D</span> / Мышь`;

            updateMissileUI();
        }

        function unlockPantsir() {
            isPantsirUnlocked = true;
            missilesCount = maxMissiles;
            updateMissileUI();

            const badge = document.getElementById("turretBadge");
            badge.innerText = "ЗЕНИТНЫЙ КОМПЛЕКС";
            badge.className = "brand-pill pantsir";

            document.getElementById("missileBlock").style.opacity = "1";
            document.getElementById("unlockHint").style.display = "none";
            document.getElementById("controlsText").innerHTML = `Спаренная пушка: <span class="key">ПРОБЕЛ</span> / <span class="key">ЛКМ</span> &nbsp;|&nbsp; 🚀 Ракета: <span class="key">F</span> / <span class="key">ПКМ</span> &nbsp;|&nbsp; ⚡ Взрывной РЭБ: <span class="key">E</span>`;

            // Show celebratory banner
            const banner = document.getElementById("levelupBanner");
            banner.classList.add("show");
            setTimeout(() => banner.classList.remove("show"), 4500);

            // Flash effect particles around turret
            for (let i = 0; i < 30; i++) {
                const a = Math.random() * Math.PI * 2;
                particles.push({
                    x: turret.x,
                    y: turret.y,
                    vx: Math.cos(a) * (2 + Math.random() * 4),
                    vy: Math.sin(a) * (2 + Math.random() * 4),
                    color: "#fb923c",
                    life: 40
                });
            }
        }

        function gameOver() {
            active = false;
            document.getElementById("ovTitle").innerText = "Объект повреждён";
            document.getElementById("ovDesc").innerText = `Налёт БПЛА отражён частично. Сбито дронов: ${score}. Резервные цепи переведены на автономные генераторы.`;
            document.getElementById("playOverlay").classList.remove("hidden");
        }

        // Firing Mechanics: Machinegun (single) vs Pantsir (twin 30mm)
        function fireCannon() {
            const now = Date.now();
            const delay = isPantsirUnlocked ? 130 : 190;
            if (now - lastFireTime < delay) return;
            lastFireTime = now;

            const spd = isPantsirUnlocked ? 14 : 11;
            const dx = Math.cos(turret.angle);
            const dy = Math.sin(turret.angle);

            if (isPantsirUnlocked) {
                // Twin autocannons
                const perpX = -dy * 6;
                const perpY = dx * 6;
                bullets.push({
                    x: turret.x + dx * 34 + perpX,
                    y: turret.y + dy * 34 + perpY,
                    vx: dx * spd,
                    vy: dy * spd
                });
                bullets.push({
                    x: turret.x + dx * 34 - perpX,
                    y: turret.y + dy * 34 - perpY,
                    vx: dx * spd,
                    vy: dy * spd
                });
            } else {
                // Single machine gun barrel
                bullets.push({
                    x: turret.x + dx * 28,
                    y: turret.y + dy * 28,
                    vx: dx * spd,
                    vy: dy * spd
                });
            }
        }

        // Pantsir Guided SAM Missile (57E6)
        function fireMissile() {
            if (!isPantsirUnlocked || missilesCount <= 0 || !active) return;
            missilesCount--;
            updateMissileUI();

            const dx = Math.cos(turret.angle);
            const dy = Math.sin(turret.angle);
            const side = (missilesCount % 2 === 0) ? 18 : -18;
            const perpX = -dy * side;
            const perpY = dx * side;

            missiles.push({
                x: turret.x + perpX,
                y: turret.y - 10 + perpY,
                vx: dx * 4,
                vy: dy * 4,
                angle: turret.angle,
                speed: 4,
                maxSpeed: 17,
                target: findBestTarget()
            });

            // Launch smoke puff
            for (let i = 0; i < 8; i++) {
                particles.push({
                    x: turret.x + perpX,
                    y: turret.y - 10 + perpY,
                    vx: (Math.random() - 0.5) * 3,
                    vy: Math.random() * 2,
                    color: "rgba(200, 210, 220, 0.6)",
                    life: 25
                });
            }
        }

        function findBestTarget() {
            if (drones.length === 0) return null;
            let best = drones[0];
            let bestDist = 9999;
            drones.forEach(d => {
                const dist = Math.hypot(d.x - mouseX, d.y - mouseY);
                if (dist < bestDist) {
                    bestDist = dist;
                    best = d;
                }
            });
            return best;
        }

        function useReb() {
            if (!rebReady || !active) return;
            rebReady = false;
            rebTimer = Date.now();
            document.getElementById("rebText").innerText = "15с";
            document.getElementById("rebText").style.color = "var(--text-dim)";

            rebPulse = { radius: 10, max: c.width * 0.75, alpha: 1.0 };

            // Instantly detonate and explode all drones on the screen!
            drones.forEach(d => {
                explode(d.x, d.y, "#facc15", 26);
                explode(d.x, d.y, "#fc3f1d", 18);
                addScore(1);
            });
            drones = [];
        }

        function addScore(pts = 1) {
            score += pts;
            document.getElementById("scoreText").innerText = score;

            if (!isPantsirUnlocked) {
                const left = Math.max(0, 20 - score);
                document.getElementById("unlockHint").innerText = `(до Панциря: ${left})`;
                if (score >= 20) {
                    unlockPantsir();
                }
            }
        }

        // Dynamic difficulty progression based on score
        let lastSpawn = 0;
        function spawnDrone() {
            // Base speed scales smoothly with score
            const speedFactor = 1 + Math.min(2.2, score * 0.035);
            const baseSpd = (0.5 + Math.random() * 0.35) * speedFactor;

            // Chances for heavy winged drones and fast FPVs increase
            const heavyProb = Math.min(0.5, 0.15 + score * 0.015);
            const isHeavy = Math.random() < heavyProb;

            // Safe screen margin (keeps drones clearly visible on all screen sizes)
            const margin = Math.max(120, c.width * 0.14);
            const spawnX = margin + Math.random() * (c.width - margin * 2);

            drones.push({
                x: spawnX,
                y: -20,
                vx: (Math.random() - 0.5) * 0.25,
                vy: isHeavy ? baseSpd * 0.75 : baseSpd,
                hp: isHeavy ? (score >= 25 ? 3 : 2) : 1,
                size: isHeavy ? 18 : 11,
                color: isHeavy ? "#facc15" : "#fc3f1d",
                wobble: Math.random() * Math.PI
            });
        }

        function explode(x, y, color, count = 14) {
            for (let i = 0; i < count; i++) {
                const a = Math.random() * Math.PI * 2;
                const s = 0.5 + Math.random() * 3.5;
                particles.push({
                    x, y,
                    vx: Math.cos(a) * s,
                    vy: Math.sin(a) * s,
                    color,
                    life: 25 + Math.random() * 20
                });
            }
        }

        // Loop with Delta Time (FPS-independent physics)
        let lastFrameTime = performance.now();

        function update(dt) {
            if (!active) return;

            // Rotate search radar
            turret.radarAngle += 0.05 * dt;

            // Keyboard turret movement
            if (keys.left) turret.angle -= 0.04 * dt;
            if (keys.right) turret.angle += 0.04 * dt;
            if (turret.angle > -0.1) turret.angle = -0.1;
            if (turret.angle < -Math.PI + 0.1) turret.angle = -Math.PI + 0.1;

            // Missile reload over time for Pantsir (1 missile every 5 sec)
            if (isPantsirUnlocked) {
                if (missilesCount < maxMissiles) {
                    if (Date.now() - lastMissileRegen > 5000) {
                        missilesCount++;
                        lastMissileRegen = Date.now();
                        updateMissileUI();
                    }
                } else {
                    lastMissileRegen = Date.now();
                }
            }

            // REB timer
            if (!rebReady) {
                const passed = Date.now() - rebTimer;
                if (passed >= rebCD) {
                    rebReady = true;
                    document.getElementById("rebText").innerText = "ГОТОВ";
                    document.getElementById("rebText").style.color = "var(--yellow)";
                } else {
                    document.getElementById("rebText").innerText = Math.ceil((rebCD - passed) / 1000) + "с";
                }
            }

            // Spawn rate accelerates with score (from 2400ms down to 900ms)
            const currentSpawnDelay = Math.max(900, 2400 - score * 45);
            if (Date.now() - lastSpawn > currentSpawnDelay) {
                spawnDrone();
                lastSpawn = Date.now();
            }

            // Bullets
            for (let i = bullets.length - 1; i >= 0; i--) {
                const b = bullets[i];
                b.x += b.vx * dt;
                b.y += b.vy * dt;
                if (b.x < 0 || b.x > c.width || b.y < 0 || b.y > c.height) {
                    bullets.splice(i, 1);
                    continue;
                }

                // Check hit
                for (let j = drones.length - 1; j >= 0; j--) {
                    const d = drones[j];
                    if (Math.hypot(b.x - d.x, b.y - d.y) < d.size + 4) {
                        d.hp--;
                        bullets.splice(i, 1);
                        explode(b.x, b.y, "#38bdf8", 5);
                        if (d.hp <= 0) {
                            explode(d.x, d.y, d.color, 16);
                            drones.splice(j, 1);
                            addScore(1);
                        }
                        break;
                    }
                }
            }

            // Pantsir Missiles (Homing Physics with Smoke Trail)
            for (let i = missiles.length - 1; i >= 0; i--) {
                const m = missiles[i];
                if (m.speed < m.maxSpeed) m.speed += 0.45 * dt;

                if (!m.target || !drones.includes(m.target)) {
                    m.target = findBestTarget();
                }

                if (m.target) {
                    const targetAngle = Math.atan2(m.target.y - m.y, m.target.x - m.x);
                    let diff = targetAngle - m.angle;
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    while (diff > Math.PI) diff -= Math.PI * 2;
                    m.angle += diff * Math.min(1, 0.12 * dt);
                }

                m.vx = Math.cos(m.angle) * m.speed;
                m.vy = Math.sin(m.angle) * m.speed;
                m.x += m.vx * dt;
                m.y += m.vy * dt;

                // Smoke trail
                if (Math.random() < 0.8 * dt) {
                    particles.push({
                        x: m.x - Math.cos(m.angle) * 10,
                        y: m.y - Math.sin(m.angle) * 10,
                        vx: (Math.random() - 0.5) * 1,
                        vy: (Math.random() - 0.5) * 1,
                        color: Math.random() < 0.5 ? "#fb923c" : "#94a3b8",
                        life: 18
                    });
                }

                if (m.x < -50 || m.x > c.width + 50 || m.y < -50 || m.y > c.height) {
                    missiles.splice(i, 1);
                    continue;
                }

                // Blast detonation (radius 70px)
                for (let j = drones.length - 1; j >= 0; j--) {
                    const d = drones[j];
                    if (Math.hypot(m.x - d.x, m.y - d.y) < d.size + 16) {
                        explode(m.x, m.y, "#fb923c", 28);
                        explode(m.x, m.y, "#facc15", 18);
                        missiles.splice(i, 1);

                        // Splash damage to all nearby drones
                        for (let k = drones.length - 1; k >= 0; k--) {
                            const nearby = drones[k];
                            if (Math.hypot(m.x - nearby.x, m.y - nearby.y) < 70) {
                                nearby.hp -= 3;
                                if (nearby.hp <= 0) {
                                    explode(nearby.x, nearby.y, nearby.color, 14);
                                    drones.splice(k, 1);
                                    addScore(1);
                                }
                            }
                        }
                        break;
                    }
                }
            }

            // Drones (Delta time applied + screen margin bounce)
            const sideMargin = Math.max(90, c.width * 0.1);
            for (let i = drones.length - 1; i >= 0; i--) {
                const d = drones[i];
                d.wobble += 0.03 * dt;
                d.x += (d.vx + Math.sin(d.wobble) * 0.3) * dt;
                d.y += d.vy * dt;

                // Keep away from screen edges
                if (d.x < sideMargin) {
                    d.x = sideMargin;
                    d.vx = Math.abs(d.vx);
                } else if (d.x > c.width - sideMargin) {
                    d.x = c.width - sideMargin;
                    d.vx = -Math.abs(d.vx);
                }

                if (d.y >= c.height - 55) {
                    explode(d.x, d.y, "#fc3f1d", 18);
                    drones.splice(i, 1);
                    hp = Math.max(0, hp - 12);
                    document.getElementById("hpText").innerText = hp + "%";
                    document.getElementById("hpFill").style.width = hp + "%";
                    if (hp <= 0) {
                        gameOver();
                        return;
                    }
                }
            }

            // REB Pulse
            if (rebPulse) {
                rebPulse.radius += 14 * dt;
                rebPulse.alpha = 1 - (rebPulse.radius / rebPulse.max);
                if (rebPulse.radius >= rebPulse.max) rebPulse = null;
            }

            // Particles
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.vx * dt;
                p.y += p.vy * dt;
                p.life -= 1 * dt;
                if (p.life <= 0) particles.splice(i, 1);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, c.width, c.height);

            // Clean Dark Sky
            ctx.fillStyle = "#090e17";
            ctx.fillRect(0, 0, c.width, c.height);

            // Data Center Skyline
            const bWidth = Math.min(380, c.width * 0.35);
            const bLeft = c.width / 2 - bWidth / 2;
            const bTop = c.height - 240;

            ctx.fillStyle = "#101622";
            ctx.fillRect(bLeft - bWidth * 0.7, bTop + 40, bWidth * 0.65, 200);
            ctx.fillRect(bLeft + bWidth * 1.05, bTop + 40, bWidth * 0.65, 200);

            ctx.fillStyle = "#131b28";
            ctx.fillRect(bLeft, bTop, bWidth, 240);

            const leds = Math.floor(bWidth / 45);
            for (let i = 0; i < leds; i++) {
                ctx.fillStyle = i % 2 === 0 ? "rgba(74, 222, 128, 0.45)" : "rgba(56, 189, 248, 0.45)";
                ctx.fillRect(bLeft + 20 + i * 42, bTop + 45, 24, 8);
                ctx.fillRect(bLeft + 20 + i * 42, bTop + 65, 24, 8);
            }

            ctx.fillStyle = "#fc3f1d";
            ctx.font = "bold 14px 'JetBrains Mono', monospace";
            ctx.textAlign = "center";
            ctx.fillText("YANDEX DC", c.width / 2, bTop + 30);
            ctx.textAlign = "left";

            // Netting Protection Canopy
            ctx.strokeStyle = "rgba(56, 189, 248, 0.25)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(40, c.height - 70);
            ctx.lineTo(c.width - 40, c.height - 70);
            ctx.stroke();

            ctx.fillStyle = "rgba(148, 163, 184, 0.5)";
            ctx.font = "11px 'JetBrains Mono', monospace";
            ctx.textAlign = "center";
            ctx.fillText("СТАЛЬНАЯ ЗАЩИТНАЯ СЕТКА НАД ЭНЕРГОУЗЛАМИ", c.width / 2, c.height - 75);
            ctx.textAlign = "left";

            // Ground base
            ctx.fillStyle = "#151d2a";
            ctx.fillRect(0, c.height - 50, c.width, 50);

            // REB Pulse
            if (rebPulse) {
                ctx.save();
                ctx.strokeStyle = `rgba(250, 204, 21, ${rebPulse.alpha})`;
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.arc(turret.x, turret.y, rebPulse.radius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            }

            // Bullets
            bullets.forEach(b => {
                ctx.fillStyle = "#38bdf8";
                ctx.beginPath();
                ctx.arc(b.x, b.y, 3, 0, Math.PI * 2);
                ctx.fill();
            });

            // Missiles
            missiles.forEach(m => {
                ctx.save();
                ctx.translate(m.x, m.y);
                ctx.rotate(m.angle);

                ctx.fillStyle = "#f1f5f9";
                ctx.fillRect(-10, -2.5, 20, 5);
                ctx.fillStyle = "#fc3f1d";
                ctx.beginPath();
                ctx.moveTo(10, -2.5);
                ctx.lineTo(16, 0);
                ctx.lineTo(10, 2.5);
                ctx.closePath();
                ctx.fill();
                ctx.fillStyle = "#475569";
                ctx.fillRect(-10, -5, 3, 10);
                ctx.restore();
            });

            // Particles
            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
                ctx.fill();
            });

            // Drones
            drones.forEach(d => {
                ctx.save();
                ctx.translate(d.x, d.y);
                ctx.fillStyle = d.color;

                if (d.size > 13) {
                    ctx.beginPath();
                    ctx.moveTo(0, d.size);
                    ctx.lineTo(-d.size, -d.size / 2);
                    ctx.lineTo(d.size, -d.size / 2);
                    ctx.closePath();
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.arc(0, 0, d.size / 2, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#94a3b8";
                    ctx.lineWidth = 1;
                    ctx.strokeRect(-d.size, -2, d.size * 2, 4);
                }
                ctx.restore();
            });

            // TURRET DRAWING (Changes visually when Pantsir unlocked)
            ctx.save();
            ctx.translate(turret.x, turret.y);

            if (isPantsirUnlocked) {
                // PANTSIR-S1 MODULE
                ctx.fillStyle = "#2d3748";
                ctx.beginPath();
                ctx.arc(0, 10, 26, Math.PI, 0);
                ctx.fill();

                // Rotating Search Radar
                ctx.save();
                ctx.translate(0, -14);
                ctx.rotate(turret.radarAngle);
                ctx.strokeStyle = "#38bdf8";
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                ctx.moveTo(-14, 0);
                ctx.lineTo(14, 0);
                ctx.stroke();
                ctx.restore();

                // Rotated Guns & Missile Pods
                ctx.save();
                ctx.rotate(turret.angle);

                // Missile pods
                ctx.fillStyle = "#475569";
                ctx.fillRect(0, -18, 22, 6);
                ctx.fillRect(0, 12, 22, 6);
                ctx.fillStyle = "#fb923c";
                ctx.fillRect(20, -17, 3, 4);
                ctx.fillRect(20, 13, 3, 4);

                // Housing & Twin Barrels
                ctx.fillStyle = "#1e293b";
                ctx.fillRect(-10, -8, 20, 16);
                ctx.fillStyle = "#38bdf8";
                ctx.fillRect(0, -4, 34, 3);
                ctx.fillRect(0, 1, 34, 3);
                ctx.restore();

            } else {
                // STARTER MACHINEGUN TURRET
                ctx.fillStyle = "#273244";
                ctx.beginPath();
                ctx.arc(0, 10, 20, Math.PI, 0);
                ctx.fill();

                // Rotated single barrel
                ctx.save();
                ctx.rotate(turret.angle);
                ctx.fillStyle = "#1e293b";
                ctx.fillRect(-8, -6, 16, 12);
                ctx.fillStyle = "#38bdf8";
                ctx.fillRect(0, -2.5, 26, 5);
                ctx.restore();
            }

            ctx.restore();
        }

        function anim(now) {
            if (!now) now = performance.now();
            // Delta time normalized to 60 FPS (16.67ms = 1.0)
            let dt = (now - lastFrameTime) / (1000 / 60);
            lastFrameTime = now;

            // Clamp dt to avoid huge jumps on tab switch/lag spikes
            if (dt > 3.0) dt = 3.0;
            if (dt < 0.1) dt = 0.1;

            update(dt);
            draw();
            requestAnimationFrame(anim);
        }
        anim(performance.now());
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=HTML_CONTENT)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2222, reload=False)

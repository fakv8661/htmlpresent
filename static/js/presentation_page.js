
/* =========================================================
   presentations.js — jQuery 4.0.0
   ========================================================= */
$(function () {

    /* =========================================================
       1. ДАННЫЕ ПРЕЗЕНТАЦИЙ
       (добавь сюда новые объекты — блоки создадутся автоматически)
       ========================================================= */
    /*const PRESENTATIONS = [
        {
            id: 0,
            title: 'Квантовые вычисления',
            authors: 'Иванов А., Петрова М.',
            description:
                'Подробный обзор принципов работы квантовых компьютеров: кубиты, суперпозиция, ' +
                'запутанность и квантовый параллелизм. Рассматриваются алгоритмы Шора и Гровера, ' +
                'современные реализации квантовых процессоров, вопросы коррекции ошибок, а также ' +
                'перспективы применения в криптографии, оптимизации и моделировании молекулярных систем.',
            cover: null
        },
        {
            id: 1,
            title: 'Нейронные сети в медицине',
            authors: 'Смирнова Е., Кузнецов Д., Орлов В.',
            description:
                'Практическое применение глубокого обучения для диагностики заболеваний по снимкам МРТ и КТ. ' +
                'Разбираются архитектуры свёрточных сетей, методы аугментации данных, проблемы дисбаланса классов ' +
                'и интерпретируемости моделей. Приведены кейсы внедрения в клиническую практику и оценка точности ' +
                'по сравнению с врачами-экспертами.',
            cover: null
        },
        {
            id: 2,
            title: 'Устойчивое развитие городов',
            authors: 'Гринёва О.',
            description:
                'Концепция «умного города» и устойчивого развития urban-среды: зелёные крыши, ' +
                'энергоэффективные здания, интеллектуальные транспортные системы и управление отходами. ' +
                'Анализируются примеры Копенгагена, Сингапура и Амстердама, а также метрики оценки ' +
                'экологического следа городских агломераций.',
            cover: null
        },
        {
            id: 3,
            title: 'Космический туризм',
            authors: 'Белов К., Ясная Л.',
            description:
                'Обзор коммерческих суборбитальных и орбитальных полётов: технологии многоразовых ракет, ' +
                'подготовка туристов, медицинские ограничения и правовые аспекты. Сравнение предложений ' +
                'Blue Origin, Virgin Galactic и SpaceX, экономика отрасли и прогнозы развития на ближайшее десятилетие.',
            cover: null
        }
    ];*/

    /* =========================================================
       2. ГЕНЕРАЦИЯ ОБЛОЖКИ (SVG data URI)
       ========================================================= */
    const PALETTES = [
        ['#8b5cf6', '#00d4ff'],
        ['#ff2d95', '#ffb020'],
        ['#00d4ff', '#8b5cf6'],
        ['#ffb020', '#ff2d95'],
        ['#7b2ff7', '#00d4ff']
    ];

    function escapeXml(str) {
        return String(str).replace(/[&<>"']/g, c => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&apos;'
        }[c]));
    }

    function makeCover(data, index) {
        if (data.cover) return data.cover;

        const pair = PALETTES[index % PALETTES.length];
        const c1 = pair[0], c2 = pair[1];

        const initials = data.title
            .split(/\s+/)
            .slice(0, 2)
            .map(w => w[0])
            .join('')
            .toUpperCase();

        const svg =
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">' +
                '<defs>' +
                    '<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">' +
                        '<stop offset="0" stop-color="' + c1 + '"/>' +
                        '<stop offset="1" stop-color="' + c2 + '"/>' +
                    '</linearGradient>' +
                    '<radialGradient id="r" cx="0.25" cy="0.2" r="0.9">' +
                        '<stop offset="0" stop-color="#ffffff" stop-opacity="0.35"/>' +
                        '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>' +
                    '</radialGradient>' +
                '</defs>' +
                '<rect width="640" height="360" fill="#0a0a14"/>' +
                '<rect width="640" height="360" fill="url(#g)" opacity="0.88"/>' +
                '<rect width="640" height="360" fill="url(#r)"/>' +
                '<g opacity="0.16" fill="none" stroke="#ffffff" stroke-width="1.5">' +
                    '<circle cx="540" cy="80" r="70"/>' +
                    '<circle cx="540" cy="80" r="112"/>' +
                    '<circle cx="540" cy="80" r="154"/>' +
                '</g>' +
                '<text x="48" y="302" font-family="Orbitron, Arial, sans-serif" ' +
                    'font-size="90" font-weight="900" fill="#ffffff" opacity="0.95">' +
                    escapeXml(initials) +
                '</text>' +
            '</svg>';

        return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    }

    /* =========================================================
       3. КРАТКОЕ ОПИСАНИЕ (часть + «…»)
       ========================================================= */
    const SHORT_LEN = 110;

    function shortDescription(text) {
        const t = String(text).trim();
        if (t.length <= SHORT_LEN) return t;
        return t.slice(0, SHORT_LEN).replace(/\s+\S*$/, '') + '…';
    }

    /* =========================================================
       4. createPresentationBlock(data, type, index)
          type: 'short' — краткий блок (карточка)
                'full'  — полный блок (для модального окна)
       ========================================================= */
    function createPresentationBlock(data, type, index) {
        const cover = makeCover(data, index || 0);

        /* ---------- ПОЛНЫЙ БЛОК ---------- */
        if (type === 'full') {
            return $('<div class="presentation-full">').append(

                $('<div class="modal__media">').append(
                    $('<img class="modal__cover">')
                        .attr('src', cover)
                        .attr('alt', data.title)
                ),

                $('<h2 class="modal__title">').text(data.title),

                $('<p class="modal__authors">').text('Авторы: ' + data.authors),

                $('<p class="modal__desc">').text(data.description),

                $('<a class="btn-watch">')
                    .attr('href', 'presentation/' + data.id)
                    .text('Просмотреть')
            );
        }

        /* ---------- КРАТКИЙ БЛОК ---------- */
        const $card = $('<article class="card">')
            .attr('data-id', data.id)
            .attr('tabindex', 0)
            .attr('role', 'button')
            .attr('aria-label', 'Открыть презентацию: ' + data.title);

        $('<div class="card__media">').append(
            $('<img class="card__cover">')
                .attr('src', cover)
                .attr('alt', data.title)
                .attr('loading', 'lazy')
        ).appendTo($card);

        $('<div class="card__body">').append(
            $('<h3 class="card__title">').text(data.title),
            $('<p class="card__authors">').text('Авторы: ' + data.authors),
            $('<p class="card__desc">').text(shortDescription(data.description))
        ).appendTo($card);

        $('<span class="card__shine" aria-hidden="true">').appendTo($card);

        return $card;
    }

    /* =========================================================
       5. РЕНДЕР СЕТКИ КАРТОЧЕК
       ========================================================= */
    const $grid = $('#cardsGrid');

    if (PRESENTATIONS.length === 0) {
        $grid.append(
            $('<p class="no-presentations">')
                .text('Презентаций нет')
        );
    } else {
        PRESENTATIONS.forEach(function (p, i) {
            const $card = createPresentationBlock(p, 'short', i);
            $card.css('--i', i);
            $grid.append($card);
        });
    }

    /* =========================================================
       6. МОДАЛЬНОЕ ОКНО
       ========================================================= */
    const $modal = $('#modal');

    function openModal(data, index) {
        const $win = $modal.find('.modal__window');

        const $close = $('<button class="modal__close" type="button" data-close aria-label="Закрыть">')
            .html(
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">' +
                    '<path d="M6 6l12 12M18 6L6 18"/>' +
                '</svg>'
            );

        $win.empty().append($close, createPresentationBlock(data, 'full', index));

        $modal.addClass('is-open').attr('aria-hidden', 'false');
        $('body').css('overflow', 'hidden');
    }

    function closeModal() {
        $modal.removeClass('is-open').attr('aria-hidden', 'true');
        $('body').css('overflow', '');
    }

    /* ---------- Клик по карточке ---------- */
    $grid.on('click', '.card', function () {
        const id = Number($(this).attr('data-id'));
        const index = PRESENTATIONS.findIndex(p => p.id === id);
        if (index === -1) return;
        openModal(PRESENTATIONS[index], index);
    });

    /* ---------- Доступность: Enter / Space ---------- */
    $grid.on('keydown', '.card', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            $(this).trigger('click');
        }
    });

    /* ---------- Закрытие: клик по backdrop / крестику ---------- */
    $modal.on('click', '[data-close]', closeModal);

    /* ---------- Закрытие: Escape ---------- */
    $(document).on('keydown', function (e) {
        if (e.key === 'Escape' && $modal.hasClass('is-open')) closeModal();
    });

    /* =========================================================
       7. ХОВЕР КАРТОЧЕК: 3D-наклон + блик
       ========================================================= */
    $grid.on('mouseenter', '.card', function () {
        $('body').addClass('hovering');
    });

    $grid.on('mouseleave', '.card', function () {
        $('body').removeClass('hovering');
        $(this).css('transform', '');
    });

    $grid.on('mousemove', '.card', function (e) {
        const rect = this.getBoundingClientRect();
        const nx = (e.clientX - rect.left) / rect.width;
        const ny = (e.clientY - rect.top) / rect.height;

        $(this).css({
            '--mx': (nx * 100) + '%',
            '--my': (ny * 100) + '%',
            'transform':
                'perspective(900px) rotateX(' + ((ny - 0.5) * -7) + 'deg) ' +
                'rotateY(' + ((nx - 0.5) * 7) + 'deg) ' +
                'translateY(-8px) scale(1.02)'
        });
    });

    /* ---------- Курсор над кнопками/ссылками ---------- */
    $(document).on('mouseenter', 'button, a', function () {
        $('body').addClass('hovering');
    });

    $(document).on('mouseleave', 'button, a', function () {
        $('body').removeClass('hovering');
    });

    /* =========================================================
       8. ЗВЁЗДНОЕ ПОЛЕ + МЕТЕОРЫ + ПАРАЛЛАКС
       ========================================================= */
    const canvas = document.getElementById('starfield');

    if (canvas) {
        const ctx = canvas.getContext('2d', { alpha: true });

        let W = 0, H = 0, DPR = 1;
        const mouse = { x: -9999, y: -9999 };
        const parallax = { x: 0, y: 0, tx: 0, ty: 0 };

        function resize() {
            DPR = Math.min(window.devicePixelRatio || 1, 2);
            W = window.innerWidth;
            H = window.innerHeight;

            canvas.width = W * DPR;
            canvas.height = H * DPR;
            canvas.style.width = W + 'px';
            canvas.style.height = H + 'px';

            ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
        }

        resize();
        window.addEventListener('resize', resize);

        window.addEventListener('mousemove', function (e) {
            mouse.x = e.clientX;
            mouse.y = e.clientY;

            parallax.tx = (e.clientX / W - 0.5) * 2;
            parallax.ty = (e.clientY / H - 0.5) * 2;
        });

        window.addEventListener('mouseleave', function () {
            mouse.x = -9999;
            mouse.y = -9999;
            parallax.tx = 0;
            parallax.ty = 0;
        });

        const STAR_PALETTE = [
            '#8b5cf6',
            '#ff2d95',
            '#00d4ff',
            '#ffffff',
            '#ffb020'
        ];

        class Star {
            constructor() {
                this.depth = Math.random();
                this.reset();
                this.x = Math.random() * W;
                this.y = Math.random() * H;
            }

            reset() {
                this.x = Math.random() * W;
                this.y = Math.random() * H;
                this.z = 0.22 + this.depth * 0.95;
                this.r = 0.4 + this.depth * 1.9;
                this.vx = (Math.random() - 0.5) * 0.22 * this.z;
                this.vy = (Math.random() - 0.5) * 0.22 * this.z;
                this.phase = Math.random() * Math.PI * 2;
                this.speed = 0.006 + Math.random() * 0.018;

                this.color = Math.random() < 0.55
                    ? '#ffffff'
                    : STAR_PALETTE[(Math.random() * STAR_PALETTE.length) | 0];

                this.px = this.x;
                this.py = this.y;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.phase += this.speed;

                const ox = parallax.x * this.z * 26;
                const oy = parallax.y * this.z * 26;

                this.px = this.x + ox;
                this.py = this.y + oy;

                const dx = mouse.x - this.px;
                const dy = mouse.y - this.py;
                const d = Math.hypot(dx, dy);

                if (d < 170 && d > 1) {
                    const f = ((170 - d) / 170) * 0.55 * this.z;
                    this.x += (dx / d) * f;
                    this.y += (dy / d) * f;
                }

                if (this.x < -70) this.x = W + 70;
                if (this.x > W + 70) this.x = -70;
                if (this.y < -70) this.y = H + 70;
                if (this.y > H + 70) this.y = -70;
            }

            draw() {
                const tw = 0.55 + Math.sin(this.phase) * 0.45;
                ctx.globalAlpha = tw * (0.3 + this.z * 0.7);

                if (this.z > 0.55) {
                    ctx.shadowBlur = 13 * this.z;
                    ctx.shadowColor = this.color;
                }

                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.px, this.py, this.r, 0, Math.PI * 2);
                ctx.fill();

                ctx.shadowBlur = 0;
                ctx.globalAlpha = 1;
            }
        }

        const starCount = Math.min(
            130,
            Math.max(50, Math.floor((W * H) / 13000))
        );

        const stars = Array.from(
            { length: starCount },
            () => new Star()
        );

        const LINK_DIST = 128;
        const LINK_DIST_SQ = LINK_DIST * LINK_DIST;

        function connect() {
            for (let i = 0; i < stars.length; i++) {
                const a = stars[i];

                for (let j = i + 1; j < stars.length; j++) {
                    const b = stars[j];

                    const dx = a.px - b.px;
                    const dy = a.py - b.py;
                    const d2 = dx * dx + dy * dy;

                    if (d2 < LINK_DIST_SQ) {
                        const alpha = (1 - Math.sqrt(d2) / LINK_DIST) * 0.30;

                        ctx.beginPath();
                        ctx.strokeStyle = 'rgba(150, 135, 255, ' + alpha + ')';
                        ctx.lineWidth = 0.55;
                        ctx.moveTo(a.px, a.py);
                        ctx.lineTo(b.px, b.py);
                        ctx.stroke();
                    }
                }
            }
        }

        const shooters = [];
        let shootCooldown = 200;

        function spawnShooter() {
            const fromLeft = Math.random() > 0.5;
            const angle = fromLeft ? Math.PI * 0.22 : Math.PI * 0.78;
            const speed = 9 + Math.random() * 6;

            shooters.push({
                x: fromLeft ? -120 : W + 120,
                y: Math.random() * H * 0.55,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1,
                len: 120 + Math.random() * 130
            });
        }

        function updateShooters() {
            if (--shootCooldown <= 0) {
                spawnShooter();
                shootCooldown = 260 + Math.random() * 480;
            }

            for (let i = shooters.length - 1; i >= 0; i--) {
                const s = shooters[i];

                s.x += s.vx;
                s.y += s.vy;
                s.life -= 0.008;

                if (
                    s.life <= 0 ||
                    s.x < -350 ||
                    s.x > W + 350 ||
                    s.y > H + 350
                ) {
                    shooters.splice(i, 1);
                    continue;
                }

                const tailX = s.x - s.vx * (s.len / 12);
                const tailY = s.y - s.vy * (s.len / 12);

                const grad = ctx.createLinearGradient(
                    s.x, s.y, tailX, tailY
                );

                grad.addColorStop(
                    0,
                    'rgba(255, 255, 255, ' + s.life + ')'
                );

                grad.addColorStop(
                    0.35,
                    'rgba(140, 200, 255, ' + (s.life * 0.55) + ')'
                );

                grad.addColorStop(
                    1,
                    'rgba(140, 200, 255, 0)'
                );

                ctx.beginPath();
                ctx.strokeStyle = grad;
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.moveTo(s.x, s.y);
                ctx.lineTo(tailX, tailY);
                ctx.stroke();
            }
        }

        function animate() {
            ctx.clearRect(0, 0, W, H);

            parallax.x += (parallax.tx - parallax.x) * 0.055;
            parallax.y += (parallax.ty - parallax.y) * 0.055;

            for (let i = 0; i < stars.length; i++) {
                stars[i].update();
                stars[i].draw();
            }

            connect();
            updateShooters();

            requestAnimationFrame(animate);
        }

        animate();
    }

    /* =========================================================
       9. КАСТОМНЫЙ КУРСОР
       ========================================================= */
    const $dot = $('.cursor-dot');
    const $ring = $('.cursor-ring');
    const $ringDashed = $('.cursor-ring-dashed');

    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;
    let dashX = 0, dashY = 0;
    let cursorInited = false;

    window.addEventListener('mousemove', function (e) {
        dotX = e.clientX;
        dotY = e.clientY;

        if (!cursorInited) {
            ringX = dashX = dotX;
            ringY = dashY = dotY;
            cursorInited = true;
        }
    });

    function cursorLoop() {
        if ($dot.length) {
            $dot[0].style.transform =
                'translate(' + dotX + 'px, ' + dotY + 'px) translate(-50%, -50%)';
        }

        dashX += (dotX - dashX) * 0.26;
        dashY += (dotY - dashY) * 0.26;

        if ($ringDashed.length) {
            $ringDashed[0].style.left = dashX + 'px';
            $ringDashed[0].style.top = dashY + 'px';
        }

        ringX += (dotX - ringX) * 0.075;
        ringY += (dotY - ringY) * 0.075;

        if ($ring.length) {
            $ring[0].style.left = ringX + 'px';
            $ring[0].style.top = ringY + 'px';
        }

        requestAnimationFrame(cursorLoop);
    }

    cursorLoop();

});
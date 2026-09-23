$(function () {
    /*
     * 1. Анимация текста кнопок
     */
    $('.ButtonS1 .label').each(function () {
        const $label = $(this);
        const text = $label.data('text') || '';

        [...text].forEach((ch, i) => {
            $('<span>')
                .text(ch === ' ' ? '\u00A0' : ch)
                .css('--i', i)
                .appendTo($label);
        });
    });

    /*
     * 2. Канвас: звёзды, созвездия, параллакс, метеоры
     */
    const canvas = $('#starfield')[0];

    if (!canvas) {
        console.error('Canvas #starfield не найден');
        return;
    }

    const ctx = canvas.getContext('2d', { alpha: true });

    let W = 0;
    let H = 0;
    let DPR = 1;

    const mouse = {
        x: -9999,
        y: -9999
    };

    const parallax = {
        x: 0,
        y: 0,
        tx: 0,
        ty: 0
    };

    function resize() {
        DPR = Math.min(window.devicePixelRatio || 1, 2);

        W = window.innerWidth;
        H = window.innerHeight;

        canvas.width = W * DPR;
        canvas.height = H * DPR;

        $(canvas).css({
            width: W + 'px',
            height: H + 'px'
        });

        ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }

    resize();
    $(window).on('resize', resize);

    $(window).on('mousemove', function (e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;

        parallax.tx = (e.clientX / W - 0.5) * 2;
        parallax.ty = (e.clientY / H - 0.5) * 2;
    });

    $(window).on('mouseleave', function () {
        mouse.x = -9999;
        mouse.y = -9999;

        parallax.tx = 0;
        parallax.ty = 0;
    });

    const PALETTE = [
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
                : PALETTE[(Math.random() * PALETTE.length) | 0];

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
            const distance = Math.hypot(dx, dy);

            if (distance < 170 && distance > 1) {
                const force =
                    ((170 - distance) / 170) * 0.55 * this.z;

                this.x += (dx / distance) * force;
                this.y += (dy / distance) * force;
            }

            if (this.x < -70) this.x = W + 70;
            if (this.x > W + 70) this.x = -70;
            if (this.y < -70) this.y = H + 70;
            if (this.y > H + 70) this.y = -70;
        }

        draw() {
            const twinkle =
                0.55 + Math.sin(this.phase) * 0.45;

            ctx.globalAlpha =
                twinkle * (0.3 + this.z * 0.7);

            if (this.z > 0.55) {
                ctx.shadowBlur = 13 * this.z;
                ctx.shadowColor = this.color;
            }

            ctx.fillStyle = this.color;

            ctx.beginPath();
            ctx.arc(
                this.px,
                this.py,
                this.r,
                0,
                Math.PI * 2
            );
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

    /*
     * Линии созвездий
     */
    const LINK_DIST = 128;
    const LINK_DIST_SQ = LINK_DIST * LINK_DIST;

    function connectStars() {
        for (let i = 0; i < stars.length; i++) {
            const a = stars[i];

            for (let j = i + 1; j < stars.length; j++) {
                const b = stars[j];

                const dx = a.px - b.px;
                const dy = a.py - b.py;
                const distanceSquared = dx * dx + dy * dy;

                if (distanceSquared < LINK_DIST_SQ) {
                    const alpha =
                        (1 - Math.sqrt(distanceSquared) / LINK_DIST) * 0.30;

                    ctx.beginPath();
                    ctx.strokeStyle =
                        `rgba(150, 135, 255, ${alpha})`;
                    ctx.lineWidth = 0.55;

                    ctx.moveTo(a.px, a.py);
                    ctx.lineTo(b.px, b.py);
                    ctx.stroke();
                }
            }
        }
    }

    /*
     * Метеоры
     */
    const shooters = [];
    let shootCooldown = 200;

    function spawnShooter() {
        const fromLeft = Math.random() > 0.5;
        const angle = fromLeft
            ? Math.PI * 0.22
            : Math.PI * 0.78;

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
        shootCooldown--;

        if (shootCooldown <= 0) {
            spawnShooter();
            shootCooldown = 260 + Math.random() * 480;
        }

        for (let i = shooters.length - 1; i >= 0; i--) {
            const shooter = shooters[i];

            shooter.x += shooter.vx;
            shooter.y += shooter.vy;
            shooter.life -= 0.008;

            if (
                shooter.life <= 0 ||
                shooter.x < -350 ||
                shooter.x > W + 350 ||
                shooter.y > H + 350
            ) {
                shooters.splice(i, 1);
                continue;
            }

            const tailX =
                shooter.x - shooter.vx * (shooter.len / 12);

            const tailY =
                shooter.y - shooter.vy * (shooter.len / 12);

            const gradient = ctx.createLinearGradient(
                shooter.x,
                shooter.y,
                tailX,
                tailY
            );

            gradient.addColorStop(
                0,
                `rgba(255, 255, 255, ${shooter.life})`
            );

            gradient.addColorStop(
                0.35,
                `rgba(140, 200, 255, ${shooter.life * 0.55})`
            );

            gradient.addColorStop(
                1,
                'rgba(140, 200, 255, 0)'
            );

            ctx.beginPath();
            ctx.strokeStyle = gradient;
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';

            ctx.moveTo(shooter.x, shooter.y);
            ctx.lineTo(tailX, tailY);
            ctx.stroke();
        }
    }

    function animate() {
        ctx.clearRect(0, 0, W, H);

        parallax.x +=
            (parallax.tx - parallax.x) * 0.055;

        parallax.y +=
            (parallax.ty - parallax.y) * 0.055;

        $.each(stars, function (_, star) {
            star.update();
            star.draw();
        });

        connectStars();
        updateShooters();

        requestAnimationFrame(animate);
    }

    animate();

    /*
     * 3. Кастомный курсор
     */
    const $dot = $('.cursor-dot');
    const $ring = $('.cursor-ring');
    const $ringDashed = $('.cursor-ring-dashed');

    let dotX = 0;
    let dotY = 0;

    let ringX = 0;
    let ringY = 0;

    let dashX = 0;
    let dashY = 0;

    let cursorInited = false;

    $(window).on('mousemove', function (e) {
        dotX = e.clientX;
        dotY = e.clientY;

        if (!cursorInited) {
            ringX = dotX;
            dashX = dotX;

            ringY = dotY;
            dashY = dotY;

            cursorInited = true;
        }
    });

    function cursorLoop() {
        $dot.css(
            'transform',
            `translate(${dotX}px, ${dotY}px) translate(-50%, -50%)`
        );

        dashX += (dotX - dashX) * 0.26;
        dashY += (dotY - dashY) * 0.26;

        $ringDashed.css({
            left: dashX + 'px',
            top: dashY + 'px'
        });

        ringX += (dotX - ringX) * 0.075;
        ringY += (dotY - ringY) * 0.075;

        $ring.css({
            left: ringX + 'px',
            top: ringY + 'px'
        });

        requestAnimationFrame(cursorLoop);
    }

    cursorLoop();

    /*
     * 4. Кнопки: hover и 3D-наклон
     */
    $('.ButtonS1')
        .on('mouseenter', function () {
            $('body').addClass('hovering');
        })
        .on('mouseleave', function () {
            $('body').removeClass('hovering');

            $(this).css('transform', '');
        })
        .on('mousemove', function (e) {
            const $button = $(this);
            const rect = this.getBoundingClientRect();

            const nx =
                (e.clientX - rect.left) / rect.width;

            const ny =
                (e.clientY - rect.top) / rect.height;

            $button.css({
                '--mx': (nx * 100) + '%',
                '--my': (ny * 100) + '%',
                transform:
                    `perspective(900px) ` +
                    `rotateX(${(ny - 0.5) * -9}deg) ` +
                    `rotateY(${(nx - 0.5) * 9}deg) ` +
                    `translateY(-8px) ` +
                    `scale(1.045)`
            });
        });
});


$("#presentations").click(function (e) { 
    e.preventDefault();
    
    window.location.href = '/presentations'
});

$("#achievments").click(function (e) { 
    e.preventDefault();
    
    //window.location.href = '/achievments'
    alert("Coming soon...");
});
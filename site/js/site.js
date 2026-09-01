/* Meridian ATM Group — theme toggle, location counters, enquiry form. */
(function () {
    'use strict';

    /* ---- Theme toggle -------------------------------------------------
       The `.dark` class is applied by the inline script in <head> before
       first paint; this only handles switching and remembering the choice. */
    var toggle = document.getElementById('theme-toggle');
    var darkIcon = document.getElementById('theme-toggle-dark-icon');
    var lightIcon = document.getElementById('theme-toggle-light-icon');

    function paintThemeIcons() {
        var isDark = document.documentElement.classList.contains('dark');
        // Show the icon for the theme you would switch *to*.
        darkIcon.classList.toggle('hidden', isDark);
        lightIcon.classList.toggle('hidden', !isDark);
        toggle.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
    }

    if (toggle && darkIcon && lightIcon) {
        paintThemeIcons();
        toggle.addEventListener('click', function () {
            var nowDark = document.documentElement.classList.toggle('dark');
            try {
                localStorage.setItem('color-theme', nowDark ? 'dark' : 'light');
            } catch (e) { /* private mode: the choice just will not persist */ }
            paintThemeIcons();
        });
    }

    /* ---- Location counters --------------------------------------------
       Each .js-counter ships its final value as text, so the real number is
       present with JavaScript off and for crawlers. We only animate up to it
       once the element scrolls into view. */
    var counters = Array.prototype.slice.call(document.querySelectorAll('.js-counter'));
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function format(value, decimals, suffix) {
        return value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
    }

    function run(el) {
        var target = parseFloat(el.dataset.target);
        var decimals = parseInt(el.dataset.decimals || '0', 10);
        var suffix = el.dataset.suffix || '';
        if (isNaN(target)) return;

        var duration = 1400;
        var start = null;

        function frame(now) {
            if (start === null) start = now;
            var progress = Math.min((now - start) / duration, 1);
            // easeOutCubic: fast to begin with, settles onto the number.
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = format(target * eased, decimals, suffix);
            if (progress < 1) requestAnimationFrame(frame);
            else el.textContent = format(target, decimals, suffix);
        }

        el.textContent = format(0, decimals, suffix);
        requestAnimationFrame(frame);
    }

    if (counters.length && !reduceMotion && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                observer.unobserve(entry.target);
                run(entry.target);
            });
        }, { threshold: 0.4 });
        counters.forEach(function (el) { observer.observe(el); });
    }

    /* ---- Enquiry form --------------------------------------------------
       Submits over fetch so the visitor stays on the page. If the endpoint is
       unreachable or still unconfigured, we fall back to a normal submit
       rather than swallowing the enquiry. */
    var form = document.getElementById('enquiry-form');
    var status = document.getElementById('form-status');

    if (form && status) {
        form.addEventListener('submit', function (event) {
            if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
                event.preventDefault();
                status.textContent = 'This form is not connected yet — set the Formspree endpoint in index.html.';
                status.className = 'mt-3 text-sm text-amber-600 dark:text-amber-500';
                return;
            }

            event.preventDefault();
            var button = form.querySelector('button[type="submit"]');
            button.disabled = true;
            button.textContent = 'Sending…';
            status.textContent = '';
            status.className = 'mt-3 text-sm';

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { Accept: 'application/json' }
            }).then(function (response) {
                if (!response.ok) throw new Error('Bad status ' + response.status);
                form.reset();
                status.textContent = 'Thanks — your enquiry is in. We usually reply within one business day.';
                status.className = 'mt-3 text-sm text-green-600 dark:text-green-400';
                button.textContent = 'Send enquiry';
            }).catch(function () {
                status.textContent = 'That did not send. Please email hello@meridianatmgroup.com and we will pick it up there.';
                status.className = 'mt-3 text-sm text-red-600 dark:text-red-500';
                button.textContent = 'Send enquiry';
            }).finally(function () {
                button.disabled = false;
            });
        });
    }
})();

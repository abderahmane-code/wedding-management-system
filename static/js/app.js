// Wedding Management System — small bits of UI wiring.
(function () {
    "use strict";

    // Sidebar toggle on mobile
    const toggle = document.querySelector('[data-toggle-sidebar]');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.toggle('is-open');
        });
        document.addEventListener('click', function (e) {
            if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('is-open');
            }
        });
    }

    // Auto-dismiss success messages
    document.querySelectorAll('.alert-success').forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity .4s ease';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 450);
        }, 4000);
    });

    // Confirm delete forms (extra safety net)
    document.querySelectorAll('form[data-confirm]').forEach(function (form) {
        form.addEventListener('submit', function (ev) {
            if (!window.confirm(form.dataset.confirm || 'Are you sure?')) {
                ev.preventDefault();
            }
        });
    });
})();

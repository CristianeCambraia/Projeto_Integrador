document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const nav = document.querySelector('header nav');
    const navList = nav ? nav.querySelector('ul') : null;

    function closeMenu() {
        if (navList) {
            navList.classList.remove('nav-expanded');
            navList.classList.add('nav-collapsed');
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    }

    function openMenu() {
        if (navList) {
            navList.classList.remove('nav-collapsed');
            navList.classList.add('nav-expanded');
            menuToggle.setAttribute('aria-expanded', 'true');
        }
    }

    if (!menuToggle || !navList) return;

    // Inicia colapsado em telas pequenas
    if (window.innerWidth <= 768) {
        navList.classList.add('nav-collapsed');
    }

    menuToggle.addEventListener('click', function (e) {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        if (expanded) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Fecha menu ao clicar fora (em mobile)
    document.addEventListener('click', function (e) {
        const target = e.target;
        if (window.innerWidth <= 768) {
            if (!nav.contains(target) && target !== menuToggle) {
                closeMenu();
            }
        }
    });

    // Ajusta ao redimensionar
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            // garante que o menu fique visível em desktop
            navList.classList.remove('nav-collapsed', 'nav-expanded');
            menuToggle.style.display = 'none';
            navList.style.display = '';
            menuToggle.setAttribute('aria-expanded', 'false');
        } else {
            menuToggle.style.display = '';
            if (!navList.classList.contains('nav-expanded')) {
                navList.classList.add('nav-collapsed');
            }
        }
    });
});

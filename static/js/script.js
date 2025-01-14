document.querySelector('.toggle-sidebar').addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('collapsed');
    document.getElementById('content').classList.toggle('collapsed');
});

document.querySelectorAll('#sidebar .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
        document.querySelectorAll('#sidebar .nav-link').forEach(function (link) {
            link.classList.remove('active');
        });
        this.classList.add('active');
    });
});

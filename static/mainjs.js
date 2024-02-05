document.addEventListener('DOMContentLoaded', function () {
    anime({
        targets: '.animated-footer',
        translateY: [50, 0],
        opacity: [0, 1],
        easing: 'easeInOutQuad',
        duration: 1000,
        delay: 500
    });
});

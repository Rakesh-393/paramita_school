'use strict';
(function () {
    function toggleCustomPlatform() {
        var platform = document.getElementById('id_platform');
        var row = document.querySelector('.field-custom_platform');
        if (!platform || !row) return;
        row.style.display = platform.value === 'other' ? '' : 'none';
    }

    document.addEventListener('DOMContentLoaded', function () {
        var platform = document.getElementById('id_platform');
        if (!platform) return;
        toggleCustomPlatform();
        platform.addEventListener('change', toggleCustomPlatform);
    });
})();

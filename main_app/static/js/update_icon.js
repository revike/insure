window.onload = function () {
    let interval = 10000;

    function doAjax() {
        $.ajax({
            url: '/',
            success: function (data) {
                let response_len = new DOMParser().parseFromString(data, 'text/html').getElementById('response_length')
                let img = document.getElementById('header_img')
                if (response_len.innerText === '0') {
                    img.remove()
                    $('#header_images').append('<img id="header_img" class="header__img" src="/static/img/user.svg" alt="icon">')
                } else {
                    img.remove()
                    $('#header_images').append('<img id="header_img" class="header__img" src="/static/img/bell.gif" alt="icon">')
                }
            },
            complete: function () {
                setTimeout(doAjax, interval);
            }
        });
    }

    setTimeout(doAjax, interval);
}

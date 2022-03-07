window.onload = function () {
    $('.read_button').on('click', '.read_buttons', function () {
        let pk = $(this).attr('data-pk');
        if (pk) {
            $.ajax({
                url: "/cabinet/response_read/" + pk + "/",

                success: function () {
                    document.getElementById(pk).remove()
                    document.getElementById('res_' + pk).classList.remove('product_response')
                    document.getElementById('res_' + pk).classList.add('product_response_read')
                    let response = document.getElementById('response')
                    let result = $(response).text(response.innerText - 1)
                    if (result.text() === '0') {
                        $(response).remove();
                        let img = document.getElementById('header_img')
                        img.remove()
                        $('#header_images').append('<img id="header_img" class="header__img" src="/static/img/user.svg" alt="icon">')
                    }

                }
            })
        }
    })
}

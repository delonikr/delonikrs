$(document).ready(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function(data) {
                alert('Pesan berhasil dikirim!');
                form[0].reset();
            },
            error: function(data) {
                alert('Terjadi kesalahan. Silakan coba lagi.');
            }
        });
    });
});
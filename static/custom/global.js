$(document).ready(function () {


    $('.table-responsive').on('show.bs.dropdown', function () {
         $('.table-responsive').css( "overflow", "inherit" );
    });

    $('.table-responsive').on('hide.bs.dropdown', function () {
         $('.table-responsive').css( "overflow", "auto" );
    })

    $(document).on('click', '#userSessionLogout', function () {
        let buttonId = '#userSessionLogout'
        $(buttonId).prop('disabled', true);
//        $(buttonId).prop('innerText', 'Logged out');
        toastr.success("Logged out successfully");
        setTimeout(function () {
            window.location.href = '/logout'
        },1000);
    });


});
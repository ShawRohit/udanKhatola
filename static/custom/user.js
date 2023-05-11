$(document).ready(function () {
    var forgotPassEmail = localStorage.getItem("user_email");
    $('#forgotPassMsg').prop('innerText', `We sent a confirmation code to ` + forgotPassEmail + ` Please type in the confirmation code below, along with your new password`)
    $(document).on('click', '#login_btn', function () {
        let buttonId = '#login_btn'
        let email = $('#email').val();
        let password = $('#password').val();
        let formdata = new FormData();
        formdata.append("email", email);
        formdata.append("password", password);
        $.ajax({
            url: '/api/v1/web-user/login',
            type: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Logging In...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Logged In');
                    toastr.success(data.message);
                    setTimeout(function () {
                        window.location.href = '/dubbing-management';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Log In');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Log In');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

$(document).on('keypress', '.form-input', function (e) {
        console.log(e.keyCode);
        if (e.keyCode == 13) {
            let buttonId = '#login_btn'
            let email = $('#email').val();
            let password = $('#password').val();
            let formdata = new FormData();
            formdata.append("email", email);
            formdata.append("password", password);
            $.ajax({
                url: '/api/v1/web-user/login',
                type: 'POST',
                cache: false,
                processData: false,
                contentType: false,
                data: formdata,
                beforeSend: function (xhr, settings) {
                    $(buttonId).prop('disabled', true);
                    $(buttonId).prop('innerText', 'Logging In...');
                },
                success: function (data) {
                    data = JSON.parse(data);
                    if (data.status) {
                        $(buttonId).prop('disabled', false);
                        $(buttonId).prop('innerText', 'Logged In');
                        toastr.success(data.message);
                        setTimeout(function () {
                            window.location.href = '/dubbing-management';
                        }, 1000);
                    } else {
                        $(buttonId).prop('disabled', false);
                        $(buttonId).prop('innerText', 'Log In');
                        console.log("error")
                        toastr.error(data.message);
                    }
                },
                error: function (err) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Log In');
                    const data = JSON.parse(err.responseText)
                    toastr.error(data.message);
                }
            });
        }
    });

    $(document).on('click', '#btnSendForgotPassOTP', function () {
        let buttonId = '#btnSendForgotPassOTP'
        let email = $('#forgotPassEmail').val();
        let formdata = new FormData();
        formdata.append("email", email);
        $.ajax({
            url: '/api/v1/web-user/forgot-password-otp',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Sending...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Code Sent');
                    localStorage.setItem("user_email", email.toString())
                    toastr.success(data.message);
                    setTimeout(function () {
                        window.location.href = '/change-password';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Send Code');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Send Code');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

    $(document).on('click', '#btnResendForgotPassOTP', function () {
        let buttonId = '#btnResendForgotPassOTP'
        let formdata = new FormData();
        formdata.append("email", forgotPassEmail);
        $.ajax({
            url: '/api/v1/web-user/forgot-password-otp',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Resending Code...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    toastr.success(data.message);
                    $(buttonId).prop('innerText', 'Resend Code');
                    setTimeout(function () {
                        $(buttonId).prop('disabled', false);
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Resend Code');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Resend Code');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

    $(document).on('click', '#bthChangeForgotPass', function () {
        let buttonId = '#bthChangeForgotPass'
        let confCode = $('#forgotPassOTP').val();
        let newPass = $('#newPass').val();
        let confNewPass = $('#confNewPass').val();
        let formdata = new FormData();
        formdata.append("email", forgotPassEmail);
        formdata.append("conf_code", confCode);
        formdata.append("password", newPass);
        formdata.append("conf_password", confNewPass);
        $.ajax({
            url: '/api/v1/web-user/change-forgot-password',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Confirming...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Confirmed');
                    toastr.success(data.message);
                    setTimeout(function () {
                        window.location.href = '/password-reset'
                    }, 1000);
                } else {
                    $(buttonId).prop('innerText', 'Confirm');
                    $(buttonId).prop('disabled', false);
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('innerText', 'Confirm');
                $(buttonId).prop('disabled', false);
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

});
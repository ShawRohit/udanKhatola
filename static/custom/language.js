var languageID = ""
var language_icon = ""
var edit_language_icon = ""
$(document).ready(function () {
    $(document).on('click', '#addLanguage', function () {
        $('#lang_name_create').val("")
        $('#lang_region_create').prop("selectedIndex", 0);
        $('#lang_reg_lang_create').prop("selectedIndex", 0);
    });

    $(document).on("change",".change-language-status",function(e){
        var language_status = $(this).val();
        var language_data_id = $(this).attr("data-language-id")
        changeLanguageStatus(language_status, language_data_id);

    })


    $(document).on('click', '#language-filter', function () {
        let language_name = $('#language-name').val();
        let regional_language = $('#regional-language').val();
        console.log(language_name)
        console.log(regional_language)
        if (language_name == "" && regional_language == ""){
            toastr.error("Please input at least one filter option");
            return
        }
        let language_status = $('#language-filter-status').val();
        table = $('#example').DataTable();
        tables_rows_col = table.rows().nodes()
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex, rowData, cell) {
                console.log('regional_language')
                console.log(regional_language)
                console.log(data[2])
                let selected_value = $(tables_rows_col[cell]).find('select').val();
                if (data[0] != "" && data[2] == "") {
                    return (data[0].toLowerCase().includes(language_name.toLowerCase()))
                        ? true
                        : false
                } else if (data[0] == "" && data[2] != "") {
                    return (regional_language == data[2]
                        ? true
                        : false)
                } else {
                    return (data[0].toLowerCase().includes(language_name.toLowerCase()) && regional_language == data[2])
                        ? true
                        : false
                }
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
    });

    $(document).on("click", "#clear-language-filter", function (e) {
        $('#language-name').val("")
        let language_status = $('#language-filter-status').val();
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                return true
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
        // $('#regional-language').val('n/a');
        $('#regional-language').val('');
    })

    $(document).on('change', '#language_icon', function (e) {
        language_icon = this.files[0];
        $("#language_icon_text").val(language_icon["name"]);
    });

    $(document).on('change', '#edit_language_icon', function (e) {
        edit_language_icon = this.files[0];
        $("#edit_language_icon_text").val(edit_language_icon["name"]);
    });


    $(document).on('click', '#btnCreateLanguage', function () {
        let buttonId = '#btnCreateLanguage'
        let langName = $('#lang_name_create').val();
        let region = $('#lang_region_create').val();
        let regionalLang = $('#lang_reg_lang_create').val();
        let formdata = new FormData();
        formdata.append("language_name", langName);
        formdata.append("region", region);
        formdata.append("regional_language_id", regionalLang);
        formdata.append("language_icon", language_icon);
        $.ajax({
            url: '/api/v1/language/create',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Adding...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Add');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.href = '/language-management';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Add');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Add');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });
    $(document).on('click', '.btnViewEditLanguage', function () {
        languageID = $(this).attr("language-id");
        console.log(languageID)
        callLanguageDetailsAPI(languageID)
    });




    $(document).on('click', '#btnEditLanguage', function () {
        let buttonId = '#btnEditLanguage'
        let langName = $('#lang_name_edit').val();
        let region = $('#lang_region_edit').val();
        let regionalLang = $('#lang_reg_lang_edit').val();
        let formdata = new FormData();
        console.log(languageID)
        formdata.append("language_id", languageID);
        formdata.append("language_name", langName);
        formdata.append("region", region);
        formdata.append("language_icon", edit_language_icon);
        formdata.append("regional_language_id", regionalLang);
        $.ajax({
            url: '/api/v1/language/edit',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Saving Changes...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Saved Changes');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.href = '/language-management';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Confirm Changes');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Confirm Changes');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });
    $(document).on('click', '.btnViewDeleteLanguage', function () {
        languageID = $(this).attr("language-id");
        var formdata = new FormData();
        formdata.append("language_id", languageID);
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to Delete Language? This process is irreversible, and will remove ALL related data (audio recordings, video, etc)",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: '/api/v1/language/delete',
                    type: 'POST',
                    processData: false,
                    contentType: false,
                    data: formdata,

                    success: function (data) {
                        data = JSON.parse(data);
                        if (data.status) {
                            toastr.success(data.message);
                            setInterval(function () {
                                window.location.href = '/language-management';
                            }, 1000);
                        } else {
                            console.log("error")
                            toastr.error(data.message);
                        }
                    },
                    error: function (err) {
                        const data = JSON.parse(err.responseText)
                        toastr.error(data.message);
                    }
                });
            } else {
                swal("Language's data is safe");
            }
        });

    });


//    $(document).on('click', '#btnDeleteLanguage', function () {
//        let buttonId = '#btnDeleteLanguage'
//        let formdata = new FormData();
//        var languageID= $(this).attr("language-id")
//
//        formdata.append("language_id", languageID);
//        $.ajax({
//            url: '/api/v1/language/delete',
//            type: 'POST',
//            processData: false,
//            contentType: false,
//            data: formdata,
//            beforeSend: function () {
//                $(buttonId).prop('disabled', true);
//                $(buttonId).prop('innerText', 'Deleting...');
//            },
//            success: function (data) {
//                data = JSON.parse(data);
//                if (data.status) {
//                    $(buttonId).prop('disabled', false);
//                    $(buttonId).prop('innerText', 'Deleted');
//                    toastr.success(data.message);
//                    setInterval(function(){
//                        window.location.href = '/language-management';
//                    },1000);
//                }
//                else{
//                    $(buttonId).prop('disabled', false);
//                    $(buttonId).prop('innerText', 'Delete');
//                    console.log("error")
//                    toastr.error(data.message);
//                }
//            },
//            error: function (err) {
//                $(buttonId).prop('disabled', false);
//                $(buttonId).prop('innerText', 'Delete');
//                const data=JSON.parse(err.responseText)
//                toastr.error(data.message);
//            }
//        });
//    });
    $(document).on('click', '.btnViewLanguage', function () {
        languageID = $(this).attr("language-id");
        let formdata = new FormData();
        formdata.append("language_id", languageID);
        $.ajax({
            url: '/api/v1/language/affix_id',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
//                    toastr.success(data.message);
                    window.location.href = '/language-management/language';
                } else {
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });
    $(document).on('click', '.btnViewEditLangKeywords', function () {
        $('#updateKeywordValue').val($(this).attr("keyword-value"));
        $('#updateKeywordValue').attr("keyword-key", $(this).attr("keyword-key"));
        $("#lang-key-value").html($(this).attr("keyword-key"))
    });
    $(document).on('click', '#btnEditLangKeywords', function () {
        let langKeywordTable = document.getElementById("langKeywordTable");
        let langKeywordObj = {}
        let langKeywordKey = $('#updateKeywordValue').attr("keyword-key").toString()
        let langKeywordVal = $('#updateKeywordValue').val()
        console.log(langKeywordVal)
        if (langKeywordVal == '') {
            console.log("ok")
            toastr.error('Please enter the text');
            return false;
        }else if(Number(langKeywordVal)){
            toastr.error('Please enter a valid input');
            return false;
        }
        for (var i = 0, row; row = langKeywordTable.rows[i]; i++) {
            if (i > 0) {
                if (row.cells[0].innerText.toString() == langKeywordKey) {
                    row.cells[1].innerText = langKeywordVal
                    langKeywordObj[row.cells[0].innerText.toString()] = langKeywordVal
                } else {
                    langKeywordObj[row.cells[0].innerText.toString()] = row.cells[1].innerText.toString()
                }
            }
        }
//        console.log(langKeywordObj)
        let buttonId = '#btnEditLangKeywords'
        let formData = new FormData();
        formData.append("language_keywords", JSON.stringify(langKeywordObj));
        $.ajax({
            url: '/api/v1/language/update_keywords',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            beforeSend: function () {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Saving Changes...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Saved Changes');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.href = '/language-management/language';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Confirm Changes');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Confirm Changes');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

});

function callLanguageDetailsAPI(languageID) {
    var formData = new FormData();
    formData.append('language_id', languageID);

    $.ajax({
        async: true,
        type: "POST",
        url: "/api/v1/language/details",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        beforeSend: function () {
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status) {
                setDataInEditLanguageModal(data.data)
            } else {
                toastr.error(data.message)
                return false;
            }
        },
        error: function (request, status, error) {
            toastr.error("Internal Server Error")
            return false;
        }
    });
}

function setDataInEditLanguageModal(details) {
    $('#lang_name_edit').val(details.language_name)
    var icon_link = details['language_icon_path'].split("/")
    $('#edit_language_icon_text').val(icon_link[icon_link.length - 1].slice(11))
    $("#lang_region_edit > option").each(function () {
        if ($(this).val().toString() == details.region) {
            $('#lang_region_edit').prop("selectedIndex", $(this).prop("index"));
        }
    });
    $("#lang_reg_lang_edit > option").each(function () {
        if ($(this).val().toString() == details.regional_language_id) {
            $('#lang_reg_lang_edit').prop("selectedIndex", $(this).prop("index"));
        }
    });
}

function changeLanguageStatus(language_status, language_id) {
        let formdata = new FormData();
        formdata.append("language_status", language_status);
        formdata.append("language_id", language_id);
        $.ajax({
            url: '/api/v1/language/update-language-status',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {


                if (data == "true") {
                    console.log("heheheh")
                    let success_msg = '';
                    if (language_status == "Active") {
                        success_msg = "Language activated successfully";
                    } else if ((language_status == "Inactive")) {
                        success_msg = "Language deactivated successfully";
                    }
                    toastr.success(success_msg);
                    setInterval(function () {
                        window.location.reload();
                        console.log("-----------")
                    }, 1000);
                } else {
                    data = JSON.parse(data);
                    console.log(data)
                    console.log("--------------")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                data = JSON.parse(data);
                console.log(data)
                console.log("--------------22")
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });

    }
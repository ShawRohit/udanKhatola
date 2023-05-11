var languageID = ""
var seriesThumbnail = ""
var seriesLanguageThumbnail = ""
var editThumbnail = ""
toastr.options = {
    "preventDuplicates": true,
    "preventOpenDuplicates": true
};
var lower_range = 0;
var higher_range = 1000;


$(document).ready(function () {


    $("#add_series_position").on('keydown', function (e) {
        if ($("#add_series_position").val() > 10000 && e.keyCode != 8) {
            e.preventDefault();
            return;

        }
        console.log($("#add_series_position").val());
    });

    $("#edit_series_position").on('keydown', function (e) {
        if ($("#edit_series_position").val() > 10000 && e.keyCode != 8) {
            e.preventDefault();
            return;
        }

    });


    window.onload = function () {
        console.log("clciked")
        var reloading = sessionStorage.getItem("language-added");
        if (reloading) {
            console.log("here")
            sessionStorage.removeItem("language-added");
            $(".manage-language-tab").click();
        }
    }

    var s3 = $("#ranged-value").freshslider({
        range: true,
        step: 1,
        value: [0, 200],
        max : 500,
        slide: function (event, ui) {
            console.log(ui)
            if ((ui.values[0] + 20) >= ui.values[1]) {
                return false;
            }
        },
        onchange: function (low, high) {
            lower_range = low;
            higher_range = high;
            if (lower_range >= higher_range) {
                console.log("enter")
                return false
            }

        }

    });

    function resetViewFilter() {
        s3 = $("#ranged-value").freshslider({
            range: true,
            step: 1,
            value: [0, 200],
            max : 500,
            slide: function (event, ui) {
                console.log(ui)
                if ((ui.values[0] + 20) >= ui.values[1]) {
                    return false;
                }
            },
            onchange: function (low, high) {
                lower_range = low;
                higher_range = high;
                if (lower_range >= higher_range) {
                    console.log("enter")
                    return false
                }

            }

        });
    }


//Create master series tag


//************************end master series tag***************

//Create master series tag

//****************************************
//Create master series tag
// var tags = $('#episode-tags').inputTags({
//            tags: [],
//            autocomplete: {
//                values: []
//            },
//
//        });
//
//        $('#episode-tags').inputTags('tags', '', function (tags) {
//            $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
//        });
//
//var autocomplete = $('#episode-tags').inputTags('options', 'autocomplete');
//$('span', '#autocomplete').text(autocomplete.values.join(', '));
//****************************************


    $(document).on('click', '.close-add-edit-modal', function () {
        $(this).attr("data-id", "")
        $("#add-language-name").val("");
        $("#title").val("");
        $("#language_thumbnail_name").val("");
        $("#language_description").val("");
        $("#modal-heading").text("Add Language Support for Series");
        let tags = $("#tags1").val();
        $(".close-item").click();
        $("#add-language-support").attr("data-language-id", "");
    });


    // $(".close-video-player")

    $(document).on('click', '.episode-video-icon', function (e) {
        console.log("Video button paused");
        var episode_name = $(this).attr("data-episode-title");
        var episode_video = $(this).attr("data-video-url");
        console.log(episode_video)
        $("#episode-video > source").attr("src", episode_video);
        $("#episode-video").load();
        if (episode_name.length > 50){

            $("#exampleModalLongTitle").text(episode_name.substr(0,50)+'...');
        }else{
            $("#exampleModalLongTitle").text(episode_name)
        }

        $("#video-src").attr('src', episode_video);
        $('#exampleModalCenter').modal('show');
        e.stopPropagation();
    });


    $(document).on('click', '.close-video-player', function (e) {
        var video = document.getElementById("episode-video");

        video.pause();
        video.currentTime = 0;

        // $("#episode-video ").pause();
        // $("#episode-video ").currentTime = 0;
        // video.pause();
        //   video.currentTime = 0;

        $('#exampleModalCenter').modal('hide');
    });


    $(document).on('click', '.edit-series-language', function () {
        var language_id = $(this).attr("language-id")
        $('#add-language-support').attr("data-language-id", language_id)
        $("#modal-heading").text("Edit Language Support for Series");
        callSeriesLanguageDetailsAPI(language_id, "edit");

    });

    $(document).on('click', '.view-series-language', function () {
        var language_id = $(this).attr("language-id")
        $('#add-language-support').attr("data-language-id", language_id)
        $("#modal-heading").text("View Language Support for Series");
        callSeriesLanguageDetailsAPI(language_id, "view");

    });

//    $(document).on('click', '.view-series-language', function () {
//        var language_id = $(this).attr("language-id")
//        $('#add-language-support').attr("data-language-id",language_id)
//        $("#modal-heading").text("Edit Language Support for Series");
//        callSeriesLanguageDetailsAPI(language_id , "view");
//
//    });


    $(document).on('click', '.text-reset', function () {
        clearAddSeriesModal();
    });


    $(document).on('click', '.close-add-master-episode-modal', function () {
        $("#master_episode").val("");
        $("#episode_position").val("");
        $("#master_episode_title").val("");
        $("#add_episode_thumbnail").val("");
        $("#add_episode_video").val("");
        $("#add_episode_audio").val("");
        $("#episode-thumbnail").val("");
        $("#episode-thumbnail_video").val("");
        $("#episode-thumbnail_audio").val("");
        $("#master_episode_description").val("");
        $(".close-item").click();
    })


    $(document).on('click', '.close-add-series-modal', function () {
        clearAddSeriesModal();

    })

    $(document).on('change', '#language_thumbnail', function (e) {
        seriesLanguageThumbnail = this.files[0];
        console.log(this.files[0].name);
        console.log(this.files[0]['name']);
        $("#language_thumbnail_name").val(this.files[0].name)
    });

    $(document).on('click', '#add-language-support', function () {
        let series_id = $(this).attr("data-id")
        let language_id1 = $("#add-language-name").val();
        // let language_name_id = $("#add-language-name").text();
        let language_name = $("#add-language-name option:selected").text();
        let title = $("#title").val();
        let description = $("#language_description").val();
//        let tags = $("#tags1").val();
        let language_id = $(this).attr("data-language-id");
        createLangugageForSeries(language_id, series_id, language_name, title, description, language_id1);
    });


    $(document).on("click", ".delete-series-language", function () {
        let language_id = $(this).attr("data-language-id")
        console.log(language_id)
        deleteSeriesLanguageSupport(language_id);

    })


    $(document).on("click", "#btn-series-filer", function () {
        let title = $("#filter-title").val();
        let tag = $("#tags").val();
        console.log(status)
        console.log("****************")
        console.log(lower_range);
        console.log(higher_range);
        console.log("*****************")
        table = $('#example').DataTable();
//        getSeriesFilterData(title,tag,status);
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                console.log(data[5])
                if (data[1] == "") {
                    return data[4] >= lower_range && data[4] <= higher_range
                        ? true
                        : false
                } else if (data[1] != "") {
                    return data[1].toLowerCase().includes(title.toLowerCase()) && (data[4] >= lower_range && data[4] <= higher_range)
                        ? true
                        : false
                }

            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
    });

    $(document).on("click", "#btn-clear-filer", function () {
        $("#filter-title").val("");
        $("#tags").val("");
        console.log(status)
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                return true
            }
        );
        table.draw();
        resetViewFilter();
        $.fn.dataTable.ext.search.pop();
    })


    $(document).on("click", ".delete-series", function () {
        let series_id = $(this).attr("data-series-id")
        deleteSeries(series_id);

    })

    $(document).on('click', "#btnEditSeries", function () {
        let buttonId = '#btnEditSeries'
        let editseriesName = $.trim($('#edit_series_name').val());
        let editseriestags = $.trim($('#tags5').val());
        let editedImage = $('#edit-thumbnail-img').attr("src");
        let series_id = $('#btnEditSeries').attr("data-id");

        let formdata = new FormData();
        formdata.append("series_name", editseriesName);
        formdata.append("editseriestags", editseriestags);
        formdata.append("series_thumbnail", editedImage);
        formdata.append("editThumbnail", editThumbnail);
        formdata.append("series_id", series_id);
        $.ajax({
            url: '/api/v1/series/edit',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Creating...');
                $(".custom_loader").show();
            },
            success: function (data) {
                $(".custom_loader").hide();
//                data = JSON.parse(data);
                if (data.status) {
                    console.log(data)

                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Created');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.href = '/dubbing-management';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Create');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(".custom_loader").hide();
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Create');
                const data = JSON.parse(err.responseText)
                toastr.error("Something went wrong");
            }
        });
    });

    $(document).on('change', '.series_status', function (e) {
        e.stopPropagation();
        let series_status = $(this).val()
        let series_id = $(this).attr("data-id");
        changeSeriesStatus(series_status, series_id);
    });

    $(document).on('change', '.series-language-status', function (e) {
        e.stopPropagation();
        let series_language_status = $(this).val()
        let language_id = $(this).attr("data-id");
        changeSeriesLanguageStatus(series_language_status, language_id);
    });


    $(document).on('click', '.series_list', function () {
        let series_id = $(this).attr("data-id");
        console.log(series_id);
        window.location.href = "/series-management/" + series_id

    });

    $(document).on('change', '#add_series_thumbnail', function (e) {
        seriesThumbnail = this.files[0];
        $("#add-series-thumbnail-text").val(seriesThumbnail["name"])
    });

    $(document).on('change', '#edit_series_thumbnail', function (e) {
        editThumbnail = this.files[0];
        $("#edit-series-thumbnail-text").val(editThumbnail["name"])
    });


    $(document).on('click', '.edit-series', function () {
        console.log("calleld")
        seriesId = $(this).attr("data-series-id");
        console.log(seriesId);
        callSeriesDetailsAPI(seriesId)
    });


    $(document).on('click', '#btnCreateSeries', function () {
        console.log("called---")
        let buttonId = '#btnCreateSeries'
        let seriesName = $.trim($('#add_series_name').val());
        let seriesPosition = $.trim($('#add_series_position').val());
        let series_tags = $.trim($('#tags4').val());
        let existingImage = $('#edit-thumbnail-img').attr("src");
        let formdata = new FormData();
        formdata.append("series_name", seriesName);
        formdata.append("series_position", seriesPosition);
        formdata.append("series_thumbnail", seriesThumbnail);
        formdata.append("series_tags", series_tags);
        $.ajax({
            url: '/api/v1/series/create',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Creating...');
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Created');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.href = '/dubbing-management';
                    }, 1000);
                } else {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Create');
                    console.log("error")
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Create');
                const data = JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });
    });

    function changeSeriesStatus(series_status, series_id) {
        console.log("called")
        let formdata = new FormData();
        formdata.append("series_status", series_status);
        formdata.append("series_id", series_id);
        $.ajax({
            url: '/api/v1/series/update-series-status',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {

                if (data) {
                    console.log("success" + data)
                    console.log("success" + series_status)
                    let success_msg = '';
                    if (series_status == "Active") {
                        success_msg = "Series activated succesfully";
                    } else if ((series_status == "Deactivated")) {
                        success_msg = "Series deactivated succesfully";
                    } else if (series_status == "In Progress") {
                        success_msg = "Series paused succesfully";
                    }
                    toastr.success(success_msg);
                    setInterval(function () {
                        window.location.href = '/dubbing-management';
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

    function changeSeriesLanguageStatus(language_status, language_id) {
        console.log("called")
        let formdata = new FormData();
        formdata.append("language_status", language_status);
        formdata.append("language_id", language_id);
        $.ajax({
            url: '/api/v1/series/update-series-language-status',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {

                if (data) {
                    console.log("success" + data)
                    console.log("success" + language_status)
                    let success_msg = '';
                    if (language_status == "Active") {
                        success_msg = "Language activated succesfully";
                    } else if ((language_status == "Deactivated")) {
                        success_msg = "Language deactivated succesfully";
                    } else if (language_status == "In Progress") {
                        success_msg = "Language paused succesfully";
                    }
                    toastr.success(success_msg);
                    // setInterval(function () {
                    //     window.location.reload();
                    //     console.log("-----------")
                    // }, 1000);
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

    function callSeriesDetailsAPI(seriesId) {
        var formData = new FormData();
        console.log("function called");
        formData.append('series_id', seriesId);

        $.ajax({
            async: true,
            type: "POST",
            url: "/api/v1/series/details",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function () {
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    console.log(data)
                    setDataInEditSeriesModal(data)
                    console.log(data);
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

    function callSeriesLanguageDetailsAPI(language_id, task) {
        var formData = new FormData();
        console.log("function called");
        formData.append('language_id', language_id);

        $.ajax({
            async: true,
            type: "POST",
            url: "/api/v1/series/series-language-details",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function () {
            },
            success: function (data) {
                data = JSON.parse(data);
                console.log(data)
                if (data.status) {
                    console.log(data)
                    if (task == "edit") {
                        setDataInEditSeriesLanguageModal(data)
                        console.log(data);
                    } else {
                        setDataInViewSeriesLanguageModal(data)
                        console.log(data);
                    }

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

    function setDataInViewSeriesLanguageModal(data) {
        console.log(data)
        console.log("==============")
//        console.log(data.tags);
//        console.log(typeof (data.tags));
        $("#view-language-name").attr("disabled", true);
//        $(".close-item").click()
//        var tags_array = data.tags.split(",");
//        tags_array.forEach(function (item) {
//            $('#tags2').inputTags('tags', item, function (tags) {
//                $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
//            });
//        });
//        console.log("============");
//        var image_link = data.thumbnail.split("/")

        $("#view-title").val(data.title)
//        $("#view_language_thumbnail").attr("disabled",true);
//        $("#view_language_thumbnail_name").val(image_link[image_link.length - 1].slice(11));
        $("#view_language_description").val(data.description)
        $("#view-language-name > option").each(function () {
            if ($(this).text().toString() == data.language_name) {
                $('#view-language-name').prop("selectedIndex", $(this).prop("index"));
            }
        });
//        $("#add-language-support").hide();
    }


    function setDataInEditSeriesLanguageModal(data) {
        $("#offcanvasEndLabel").text("");
        $("#add-language-name").attr("disabled", false);
//        console.log(typeof (data.tags));
//        var tags_array = data.tags.split(",")
//        $(".close-item").click()
//        tags_array.forEach(function (item) {
//            $('#tags1').inputTags('tags', item, function (tags) {
//                $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
//            });
//        });
//        var image_link = data.thumbnail.split("/")
        $("#title").val(data.title)
//        $("#language_thumbnail_name").val(image_link[image_link.length - 1].slice(11));
        $("#language_description").val(data.description)
        $("#add-language-name > option").each(function () {
            if ($(this).text().toString() == data.language_name) {
                $('#add-language-name').prop("selectedIndex", $(this).prop("index"));
            }
        });

    }


    function setDataInEditSeriesModal(details) {
        var image_link = details['series_thumbnail'].split("/")
        $('#edit_series_name').val(details['series_name'])
        $('#edit_series_position').val(details['series_position'])
        $('#edit-series-thumbnail-text').val(image_link[image_link.length - 1].slice(11))
        $('#btnEditSeries').attr("data-id", details['id'])
        $(".close-item").click()
        var tags_array = details.series_tags.split(",")
        tags_array.forEach(function (item) {
            $('#tags5').inputTags('tags', item, function (tags) {
                $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
            });
        });
    }

    function deleteSeries(series_id) {

        console.log(series_id);
        var formdata = new FormData();
        formdata.append("series_id", series_id);
//      var token = $("#acess-token").val();
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to Delete Series? This process is irreversible, and will remove ALL related data (audio recordings, video, etc)",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/api/v1/series/delete",
                    method: "POST",
                    data: formdata,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        data = JSON.parse(data);
                        console.log(typeof (data))
                        console.log(data.status)
                        if (data.status) {
                            console.log(data)
                            swal("Series deleted", {
                                icon: "success",
                            });
                            setTimeout(function () {
                                window.location.href = '/dubbing-management';
                            }, 1000);

                        } else {
                            swal("Cannot delete", {
                                icon: "error",
                            });
                        }
                    }
                });
            } else {
                swal("Series's data is safe");
            }
        });
    }

    function deleteSeriesLanguageSupport(language_id) {

        console.log(language_id);
        var formdata = new FormData();
        formdata.append("language_id", language_id);
//      var token = $("#acess-token").val();
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to Delete language support? This process is irreversible, and will remove ALL related data (audio recordings, video, etc)",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/api/v1/series/delete-language-support",
                    method: "POST",
                    data: formdata,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        data = JSON.parse(data);
                        console.log(typeof (data))
                        console.log(data.status)
                        if (data.status) {
                            console.log(data)
                            swal("Language deleted", {
                                icon: "success",
                            });
                            setTimeout(function () {
                                window.location.reload();
                            }, 1000);

                        } else {
                            swal("Cannot delete", {
                                icon: "error",
                            });
                        }
                    }
                });
            } else {
                swal("Language's data is safe");
            }
        });
    }

    function createLangugageForSeries(language_id, series_id, language_name, title, description, languageId) {
        let buttonId = "#add-language-support"
        let formData = new FormData();
        formData.append("language_id", language_id)
        formData.append("languageId", languageId)
        formData.append("series_id", series_id)
        formData.append("language_name", language_name)
        formData.append("title", title)
        formData.append("description", description)

        if (language_name == "") {
            toastr.error("Please select the language");
            return false;
        } else if (title == "") {
            toastr.error("Please enter the title");
            return false;
        } else if (description == "") {
            toastr.error("Please enter the description");
            return false;
        } else {
            $.ajax({
                async: true,
                type: "POST",
                url: "/api/v1/series/add-language",
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                beforeSend: function (xhr, settings) {
                    $(buttonId).prop('disabled', true);
                    $(".custom_loader").show();
                    $(buttonId).prop('innerText', 'Creating...');


                },
                success: function (data) {
                    $(".custom_loader").hide();
                    data = JSON.parse(data);
                    if (data.status) {
                        console.log(data)
                        toastr.success(data.message);
                        setTimeout(function () {
//                add_data_to_dataTable(data);
                            sessionStorage.setItem("language-added", "true");
                            window.location.reload();
                            console.log(data)
                        }, 1000);


                        console.log(data);
                    } else {
                        $(buttonId).prop('disabled', false);
                        $(buttonId).prop('innerText', 'Create');
                        toastr.error(data.message)
                        return false;
                    }
                },
                error: function (request, status, error) {
                    $(".custom_loader").hide();
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Create');
                    toastr.error("Internal Server Error")
                    return false;
                }
            });

        }


    }


    function clearAddSeriesModal() {
        $('#add_series_name').val("");
        $('#add_series_position').val("")
        $('#add_series_thumbnail').val("")
        $('#add-series-thumbnail-text').val("")
        $("#tags4").val("");
        $(".inputTags-field").val("");
    }

    function add_data_to_dataTable(data) {
        var row_to_added = `<tr>
                                <td>"data["data"]["language_name"]"</td>
                            </tr>`;

        $("#language-management-table").append(row_to_added);
    }





});

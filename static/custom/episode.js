var languageID = ""
var episodeThumbnail = ""
var addepisodeVideo = ""
var addepisodeAudio = ""
var editThumbnail = ""
var editEpisodeThumbnail = "";
var editEpisodeVideo = "";
var editEpisodeAudio = "";
var episode_view_lower_range = 1;
var episode_view_higher_range = 100;


var episodeAudio = "";
var episodeThumbnail1 = "";
var episodeVideo = "";


$(document).ready(function () {


    var s3 = $("#ranged-value").freshslider({
        range: true,
        step: 1,
        value: [0, 200],
        max : 500,
        onchange: function (low, high) {
            episode_view_lower_range = low;
            episode_view_higher_range = high;

        }

    });

     $("#episode_position").on('keydown',function(e){
        if ($("#episode_position").val()> 10000 && e.keyCode != 8){
            e.preventDefault();
            return;

        }

      });

    $("#edit-episode_position").on('keydown',function(e){
        if ($("#edit-episode_position").val()> 10000 && e.keyCode != 8){
            e.preventDefault();
            return;
        }

      });


    $(document).on("click", ".episode-name", function () {
        var episode_id = $(this).attr("data-id");
        console.log("_________")
        console.log(episode_id)
        window.location.href = "/episode-management/" + episode_id;
    })

    $(document).on('click','.no-content',function(e){
            toastr.error("No content found")
            e.stopPropagation();

        })


    $(document).on("click", "#episode-filter", function () {
        let title = $("#filter-episode-title").val();
        let tag = $("#tags").val();
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {

                if (data[1] == "") {
                    return data[3] >= episode_view_lower_range && data[3] <= episode_view_higher_range
                        ? true
                        : false
                } else if (data[1] != "") {
                    return data[1].toLowerCase().includes(title.toLowerCase()) && (data[3] >= episode_view_lower_range && data[3] <= episode_view_higher_range)
                        ? true
                        : false
                }
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
        $(".btn-close").click();
    })

    $(document).on("click", "#episode-clear-filter", function () {


        $("#filter-episode-title").val("");
        $("#tags").val("");
        resetViewFilter()
        console.log(status)
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                return true
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
    })


    $(document).on("click", "#dubbed-episode-filter", function () {
        let language = $("#episode-dubbed-language").val();
        let title = $("#episode-dubbed-title").val();
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {

                if (data[0] == "" && data[2] != "") {
                    return data[2].toLowerCase().includes(title.toLowerCase())
                        ? true
                        : false
                } else if (data[0] != "" && data[2] == "") {
                    return data[0].toLowerCase().includes(language.toLowerCase())
                        ? true
                        : false
                }else{
                    return data[0].toLowerCase().includes(language.toLowerCase()) && data[2].toLowerCase().includes(title.toLowerCase())
                        ? true
                        : false

                }
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
        $(".btn-close").click();
    })

    $(document).on("click", "#cancel-dubbed-episode-filter", function () {

        $("#episode-dubbed-language").val("");
        $("#episode-dubbed-title").val("");
        table = $('#example').DataTable();
        $.fn.dataTable.ext.search.push(
            function (settings, data, dataIndex) {
                return true
            }
        );
        table.draw();
        $.fn.dataTable.ext.search.pop();
        $(".btn-close").click();
    })


    $(document).on('click', '#addSeries', function () {
        $('#add_series_name').val("");
        $('#add_series_position').val("")
        $('#add_series_thumbnail').val("")
    });

    $(document).on('click', '.edit-episode', function () {
        console.log("calleld")
        episodeId = $(this).attr("data-id");
        console.log(episodeId);
        callEditEpisodeDetailsAPI(episodeId, "edit")
    });

    $(document).on('click', '.view-episode', function () {
        console.log("calleld")
        episodeId = $(this).attr("data-id");
        console.log(episodeId);
        callEditEpisodeDetailsAPI(episodeId, "view")
    });

    $(document).on('change', '.episode_status', function (e) {
        e.stopPropagation();
        let episode_status = $(this).val()
        let episode_id = $(this).attr("data-id");
        changeEpisodeStatus(episode_status, episode_id);

    });
    $(document).on("click", ".delete-episode", function () {
        let episode_id = $(this).attr("data-episode-id")
        deleteEpisode(episode_id);

    })


    $(document).on('change', '#add_episode_thumbnail', function (e) {
        console.log("okay")
        episodeThumbnail = this.files[0];
        $("#episode-thumbnail").val(episodeThumbnail['name'])
        console.log(episodeThumbnail['type'].split("/")[0])
        console.log(episodeThumbnail)
    });
    $(document).on('change', '#add_episode_audio', function (e) {
        console.log("okay")
        addepisodeAudio = this.files[0];
        $("#episode-thumbnail_audio").val(addepisodeAudio['name'])
    });

    $(document).on('change', '#add_episode_video', function (e) {
        console.log("okay")
        addepisodeVideo = this.files[0];
        $("#episode-thumbnail_video").val(addepisodeVideo['name'])
    });


    $(document).on('click', ".cancel-episode", function () {
        $("#master_episode").val("");
        $("#add_episode_thumbnail").val("");
        $("#episode-thumbnail").val("");
        $("#episode_position").val("");
        $(".close-item").click();
    })

    $(document).on('click', ".btn-close", function () {
        $("#master_episode").val("");
        $("#add_episode_thumbnail").val("");
        $("#episode-thumbnail").val("");
        $("#episode_position").val("");
        $(".close-item").click();
    })

    $(document).on('click', ".cancel-episode", function () {
        $("#master_episode").val("");
        $("#add_episode_thumbnail").val("");
    })

    $(document).on('click', '#btnCreateEpisode', function () {
        console.log("Clled")
        let buttonId = '#btnCreateEpisode'
        let series_id = $(this).attr("data-series-id");
        let episodeName = $.trim($('#master_episode').val());
        let episodeTitle = $.trim($('#master_episode_title').val());
        let episodeDescription = $.trim($('#master_episode_description').val());
        let episode_position = $.trim($('#episode_position').val());
        let episodetags = $.trim($('#tags4').val());
        let formdata = new FormData();
        console.log(episodeThumbnail);
        formdata.append("episode_name", episodeName);
        formdata.append("episodeTitle", episodeTitle);
        formdata.append("episodeDescription", episodeDescription);
        formdata.append("episode_thumbnail", episodeThumbnail);
        formdata.append("addepisodeAudio", addepisodeAudio);
        formdata.append("addepisodeVideo", addepisodeVideo);
        formdata.append("series_id", series_id);
        formdata.append("episode_position", episode_position);
        formdata.append("episodetags", episodetags);
        let validation_res = validateEpisodeInput(episodeName,episodeTitle,episodeDescription,episodeThumbnail,addepisodeAudio,addepisodeVideo,episode_position,episodetags)
        if (validation_res){
                    $.ajax({
            url: '/api/v1/episode/create',
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

                data = JSON.parse(data);
                if (data.status) {
                    $(".custom_loader").hide();
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Created');
                    toastr.success(data.message);
                    clear_add_episode_modal();
//                    $(".btn-close").click();
                    window.location.reload();

                } else {
                    $(".custom_loader").hide();
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
//                const data = JSON.parse(err.responseText)
                toastr.error(err);
            }
        });
        }else{
            console.log(validation_res)
        }
    });


    $(document).on('change', '#edit_episode_thumbnail', function (e) {
        editThumbnail = this.files[0];
        $("#edit-episode-thumbnail").val(editThumbnail["name"]);
    });
    $(document).on('change', '#edit_episode_video', function (e) {
        editEpisodeVideo = this.files[0];
        $("#edit_episode_video_name").val(editEpisodeVideo["name"]);
    });
    $(document).on('change', '#edit_episode_audio', function (e) {
        editEpisodeAudio = this.files[0];
        $("#edit_episode_audio_name").val(editEpisodeAudio["name"]);
    });

    $(document).on('click', "#btnEditEpisode", function () {
        console.log("function ")
        let buttonId = '#btnEditEpisode'
        let editEpisodesName = $.trim($('#edit_master_episode').val());
        let editedImage = $('#edit-episode-thumbnail').attr("src");
        let episode_id = $('#btnEditEpisode').attr("data-episode-id");
        let episode_position = $('#edit-episode_position').val();
        let episode_title = $('#edit_master_episode_title').val();
        let episode_description = $('#edit_master_episode_description').val();
        let episode_tags = $('#tags5').val();
        let formdata = new FormData();
        formdata.append("episode_name", editEpisodesName);
        formdata.append("episode_title", episode_title);
        formdata.append("episode_description", episode_description);
        formdata.append("prev_episode_thumbnail", editedImage);
        formdata.append("current_episode_thumbnail", editThumbnail);
        formdata.append("episode_audio", editEpisodeAudio);
        formdata.append("episode_video", editEpisodeVideo);
        formdata.append("episode_id", episode_id);
        formdata.append("episode_position", episode_position);
        formdata.append("episode_tags", episode_tags);
        $.ajax({
            url: '/api/v1/episode/edit',
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
//                data = JSON.parse(data);

                if (data.status) {
                    $(".custom_loader").hide();
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Created');
                    toastr.success(data.message);
                    setInterval(function () {
                        window.location.reload();
                    }, 1000);
                } else {
                    $(".custom_loader").hide();
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


    function clear_add_episode_modal() {
        $("#master_episode").val("");
        $("#add_episode_thumbnail").val("");
    }

    function callEditEpisodeDetailsAPI(episodeId, task) {
        var formData = new FormData();
        console.log("function called");
        formData.append('episode_id', episodeId);

        $.ajax({
            async: true,
            type: "POST",
            url: "/api/v1/episode/details",
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
                    setDataInEditSeriesModal(data, task)
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

    function setDataInEditSeriesModal(details, task) {

        if (task == "view") {
            $("#edit-view-modal-title").text("View episode")
            $("#btn-edit-view").hide()
            $('#edit_master_episode').attr("readonly", true)
            $('#edit-episode-thumbnail').attr("readonly", true)
            $('#edit-episode_position').attr("readonly", true)
            $('#edit_master_episode_title').attr("readonly", true)
            $('#edit_master_episode_description').attr("readonly", true)
            $('.inputTags-field').attr("readonly", true)
             $('#edit-episode-thumbnail').attr("readonly", true)
            $('#edit_episode_video_name').attr("readonly", true)
            $('#edit_episode_audio_name').attr("readonly", true)
            $("#edit_episode_thumbnail").attr("disabled", true)
            $("#edit_episode_video").attr("disabled", true)
            $("#edit_episode_audio").attr("disabled", true)
        } else {
            $("#btn-edit-view").show()
            $("#edit-view-modal-title").text("Edit episode")
            $('#edit_master_episode').attr("readonly", false)
            $('#edit-episode-thumbnail').attr("readonly", false)
            $('#edit-episode_position').attr("readonly", false)
            $('#edit_master_episode_title').attr("readonly", false)
            $('#edit_master_episode_description').attr("readonly", false)
            $('#edit-episode-thumbnail').attr("readonly", true)
            $('#edit_episode_video_name').attr("readonly", true)
            $('#edit_episode_audio_name').attr("readonly", true)
            $('.inputTags-field').attr("readonly", false)
            $("#edit_episode_thumbnail").attr("disabled", false)
            $("#edit_episode_video").attr("disabled", false)
            $("#edit_episode_audio").attr("disabled", false)
        }
        // var image_link = details['episode_thumbnail'].split("/")
        // var video_link = details['episode_video'].split("/")
        var image_link = "";
        var video_link = "";
        var audio_link = "";

        if (details['episode_thumbnail'] != null  ){

            console.log(details['episode_thumbnail'])
            image_link = details['episode_thumbnail'].split("/")
        }

        if (details['episode_video'] != null  ){

            console.log(details['episode_video'])
            video_link = details['episode_video'].split("/")
        }

        if (details['episode_audio'] != null  ){

            console.log(details['episode_audio'])
            audio_link = details['episode_audio'].split("/")
        }



        $('#edit_master_episode').val(details['episode_name'])
        $('#btnEditEpisode').attr("data-episode-id", details['id'])
        // $('#edit-episode-thumbnail').val(image_link[image_link.length - 1].slice(11))
        // $('#edit_episode_video_name').val(video_link[video_link.length - 1].slice(11))

        if (details['episode_thumbnail'] != null ){
            $('#edit-episode-thumbnail').val(image_link[image_link.length - 1].slice(11))
        }else{
            $('#edit-episode-thumbnail').val("")
        }

        if (details['episode_video'] != null ){
            $('#edit_episode_video_name').val(video_link[video_link.length - 1].slice(11))
        }else{
            $('#edit_episode_video_name').val("")
        }

        if (details['episode_audio'] != null ){
            $('#edit_episode_audio_name').val(audio_link[audio_link.length - 1].slice(11))
        }else{
            $('#edit_episode_audio_name').val("")
        }

        $('#edit-episode_position').val(details['episode_position'])
        $('#edit_master_episode_title').val(details['episode_title'])
        $('#edit_master_episode_description').val(details['episode_description'])
        var tags_array = details["episode_tags"].split(",")

        tags_array.forEach(function (item) {
            $('#tags5').inputTags('tags', item, function (tags) {
                $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
            });
        });
        console.log("============");
    }

    function changeEpisodeStatus(episode_status, episode_id) {
        console.log("called")
        let formdata = new FormData();
        formdata.append("episode_status", episode_status);
        formdata.append("episode_id", episode_id);
        $.ajax({
            url: '/api/v1/episode/update-episode-status',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {

                if (data) {
                    let success_msg = '';
                    if (episode_status == "Active") {
                        success_msg = "Episode activated succesfully";
                    } else if ((episode_status == "Deactivated")) {
                        success_msg = "Episode deactivated succesfully";
                    } else if (episode_status == "In Progress") {
                        success_msg = "Episode paused succesfully";
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

    function deleteEpisode(episode_id) {

        console.log(episode_id);
        var formdata = new FormData();
        formdata.append("episode_id", episode_id);
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to Delete Episode? This process is irreversible, and will remove ALL related data (audio recordings, video, etc)",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/api/v1/episode/delete",
                    method: "POST",
                    data: formdata,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        data = JSON.parse(data);
                        console.log(typeof (data))
                        console.log(data)
                        if (data) {
                            console.log(data)
                            swal("Episode deleted", {
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
                swal("Episode's data is safe");
            }
        });
    }


    function  validateEpisodeInput(episode_name,episodeTitle,episodeDescription,episode_thumbnail,addepisodeAudio,addepisodeVideo,episode_position,episodetags){
        if (episode_name.trim() == ""){
            toastr.error("Episode name cannot be blank");
            return false
        }else if(episode_position ==""){
            toastr.error("Position cannot be blank be blank");
            return false
        }else if(Number.isInteger(Number(episode_position)) == false){
            toastr.error("Please enter a valid position");
            return false
        }
        else if(episodeTitle == ""){
            toastr.error("Title cannot be blank");
            return false
        }else if(episodetags == ""){
            toastr.error("Please enter episode tags");
            return false
        }
        // else if(episode_thumbnail == ""){
        //     toastr.error("Please select episode thumbnail");
        //     return false
        // }
        // else if(addepisodeVideo == ""){
        //     toastr.error("Please select episode video");
        //     return false
        // }
//        else if(addepisodeAudio == ""){
//            toastr.error("Please select episode audio");
//            return false
//        }
        else if(episodeDescription == ""){
            toastr.error("Please enter episode description");
            return false
        }
        else{
            return true
        }
    }


    function resetViewFilter() {
        $("#ranged-value").freshslider({
            range: true,
            step: 1,
             value: [0, 200],
             max : 500,
            onchange: function (low, high) {
                episode_view_lower_range = low;
                episode_view_higher_range = high;

            }

        });
    }
});

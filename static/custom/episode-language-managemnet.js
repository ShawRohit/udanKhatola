var episodeAudio="";
var episodeThumbnail1="";
var episodeVideo="";


$(document).ready(function () {

    $(document).on('change', '.episode-language-status', function(e) {
        e.stopPropagation();
        let episode_language_status = $(this).val()
        let language_id = $(this).attr("data-id");
        changeEpisodeLanguageStatus(episode_language_status,language_id);
    });

//    $(document).on('click','#add-language-for-episode-modal',function(){
//        console.log("Clicked once")
//        resetDataForAddEpisodeModal();
//    });


     $(document.body).on("change", '#episode_language_thumbnail', function (e) {
        episodeThumbnail1 = this.files[0];
        $("#episode_language_thumbnail_name").val(episodeThumbnail1['name'])
    });

     $(document.body).on("change", '#episode_language_video', function (e) {
        episodeVideo = this.files[0];
        $("#episode_language_video_name").val(episodeVideo['name'])
    });

     $(document.body).on("change", '#episode_language_audio', function (e) {
        episodeAudio = this.files[0];
        $("#episode_language_audio_name").val(episodeAudio['name'])
    });


     $(document).on('click', '.edit-language-support-for-episode', function (e) {
        var episode_id = $(this).attr("data-id");
        getLanguageSupportForEpisode(episode_id,"task")
    });


    $(document).on('click', '.btn-close', function (e) {
        resetDataInAddEditEpisodeLanguageModal();
    });

     $(document).on('click', '.btn-dismiss-modal', function (e) {
        resetDataInAddEditEpisodeLanguageModal();
    });


    $(document).on('click', '#add-language-for-episode-modal', function (e) {
        resetDataInAddEditEpisodeLanguageModal();
        console.log("Clicked twice")
    });

     $(document).on('click', '.view-language-support-for-episode', function (e) {
        var language_id = $(this).attr("data-id");
        getLanguageSupportForEpisode(language_id, "view")
    });

    $(document).on('click', '.delete-language-support-for-episode', function (e) {
        var episode_id = $(this).attr("data-id");
        deleteLanguageSupportForEpisode(episode_id)
    });

     $(document).on("click","#add-language-support-for-episode",function(){
        let buttonId = '#add-language-support-for-episode';
        var language = $("#episode-add-language").val();
        var title = $("#episode-language-title").val();
        var episode_tags = $("#tags1").val();
        var episode_language_description = $("#episode_language_description").val();
        var data_episode_id = $(this).attr("data-episode-id");
        var episode_id = $(this).attr("data-id");
        var formData = new FormData();
        formData.append("language",language);
        formData.append("title",title);
        formData.append("episode_tags",episode_tags);
        formData.append("episode_language_description",episode_language_description);
        formData.append("data_episode_id",data_episode_id);
        formData.append("episode_id",episode_id);
        formData.append("episodeAudio",episodeAudio);
        formData.append("episodeVideo",episodeVideo);
        formData.append("episode_thumbnail",episodeThumbnail1);

        if (language.trim() ==""){
            toastr.error("Language cannot be empty");
            return false

        }else if (title.trim() == ""){
            toastr.error("Title cannot be empty");
            return false
        }

        if (episode_tags == ""){
            toastr.error("PLease enter episode tags");
            return false
        }
        else if (episode_language_description.trim() == ""){
            toastr.error("Please enter episode description");
            return false
        }
        else{

         $.ajax({
            url: '/api/v1/episode/add-edit-language-support',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            beforeSend: function (xhr, settings) {
                $(buttonId).prop('disabled', true);
                $(buttonId).prop('innerText', 'Creating...');
                $(".custom_loader").show();
//                $(".btn-close").click();
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data.status) {
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Created');
                    if (data_episode_id !=""){
                        setInterval(function(){
                            window.location.reload();
                        },2000);
                        toastr.success("Episode edited successfully");
                    }else{
                        setInterval(function(){
                            window.location.reload();
                        },2000);
                        toastr.success(data.message);

                    }
                    $(".custom_loader").hide();
                    $(".btn-close").click();

                }
                else{
                    $(buttonId).prop('disabled', false);
                    $(buttonId).prop('innerText', 'Create');
                    $(".custom_loader").hide();
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                $(".custom_loader").hide();
                $(buttonId).prop('disabled', false);
                $(buttonId).prop('innerText', 'Create');
                const data=JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });

        }

    })

    function deleteLanguageSupportForEpisode(episode_id){
        var formData = new FormData();
        formData.append("episode_id",episode_id)
         swal({
            title: "Are you sure?",
            text: "Are you sure you want to Delete language support? This process is irreversible, and will remove ALL related data (audio recordings, video, etc)",
            icon: "warning",
            buttons: true,
            dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                    $.ajax({
                            url: "/api/v1/episode/delete-language-support",
                            method: "POST",
                            data: formData,
                            cache: false,
                            processData: false,
                            contentType: false,
                            success: function (data) {
                                data = JSON.parse(data);
                                if(data == true){
                                     swal("Episode deleted", {
                                            icon: "success",
                                     });
                                     setTimeout(function(){
                                      window.location.reload();
                                     },1000);

                                 }else{
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

    function getLanguageSupportForEpisode(episode_id, task){
        console.log(episode_id)
        console.log(task)
        var formData = new FormData()
        formData.append("episode_id",episode_id);
         $.ajax({
        async: true,
        type: "POST",
        url: "/api/v1/episode/episode-language-details",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        beforeSend: function() {},
        success: function (data) {
            data = JSON.parse(data);
            if(data.status){
                setDataInEditEpisodeLanguageModal(data,task)
            }else{
                toastr.error(data.message)
                return false;
            }
        },
        error: function(request, status, error) {
            toastr.error("Internal Server Error")
            return false;
        }
  });
    }





    function setDataInEditEpisodeLanguageModal(data, task){
        if (task == "view"){
            $("#episode-modal-heading").text("View language support for episode")
            $("#view-save-button").hide();
            $("#episode-language-title").attr("readonly",true);
            $("#episode_language_thumbnail").attr("disabled",true);
            $("#episode_language_video").attr("disabled",true);
            $("#episode_language_audio").attr("disabled",true);
            $('.inputTags-field').attr("readonly", true)
            $("#episode_language_description").attr("readonly",true);
            $("#episode-add-language").attr("disabled",true)
        }else{
            $("#episode-modal-heading").text("Edit language support for episode")
            $("#add-language-support-for-episode").text("Edit")
            $("#view-save-button").show();
            $("#episode-language-title").attr("readonly",false);
            $("#episode_language_thumbnail").attr("disabled",false);
            $("#episode_language_video").attr("disabled",false);
            $("#episode_language_audio").attr("disabled",false);
            $('.inputTags-field').attr("readonly", false)
            $("#episode_language_description").attr("readonly",false);
            $("#episode-add-language").attr("disabled",false)
        }
        var audio_link = ""
        if (data.episode_audio != null){
           audio_link=  data.episode_audio.split("/")
        }
        var image_link =""
         if (data.episode_thumbnail != null){
           image_link = data.episode_thumbnail.split("/")
        }
        var video_link =""
         if (data.episode_video != null){
           video_link = data.episode_video.split("/")
        }

        $(".close-add-edit-modal")
        $("#add-language-support-for-episode").attr("data-episode-id",parseInt(data["id"]))
        $("#episode-language-title").val(data.episode_title);
        if (data.episode_audio != null){
            $("#episode_language_audio_name").val(audio_link[audio_link.length -1].slice(11));
        }else{
            $("#episode_language_audio_name").val("");
        }

        if (data.episode_thumbnail != null){
           $("#episode_language_thumbnail_name").val(image_link[image_link.length -1].slice(11));
        }else{
           $("#episode_language_thumbnail_name").val("");
        }

        if (data.episode_video != null){
           $("#episode_language_video_name").val(video_link[video_link.length -1].slice(11));
        }else{
            $("#episode_language_video_name").val("");
        }


        var tags_array = data.episode_tags.split(",")
        tags_array.forEach(function(item) {
            $('#tags1').inputTags('tags', item, function (tags) {
            $('.results').empty().html('<strong>Tags:</strong> ' + tags.join(' - '));
        });
       })

        $("#episode_language_description").val(data.episode_description);

        $("#episode-add-language > option").each(function() {
        if ($(this).val().toString() == data.language_id) {
            $('#episode-add-language').prop("selectedIndex", $(this).prop("index"));
            }
        })
    }

    function changeEpisodeLanguageStatus(language_status,language_id){
        let formdata = new FormData();
        formdata.append("language_status", language_status);
        formdata.append("language_id", language_id);
        $.ajax({
            url: '/api/v1/episode/update-episode-language-status',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {

                if (data) {
                    let success_msg = '';
                    if (language_status == "Active"){
                        success_msg = "Language activated succesfully";
                    }else if ((language_status == "Deactivated")){
                        success_msg = "Language deactivated succesfully";
                    }else if (language_status == "In Progress"){
                        success_msg = "Language in Progress succesfully";
                    }
                    toastr.success(success_msg);
//                    setInterval(function(){
//                        window.location.reload();
//                        console.log("-----------")
//                    },1000);
                }
                else{
                     data = JSON.parse(data);
                    toastr.error(data.message);
                }
            },
            error: function (err) {
                 data = JSON.parse(data);
                const data=JSON.parse(err.responseText)
                toastr.error(data.message);
            }
        });

    }



    function resetDataForAddEpisodeModal(){
        $("#episode-modal-heading").text("Add language support for episode")
        $("#view-save-button").show();
        $("#episode-language-title").attr("readonly",false);
        $("#episode_language_thumbnail").attr("disabled",false);
        $("#episode_language_video").attr("disabled",false);
        $("#episode_language_audio").attr("disabled",false);
        $('.inputTags-field').attr("readonly", false)
        $("#episode_language_description").attr("readonly",false);
        $("#episode-add-language").attr("disabled",false)
    }


});

 function resetDataInAddEditEpisodeLanguageModal(){
        $("#view-save-button").show();
        $("#episode_language_description").val('');
        $("#episode-modal-heading").text("Add language support for episode")
        $("#add-language-support-for-episode").attr("data-episode-id","")
        $("#episode-language-title").val("");
        $("#episode_language_audio_name").val("");
        $("#episode_language_video_name").val("");
        $("#episode_language_thumbnail_name").val("");
         $("#add-language-support-for-episode").attr("disabled",false);
        $(".close-item").click();
        $("#add-language-support-for-episode").text("Save")
        $("#episode-add-language > option").each(function() {
        if ($(this).val().toString() == "English") {
            $('#episode-add-language').prop("selectedIndex", $(this).prop("index"));
        }
        })
        $("#episode-language-title").attr("readonly",false);
        $("#episode_language_thumbnail").attr("disabled",false);
        $("#episode_language_video").attr("disabled",false);
        $("#episode_language_audio").attr("disabled",false);
        $('.inputTags-field').attr("readonly", false)
        $("#episode_language_description").attr("readonly",false);
        $("#episode-add-language").attr("disabled",false)
    }

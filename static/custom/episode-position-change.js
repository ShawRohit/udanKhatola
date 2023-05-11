let initial_data = new Array();
$('.row_position>tr').each(function () {
    initial_data.push({"position": $(this).attr("data-position-id"), "episode_id": $(this).attr("data-id")});
});
console.log(initial_data);
$(".row_position").sortable({
    delay: 150,
    stop: function () {
        var selectedData = new Array();

        $('.row_position>tr').each(function () {
            selectedData.push({"position": $(this).attr("data-position-id"), "episode_id": $(this).attr("data-id")});
        });
        let formData = new FormData();
        console.log(selectedData)
        console.log(initial_data)
        formData.append("updated_rows", JSON.stringify(selectedData));
        formData.append("initial_rows", JSON.stringify(initial_data));
        swal({
            title: "Are you sure you want to update position?",
            text: "",
            icon: "warning",
            buttons: true,
            dangerMode: false,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/api/v1/episode/update-episode-positions",
                    method: "POST",
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        data = JSON.parse(data);
                        console.log(typeof (data))
                        console.log(data.status)
                        if (data.status) {
                            console.log(data)
                            swal("Episode positions updated", {
                                icon: "success",
                            });
                            setTimeout(function () {
                                window.location.reload();
                            }, 2000);

                        } else {
                            swal("Cannot Update", {
                                icon: "error",
                            });
                            table = $('#example').DataTable();
                            table.draw();

                        }
                    }
                });
            } else {
                table = $('#example').DataTable();
                table.draw();
                swal("Episode's position is unchanged");
            }
        });
    }
});

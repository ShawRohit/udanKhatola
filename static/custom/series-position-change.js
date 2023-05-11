let change_data = new Array();
$('.series_row_position>tr').each(function () {
    change_data.push({"position": $(this).attr("data-position-id"), "series_id": $(this).attr("data-id")});
});
console.log(change_data);
$(".series_row_position").sortable({
    delay: 150,
    stop: function () {
        var selectedData = new Array();

        $('.series_row_position>tr').each(function () {
            selectedData.push({"position": $(this).attr("data-position-id"), "series_id": $(this).attr("data-id")});
        });
        let formData = new FormData();
        console.log(selectedData)
        console.log(change_data)
        formData.append("updated_rows", JSON.stringify(selectedData));
        formData.append("initial_rows", JSON.stringify(change_data));
        swal({
            title: "Are you sure you want to update position?",
            text: "",
            icon: "warning",
            buttons: true,
            dangerMode: false,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: "/api/v1/series/update-series-positions",
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
                            swal("Series positions updated", {
                                icon: "success",
                            });
                            setTimeout(function () {
                                window.location.reload();
                                console.log(data)
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
                swal("Series's position is unchanged");
            }
        });
    }
});

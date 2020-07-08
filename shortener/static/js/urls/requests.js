window.onload = function () {
    $("#approval-submit").click(function (e) {
        let approved = [];
        let denied = [];
        $(".url-approve").each(function () {
            if($(this).prop('checked'))
                approved.push($(this).prop('id'));
        })
        $(".url-deny").each(function () {
            if($(this).prop('checked'))
                denied.push($(this).prop('id'));
        })
        $("#id_approved").val(approved);
        $("#id_denied").val(denied);

    })
}
$("#commentForm").submit(function (e) {
  e.preventDefault();
  $.ajax({
    data: $(this).serialize(),
    method: $(this).attr("method"),
    url: $(this).attr("action"),
    dataType: "json",
    success: function (res) {
      console.log("Comment Save");

      if (res.bool == true) {
        $("#review-rsp").html("Review added successfully!");
      }
    },
  });
});

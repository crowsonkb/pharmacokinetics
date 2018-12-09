"use strict";

$(document).ready(() => {
    $("#main-form").submit(e => {
        e.preventDefault();
        let query = "concentration.svg?" + $("#main-form").serialize();
        let img = $("<img>", {src: query});
        $("#chart-container").html(img);
    });
});

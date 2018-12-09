"use strict";

$(document).ready(() => {
    $("#main-form").submit(e => {
        e.preventDefault();
        let dummy = new Date().getTime();
        let query = "concentration.svg?" + $("#main-form").serialize() + "&dummy=" + dummy;
        let img = $("<img>", {id: "chart", src: query});
        $("#chart-container").html(img);
    });
});

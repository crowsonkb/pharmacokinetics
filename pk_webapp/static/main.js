"use strict";

$(document).ready(() => {
    $("#main-form").submit(e => {
        e.preventDefault();
        let dummy = new Date().getTime();
        let query = `?${$("#main-form").serialize()}&dummy=${dummy}`;
        let img = $("<img>", {id: "chart", src: "concentration.svg" + query});
        let csvLink = $("<a>", {
            class: "csv-download",
            href: "concentration.csv" + query,
            text: "Download data as CSV"
        });
        $("#chart-container").html([csvLink, "<br>", img]);
    });
});

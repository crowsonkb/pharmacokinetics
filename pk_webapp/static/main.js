"use strict";

function setWithDataURL(url, elem) {
    let isFirefox = navigator.userAgent.search("Firefox") > -1;
    let img = $("<img>");
    img.attr("class", "replace");
    img[0].onload = () => {
        let h = img[0].naturalHeight;
        let w = img[0].naturalWidth;
        let scale = parseInt($(elem).css("width")) / Math.max(h, w);
        img.attr("height", Math.min(h, h * scale));
        img.attr("width", Math.min(w, w * scale));
        if (!isFirefox) $(`#${elem.id} .replace`).replaceWith(img);
    };
    img.attr("src", url);
    if (isFirefox) $(`#${elem.id} .replace`).replaceWith(img);
}

$(document).ready(() => {
    $("#main-form").submit(e => {
        e.preventDefault();
        $.post("concentration_svg", $("#main-form").serialize()).done(data => {
            setWithDataURL(data, $("#chart")[0]);
        });
    });
});

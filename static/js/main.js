window.onload = function () {
    var markdown = new Reader("mark");
    markdown.showHtml("preview");
    markdown.showHtml("wait-post");
    document.getElementById("mark").addEventListener("keyup", function () {
        var markdown = new Reader("mark");
        markdown.showHtml("preview");
        markdown.showHtml("wait-post");
    });
};

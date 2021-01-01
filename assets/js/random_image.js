// https://stackoverflow.com/a/2777577

var imageURLs = [
    "https://www.dropbox.com/s/rqq6kyw5hijdo86/nzw1.png?raw=1",
    "https://www.dropbox.com/s/zx3ad4pewvqg6mq/nzw2.png?raw=1"
];
function getImageTag() {
    var img = '<img class="img-fluid z-depth-1 rounded" src=\"';
    var randomIndex = Math.floor(Math.random() * imageURLs.length);
    img += imageURLs[randomIndex];
    img += '\" alt=\"KN pic\"/>';

    return img;
}

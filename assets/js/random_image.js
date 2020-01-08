// https://stackoverflow.com/a/2777577

var imageURLs = [
    "https://www.dropbox.com/s/feoh20rk00zuevm/nzw0.jpg?raw=1",
    "https://www.dropbox.com/s/rqq6kyw5hijdo86/nzw1.png?raw=1",
    "https://www.dropbox.com/s/zx3ad4pewvqg6mq/nzw2.png?raw=1"
];
function getImageTag() {
    var img = '<img src=\"';
    var randomIndex = Math.floor(Math.random() * imageURLs.length);
    img += imageURLs[randomIndex];
    img += '\" alt=\"nzw picture\"';
    img += 'height=\"500\" width=\"500\" />';


    return img;
}

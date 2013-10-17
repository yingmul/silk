// set up variables
var reader = new FileReader(),
    i=0,
    numFiles = 0,
    imageFiles;

// use the FileReader to read image i
function readFile() {
    reader.readAsDataURL(imageFiles[i])
}

// define function to be run when the File
// reader has finished reading the file
reader.onloadend = function(e) {

    // make an image and append it to the div
    var image = $('<img>').attr('src', e.target.result);
    $(image).appendTo('#images');

    // if there are more files run the file reader again
    if (i < numFiles) {
        i++;
        readFile();
    }
};


$('#id_file').change(function() {
    imageFiles = document.getElementById('id_file').files
    // get the number of files
    numFiles = imageFiles.length;
    readFile();

});
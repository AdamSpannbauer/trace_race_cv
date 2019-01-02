var stream, imageCapture;

function getMediaStream() {
    window.navigator.mediaDevices.getUserMedia({video: true})
    .then(function(mediaStream) {
        stream = mediaStream;
        let mediaStreamTrack = mediaStream.getVideoTracks()[0];
        imageCapture = new ImageCapture(mediaStreamTrack);
        console.log(imageCapture);
    })
    .catch(error);
}

function error(error) {
    console.error('error:', error);
}

function takePhoto(img) {
    const canvas = document.createElement('canvas');

    imageCapture.grabFrame()
      .then(imageBitmap => {
        canvas.width = imageBitmap.width;
        canvas.height = imageBitmap.height;
        canvas.getContext('2d').drawImage(imageBitmap, 0, 0);

        var dataURL = canvas.toDataURL('image/jpeg', 1.0);
          $.ajax({
             type: "POST",
             url: "get_frame",
             data: { img: dataURL }
          }).done(function(msg){
             // alert(msg);
          });
      })
      .catch();
};

/* just call */
getMediaStream();

/* and when you want to capture an image */
setInterval(function() { takePhoto() }, 0);

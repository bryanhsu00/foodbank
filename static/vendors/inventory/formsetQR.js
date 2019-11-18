var video = document.createElement("video");
var canvasElement = document.getElementById("canvas");
var canvas = canvasElement.getContext("2d");
var tmpQRdata = "";

function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
}

// Use facingMode: environment to attemt to get the front camera on phones
function turnOn(){
    document.getElementById('form-area').hidden = true;
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(function(stream) {
            video.srcObject = stream;
            video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
            video.play();
            requestAnimationFrame(tick);
        });
}

function turnOff(){
    video.srcObject.getTracks().forEach(function(track) {
        track.stop();
    });;
    canvasElement.hidden = true;
    document.getElementById('parent').removeChild(canvasElement);
    document.getElementById('form-area').hidden = false;
}

function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvasElement.hidden = false;
        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        var code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });
        if (code) {
            drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
            drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
            drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
            drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
            if (code.data !== tmpQRdata){
                let formNum = document.getElementById('id_form-TOTAL_FORMS').value;
                let lastForm = document.getElementById(`id_form-${formNum-1}-item`);
                if(tmpQRdata !== code.data){
                    if (lastForm.value == ""){
                        lastForm.value = code.data;
                    } else {
                        cloneMore('.form-row:last', 'form');
                        document.getElementById(`id_form-${formNum}-item`).value = code.data;
                    }
                    tmpQRdata = code.data;
                }
            }
        }
    }
    requestAnimationFrame(tick);
}




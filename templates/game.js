const video = document.getElementById("myvideo");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
let trackButton = document.getElementById("trackbutton");
let updateNote = document.getElementById("updatenote");
let points = [];
start = false;

let isVideo = false;
let model = null;

const modelParams = {
  flipHorizontal: true, // flip e.g for video
  maxNumBoxes: 1, // maximum number of boxes to detect
  iouThreshold: 0.85, // ioU threshold for non-max suppression
  scoreThreshold: 0.87, // confidence threshold for predictions.
};

function startVideo() {
  handTrack.startVideo(video).then(function (status) {
    console.log("video started", status);
    if (status) {
      updateNote.innerText = "Video started. Now tracking";
      isVideo = true;
      runDetection();
    } else {
      updateNote.innerText = "Please enable video";
    }
  });
}

function toggleVideo() {
  if (!isVideo) {
    updateNote.innerText = "Starting video";
    startVideo();
  } else {
    updateNote.innerText = "Stopping video";
    handTrack.stopVideo(video);
    isVideo = false;
    updateNote.innerText = "Video stopped";
  }
}

function runDetection() {
  model.detect(video).then((predictions) => {
    console.log("Predictions: ", predictions);
    if (predictions.length > 0) {
      let xpos = predictions[0].bbox[0] + predictions[0].bbox[2] / 2;
      let ypos = predictions[0].bbox[1] + predictions[0].bbox[3] / 2;
      points.push([xpos, ypos]);
      console.log("pushed");
    }
    // model.renderPredictions(predictions, canvas, context, video);
    runDrawPredictions(predictions);
    if (isVideo) {
      requestAnimationFrame(runDetection);
    }
  });
}

function runDrawPredictions(predictions) {
  // context.clearRect(0, 0, canvas.width, canvas.height);

  context.save();
  context.scale(-1, 1);
  context.translate(-video.width, 0);
  // context.drawImage(mediasource, 0, 0, mediasource.width, mediasource.height);
  context.restore();
  // context.font = '10px Arial';
  // console.log('number of detections: ', predictions.length);
  console.log("above loop");
  console.log(points);
  let nxpos, nypos, xpos, ypos
  if (points.length > 0) {
    nxpos = points[points.length - 1][0];
    nypos = points[points.length - 1][1];
    xpos = nxpos;
    ypos = nypos;
  }
  if (points.length > 1) {
    xpos = points[points.length - 2][0];
    ypos = points[points.length - 2][1];
  }
  if (points.length >= 2) {
    drawDoodle(nxpos, nypos, xpos, ypos);
  }
}

function drawDoodle(nxpos, nypos, xpos, ypos) {
  context.beginPath(); // begin
  context.lineWidth = 5;
  context.lineCap = "round";
  context.strokeStyle = "#1780DC";
  context.moveTo(xpos, ypos); // from
  context.lineTo(nxpos, nypos); // to
  context.stroke(); // draw it!
  console.log("Drawn in drawDoodle");
  context.closePath();
  console.log("closed path");
}

// Load the model.
handTrack.load(modelParams).then((lmodel) => {
  // detect objects in the image.
  model = lmodel;
  updateNote.innerText = "Loaded Model!";
  trackButton.disabled = false;
});

// function draw(x, y) {
//     background(51);
//     stroke(0);
//     strokeWeight(25);
//     noFill();
//     if (start) {
//       points.push(createVector(mouseX, mouseY));
//     }

//     beginShape();
//     for (let i = 0; i < points.length; i++) {
//     let x = points[i].x;
//     let y = points[i].y;
//     console.log(x)
//     vertex(x,y);
//     }
//     endShape();
// }

// function mousePressed() {
//     start = true;
//     points = [];
//   }

//   function mouseReleased() {
//     start = false;
//   }

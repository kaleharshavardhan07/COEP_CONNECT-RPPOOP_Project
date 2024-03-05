document.addEventListener('DOMContentLoaded', function () {
    const startGestureButton = document.getElementById('startGestureButton');
    const videoElement = document.getElementById('videoElement');
    let previousY = 0;
    const gestureThreshold = 0.01; // Threshold for detecting swipe gesture, adjust based on sensitivity required

    startGestureButton.addEventListener('click', startGestureControl);

    function startGestureControl() {
        startCamera();
        startGestureButton.disabled = true; // Disable the button after starting gesture control
    }

    function onResults(results) {
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            let landmarks = results.multiHandLandmarks[0]; // Assuming single hand, get landmarks for the first hand
            let indexFingerTip = landmarks[8]; // Index fingertip is landmark #8
            let deltaY = indexFingerTip.y - previousY;
            previousY = indexFingerTip.y;

            // Detect swipe up
            if (deltaY < -gestureThreshold) {
                window.scrollBy(0, -100); // Adjust scrolling amount as needed
            }
            // Detect swipe down
            else if (deltaY > gestureThreshold) {
                window.scrollBy(0, 100); // Adjust scrolling amount as needed
            }
        }
    }

    function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
                videoElement.play();
                const hands = new Hands({ locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
                hands.setOptions({
                    maxNumHands: 1,
                    modelComplexity: 1,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5
                });
                hands.onResults(onResults);
                const camera = new Camera(videoElement, {
                    onFrame: async () => {
                        await hands.send({ image: videoElement });
                    },
                    width: 1280,
                    height: 720
                });
                camera.start();
            })
            .catch(function (err) {
                console.error('Error accessing the camera:', err);
            });
    }
});

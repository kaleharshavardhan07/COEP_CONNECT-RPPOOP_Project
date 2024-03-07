document.addEventListener('DOMContentLoaded', function () {
    const startGestureButton = document.getElementById('startGestureButton');
    const videoElement = document.getElementById('videoElement');
    let previousThumbsUp = false;
    const gestureThreshold = 0.5; // Threshold for detecting thumbs up/down, adjust based on sensitivity required

    startGestureButton.addEventListener('click', startGestureControl);

    function startGestureControl() {
        startCamera();
        startGestureButton.disabled = true; // Disable the button after starting gesture control
    }

    function onResults(results) {
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            let landmarks = results.multiHandLandmarks[0]; // Assuming single hand, get landmarks for the first hand
            let thumbTip = landmarks[4]; // Thumb tip is landmark #4
            let thumbUp = thumbTip.y < landmarks[5].y; // Check if thumb is above index finger

            // Detect thumbs up
            if (thumbUp && !previousThumbsUp) {
                window.scrollBy(0, -100); // Scroll up
            }
            // Detect thumbs down
            else if (!thumbUp && previousThumbsUp) {
                window.scrollBy(0, 100); // Scroll down
            }
            previousThumbsUp = thumbUp;
        }
    }

    function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
                videoElement.addEventListener('loadedmetadata', function () {
                    videoElement.play();
                });

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

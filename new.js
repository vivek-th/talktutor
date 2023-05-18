// Global variables
let recognition;
let output = document.getElementById('output');

// Create SpeechRecognition object
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;

    // Adjust sensitivity for Indian English accent
    recognition.interimResults = true;
    recognition.maxAlternatives = 5;
    recognition.lang = 'en-IN';

    // Event handler for when a result is received
    recognition.onresult = function(event) {
        let transcript = event.results[event.results.length - 1][0].transcript;
        output.innerHTML = 'You said: ' + transcript;

        // Send transcript to Python backend
        fetch('http://localhost:5500/process', {  // Modify the URL to match your Python backend's URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript: transcript })
        })
        .then(response => response.json())
        .then(data => {
            output.innerHTML = 'You said: ' + transcript + '<br>Correction: ' + data.corrected_transcript;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
} else {
    output.innerHTML = 'Speech recognition not supported.';
}

// Start recording when the "Start Recording" button is clicked
function startRecording() {
    output.innerHTML = 'Listening...';
    img=
    recognition.start();
}

// Stop recording when the "Stop Recording" button is clicked
function stopRecording() {
    output.innerHTML = 'Stopped listening.';
    recognition.stop();
}

// Automatically stop recording after 10 seconds
function autoStopRecording() {
    setTimeout(function() {
        stopRecording();
    }, 10000);
}

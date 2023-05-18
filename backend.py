from flask import Flask, request, jsonify
from flask_cors import CORS
from gingerit.gingerit import GingerIt

app = Flask(__name__)
CORS(app)

ginger_parser = GingerIt()

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    transcript = data.get('transcript', '')

    # Parse and correct transcript using Ginger API
    result = ginger_parser.parse(transcript)
    corrected_transcript = result['result']
    errors = result['corrections']

    # Prepare response
    response = {
        'corrected_transcript': corrected_transcript,
        'errors': errors
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5500)

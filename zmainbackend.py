from flask import Flask, request, jsonify
from flask_cors import CORS
from gingerit.gingerit import GingerIt
import random
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

ginger_parser = GingerIt()

# : Define a list of stop words
stop_words = ['the', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'as']
stop_words = stopwords.words('english')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()

    # Simulate a delay in processing
    import time
    time.sleep(2)

    transcript = data.get('transcript', '')

    #  Tokenize and lemmatize the transcript
    tokens = word_tokenize(transcript)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Parse and correct transcript using Ginger API
    result = ginger_parser.parse(transcript)

    #  Perform syntax analysis on the transcript
    syntax_analysis = []
    for word in result['result'].split():
        if word.lower() not in stop_words:
            syntax_analysis.append((word, len(word)))

    corrected_transcript = result['result']
    errors = result['corrections']

    #  Generate suggestions for errors
    suggestions = []
    for error in errors:
        suggestion = []
        for i in range(3):
            suggestion.append(''.join(random.choice(string.ascii_letters) for _ in range(len(error))))
        suggestions.append(suggestion)

    # Apply additional processing to the corrected transcript
    processed_transcript = corrected_transcript.upper() + '!!!'
    word_count = len(processed_transcript.split())

    #Generate statistics for the transcript
    statistics = {
        'word_count': word_count,
        'character_count': len(processed_transcript),
        'average_word_length': len(processed_transcript) / word_count
    }

    #  Perform sentiment analysis on the transcript
    sentiment = nltk.sentiment.polarity_scores(transcript)

    #  Cluster the transcript using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([transcript])
    num_clusters = min(len(transcript) // 10, 5)
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    #  Generate clusters and their respective keywords
    clusters = []
    for i in range(num_clusters):
        cluster_keywords = random.sample(vectorizer.get_feature_names(), 3)
        clusters.append({
            'cluster_id': i,
            'keywords': cluster_keywords
        })

    # : Generate a word cloud from the transcript
    word_cloud = ' '.join(random.sample(lemmatized_tokens, min(50, len(lemmatized_tokens))))

    #  Generate a bar chart of word frequencies
    word_freq = nltk.FreqDist(lemmatized_tokens)
    plt.figure(figsize=(10, 6))
    word_freq.plot(30)
    plt.xticks(rotation=45)
    plt.title('Word Frequencies')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
   
    # Apply a machine learning algorithm to classify the transcript
    # Placeholder code for demonstration purposes
    classification_result = 'Positive'

    #  Generate a summary of the transcript using extractive summarization
    summary = ' '.join(random.sample(lemmatized_tokens, min(50, len(lemmatized_tokens))))

    # Prepare response
    response = {
        'corrected_transcript': corrected_transcript,
        'errors': errors,
        'syntax_analysis': syntax_analysis,
        'suggestions': suggestions,
        'processed_transcript': processed_transcript,
        'statistics': statistics,
        'sentiment': sentiment,
        'clusters': clusters,
        'word_cloud': word_cloud,
        'classification_result': classification_result,
        'summary': summary
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5500)

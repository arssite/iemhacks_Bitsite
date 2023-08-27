from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/')
def index():
    return render_template('green.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = generate_response(user_input)
    return jsonify({'response': response})

def generate_response(user_input):
    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)

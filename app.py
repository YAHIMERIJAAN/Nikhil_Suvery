from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('Survey.html')   # make sure filename matches exactly

# Submit route
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        # Get answers array from frontend
        answers = data.get("answers")

        if not answers:
            return jsonify({
                "status": "error",
                "message": "No answers received"
            }), 400

        print("Received answers:", answers)

        file_name = "responses.csv"
        file_exists = os.path.isfile(file_name)

        # Save to CSV
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header only once
            if not file_exists:
                header = [f"Q{i+1}" for i in range(len(answers))]
                writer.writerow(header)

            writer.writerow(answers)

        return jsonify({
            "status": "success",
            "message": "Data saved successfully"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Run app
if __name__ == '__main__':
    app.run(debug=True)
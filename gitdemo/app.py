from flask import Flask, render_template, request
import pickle

# Load pipeline and model
with open("pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    user_input = ""

    if request.method == "POST":
        user_input = request.form["tweet"]

        # Transform input text
        X_input = pipeline.transform([user_input])

        # Predict
        pred = model.predict(X_input)[0]

        # Convert to label
        prediction = "Real" if pred == 1 else "Fake"

    return render_template("index.html", prediction=prediction, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)

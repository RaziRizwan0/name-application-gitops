from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
names = []

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>raziii Name Storing App</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; max-width: 700px; }
    input, button { padding: 10px; font-size: 16px; }
    ul { margin-top: 20px; }
    li { padding: 4px 0; }
  </style>
</head>
<body>
  <h1>Name Storing App</h1>
  <p>Enter a name and save it.</p>

  <input id="nameInput" placeholder="Enter name" />
  <button onclick="saveName()">Save</button>

  <h2>Stored Names</h2>
  <ul id="nameList"></ul>

  <script>
    async function loadNames() {
      const res = await fetch('/names');
      const data = await res.json();
      const list = document.getElementById('nameList');
      list.innerHTML = '';
      data.names.forEach(n => {
        const li = document.createElement('li');
        li.textContent = n;
        list.appendChild(li);
      });
    }

    async function saveName() {
      const input = document.getElementById('nameInput');
      const name = input.value.trim();
      if (!name) return;

      await fetch('/names', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      });

      input.value = '';
      loadNames();
    }

    loadNames();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/names", methods=["GET"])
def get_names():
    return jsonify({"names": names})

@app.route("/names", methods=["POST"])
def add_name():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    names.append(name)
    return jsonify({"message": "saved", "names": names}), 201

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

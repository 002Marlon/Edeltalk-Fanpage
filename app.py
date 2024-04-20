from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def Create_embed(video_id, start_time):
    embed_code = f'<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/{video_id}?start={int(start_time)}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    return embed_code

@app.route("/", methods=["GET", "POST"])
def search():
  search_word = ""
  word_count = 0
  results = []
  if request.method == "POST":
    search_word = request.form["search_term"]
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "transcripts")
    word_count, results = search_json_files(search_word, directory)
  return render_template("search.html", search_term=search_word, word_count=word_count, results=results)

def search_json_files(word, directory):
  word_counter = 0
  results = []
  for filename in os.listdir(directory):
    if filename.endswith(".json"):
      filepath = os.path.join(directory, filename)
      with open(filepath, "r") as file:
        data = json.load(file)

        for item in data:
          if word in item["text"]:
            word_counter += 1
            start_time = item["start"]
            video_id = filename[:-5]
            embed_code = Create_embed(video_id, start_time)
            results.append({"filename": filename, "start_time": start_time, "embed_code": embed_code, "video_url": f"https://www.youtube.com/watch?v={video_id}&t={int(start_time)}s"})
  return word_counter, results

if __name__ == "__main__":
  app.run(debug=True)
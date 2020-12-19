from flask import Flask, render_template, request, g, jsonify
from texts import *

app = Flask(__name__)

# TODO: Style matches container. Progress bar in matches dropdown. 

@app.route('/')
def index():
    return render_template('index.html')

#  ----   TEXT_SIMI API (text-matches html generator)   ----  #   
@app.route('/local_corpus_match/<file_name>', methods=['GET', 'POST'])
def local_corpus_match(file_name):
    if request.method == 'POST':
        text = str(request.get_data())
        return jsonify(getMatchesText(text, Samples_Corpus)), 201

    return render_template('text_simi_matches.html', file_matches = getMatchesText(get_text_from_file_name(file_name), Samples_Corpus)), 201

#  ----   TEXT_SIMI MAIN VIEW   ----  #   
Checks  = Check_texts()
Checks_Names = get_filenames_from_paths(Checks)

Checks_Texts = []
for file_name in Checks_Names:
    Checks_Texts.append(get_text_from_file_name(file_name))

@app.route('/text_simi')
def text_simi():
    return render_template('text_simi.html', check_names = Checks_Names, file_texts = Checks_Texts,
                            file_matches = getMatchesText(get_text_from_file_name(Checks_Names[0]), Samples_Corpus))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
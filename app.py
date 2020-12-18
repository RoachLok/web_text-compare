from flask import Flask, render_template, request, g
from texts import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

Checks  = Check_texts()
Checks_Names = get_filenames_from_paths(Checks )

@app.route('/text_simi', methods=['GET', 'POST'])
def text_simi():
    if request.method == 'POST':
        choice       = request.form['file_selector']

        file_text    = get_text_from_file_name(choice)
        file_matches = getMatchesText(file_text, Samples_Corpus) 

        return render_template('text_simi.html', sample_names = Samples_Corpus, check_names = Checks_Names,
                                file_text = file_text, selected_file = choice, file_matches = file_matches)
    
    file_text   = get_text_from_file_name(Checks_Names[0])
    #sample_text = get_text_from_file_name(Sample_Names[0], False)
    return render_template('text_simi.html', sample_names = ["Nothing to show", ""], check_names = Checks_Names,
                            file_text = file_text, selected_file = Checks_Names[0])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')



"""
Samples = Sample_texts()
Samples_Corpus = sample_corpus_from_path(Samples)
#Sample_Names = get_filenames_from_paths(Samples)   # Removable
"""
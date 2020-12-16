from flask import Flask, render_template, request
from texts import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

Samples = Sample_texts()
Checks  = Check_texts()
Sample_Names = get_filenames_from_paths(Samples)   # Removable
Checks_Names = get_filenames_from_paths(Checks )

Checks_Map   = set()

Samples_Corpus = sample_corpus_from_path(Samples)
#file_matches = getMatchesText(get_text_from_file_name('orig_taska.txt'), Samples_Corpus) 

@app.route('/text_simi', methods=['GET', 'POST'])
def text_simi():
    if request.method == 'POST':
        choice       = request.form['file_selector']
        """
        if choice in Checks_Map:
            pass
        else:
        
        Checks_Map.add(choice)
        https://i.pinimg.com/originals/56/da/1f/56da1f2c3ec89b3406e5eb54a74c8994.gif
        """
        file_text    = get_text_from_file_name(choice)
        file_matches = getMatchesText(get_text_from_file_name(choice), Samples_Corpus) 

        return render_template('text_simi.html', sample_names = Sample_Names, check_names = Checks_Names,
                                file_text = file_text, selected_file = choice, file_matches = file_matches)
    
    file_text   = get_text_from_file_name(Checks_Names[0])
    sample_text = get_text_from_file_name(Sample_Names[0], False)
    return render_template('text_simi.html', sample_names = Sample_Names, check_names = Checks_Names,
                            file_text = file_text, selected_file = Checks_Names[0],
                            sample_text = sample_text)


if __name__ == "__main__":
    app.run(debug=True)
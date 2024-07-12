# norwegian-presidio
This is an anonymzation/de-identification tool for unstructured Norwegian text. It enables automatic detection of Personal Identifiable Information (PII) such as names, geographical places, organizations and Norwegian dates. 

The script utilize the [Presidio](https://microsoft.github.io/presidio/)
library for detecting and anonymizing PII. The supported entities can be 
found [here](https://microsoft.github.io/presidio/supported_entities/).
Currently this mostly just support PII anonymization for texts in
Norwegian Bokmål. 

## getting started

Download all files from this repository. 
Download [Presidio](https://microsoft.github.io/presidio/installation/#__tabbed_1_1)

If using SpaCy NLP model:
```
pip install presidio_analyzer
pip install presidio_anonymizer
python -m spacy download nb_core_news_lg
```

If using Stanza NLP model(the better version):
```
pip install "presidio_analyzer[stanza]"
pip install presidio_anonymizer
```

Run norwegian_text_anonymizer.py in the command line, passing arguments for source file (text to be anonymized) and target file (json file for anonymized text to be saved) and a config yaml file (nb_spacy.yaml or nb_stanza.yaml). 
\n
Example: python norwegian_text_anonymizer.py source_file.json  target_file.json nb_stanza.yaml


## accuracy

The Pattern Recognizers for Norwegian dates were tested on a translated version of OntoNotes. With a total of 3607 dates to be anonymized, the results were:\n
Precision: 0.91\n
Recall: 0.75\n
F1 Score: 0.82


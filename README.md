# norwegian-presidio
This is an anonymzation/de-identification tool for unstructured Norwegian text. It enables automatic detection of Personal Identifiable Information (PII) such as names, geographical places, organizations and Norwegian dates. 

The script utilize the [Presidio](https://microsoft.github.io/presidio/)
library for detecting and anonymizing PII. The supported entities can be 
found [here](https://microsoft.github.io/presidio/supported_entities/).
Currently this mostly just support PII anonymization for texts in
Norwegian Bokmål. 

## getting started

Download all files from this repository. 

Run norwegian_text_anonymizer.py in the command line, passing arguments for source file (text to be anonymized) and target file (json file for anonymized text to be saved) and a config yaml file (nb_spacy.yaml or nb_stanza.yaml). 


## accuracy

The Pattern Recognizers for Norwegian dates were tested on a translated version of OntoNotes. 
Precision: 0.91
Recall: 0.75
F1 Score: 0.82


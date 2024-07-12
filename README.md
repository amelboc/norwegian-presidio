# norwegian-presidio
This is an anonymzation/de-identification tool for unstructured Norwegian text. It enables automatic detection of Personal Identifiable Information (PII) such as names, geographical entities, organizations and Norwegian dates. The recognized PII will be replaced by the entity name during anonymization. For example: Oslo, Norway will be anonymized as <GEO-POLITICAL ENTITY\>

The script utilize the [Presidio](https://microsoft.github.io/presidio/)
library for detecting and anonymizing PII. The supported entities can be 
found [here](https://microsoft.github.io/presidio/supported_entities/). In addition to the supported entities, the script also loads Spacy NLP model or Stanza NLP model depending on the user's choice. Both of these NLP models calls NorNE's NER model which can be found [here](https://github.com/ltgoslo/norne). Additionally, PatternRecognizers have been created to recognize dates, time periods and age in Norwegian in different formats. 
Currently this just support PII anonymization for texts in
Norwegian Bokmål. 

## getting started

Download all files from this repository. 
Download [Presidio](https://microsoft.github.io/presidio/installation/#__tabbed_1_1).

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

Example: 
```
python norwegian_text_anonymizer.py source_file.json  target_file.json nb_stanza.yaml
```

The script expects the source file in a .txt, .yaml or .json file. If in .txt or .yaml, the text must be in string format. For example:
```
"Han jobbet i Oslo i 24 år. Når har han flyttet til Bergen."
```
If the source file is a .json file, the text must be in a single list. Either the whole text as one string in the list or split into multiple strings/sentences. For example:
```
["Han jobbet i Oslo i 24 år. Når har han flyttet til Bergen."]
```
OR
```
["Han jobbet i Oslo i 24 år.", "Nå har han flyttet til Bergen."]
```

If the source text is very large, the script will split the file into parts in order to complete detection and anonymization. To process 67381 sentences of a translated OntoNotes of different lengths (from 8 to 443 characters long), the program takes around 8min minuttes using the stanza config file. 

The script returns the source text, anonymized, to the .json file named for target file. It it is returned in the form of a string in a list. 

## accuracy

The Pattern Recognizers for Norwegian dates were tested on a translated version of OntoNotes. With a total of 3607 dates to be anonymized, the results were:

Precision: 0.92
Recall: 0.75
F1 Score: 0.83


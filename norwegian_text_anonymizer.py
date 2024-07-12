from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.context_aware_enhancers import LemmaContextAwareEnhancer
import json
import argparse 
import sys
import yaml

parser = argparse.ArgumentParser(description="Anonymize Norwegian text file. Pass a source file, target file and a configuration file. ", epilog="Example: python norwegian_text_anonymizer.py source_file.json target_file.json config_file.yaml")
parser.add_argument('source_file', type=str, help='text file to be anonymized')
parser.add_argument('target_file', type=str, help='target file to save anonymization')
parser.add_argument('config_file', type=str, help='yaml congiguration file')

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

if args.source_file:
    input_file = args.source_file
    if input_file.endswith('.txt'):
        with open(input_file) as txt_file:
            norwegian_text = txt_file.read()
            norwegian_text = [norwegian_text]
    elif input_file.endswith('.json'):
        with open(input_file) as json_file:
            norwegian_text = json.load(json_file)
    elif input_file.endswith('.yaml'):
        with open(input_file) as yaml_file:
            norwegian_text = yaml.safe_load(yaml_file)
            norwegian_text = [norwegian_text]
    else:
        raise ValueError("Source file must be a .txt or .json file.")


if args.target_file:
    if args.target_file.endswith('.json'):
        output_file=args.target_file
    else: 
        raise ValueError("Target file must be a .json file.")

if args.config_file:
    CONFIG_FILE=args.config_file


print("\nAnonymizing file: {i}. ".format(i=input_file))


# create NLP engine based on config
provider = NlpEngineProvider(conf_file=CONFIG_FILE)
nlp_engine_with_norwegian_bokmaal = provider.create_engine()

context_enhancer = LemmaContextAwareEnhancer(context_similarity_factor=0.45, 
                                             min_score_with_context_similarity=0.4,
                                             context_prefix_count=0,
                                             context_suffix_count=1)


# loading predefined recognizers 
registry = RecognizerRegistry()
registry.load_predefined_recognizers(
    nlp_engine=nlp_engine_with_norwegian_bokmaal, 
    languages=["nb"]
)


# pass the NLP engine and supported languages to AnalyzerEngine
analyzer = AnalyzerEngine(
    registry=registry,
    context_aware_enhancer=context_enhancer,
    nlp_engine=nlp_engine_with_norwegian_bokmaal,
    supported_languages=["nb"]
)


# DD. month YYYY/YY e.g. 1. januar 2019 or 10. januar 89
date_month_year_pattern = Pattern(name="date_month_year_pattern",regex=r"\b(([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\.\s((J|j)anuar|(F|f)ebruar|(M|m)ars|(A|a)pril|(M|m)ai|(J|j)uni|(J|j)uli|(A|a)ugust|(S|s)eptember|(O|o)ktober|(N|n)ovember|(D|d)esember)\s((18|19|20)[0-9]{2}|\d{2}))\b", score = 0.5)
# DD.MM.YYYY or DD.MM.YY or D.MM.YYYY or D.MM.YY or DD.M.YYYY or DD.M.YY or D.M.YY or D.M.YYYY
date_month_year_pattern_2 = Pattern(name="date_month_year_pattern_2",regex=r"(\b(1[0-9]|2[0-9]|3[0,1]|0?[1-9])\.(1[0-2]|0?[1-9])\.((18|19|20)[0-9]{2}|\d{2})\b)", score = 0.5)
# month and year e.g. Januar 2020
month_year_pattern = Pattern(name="month_year_pattern",regex=r"\b((J|j)anuar|(F|f)ebruar|(M|m)ars|(A|a)pril|(M|m)ai|(J|j)uni|(J|j)uli|(A|a)ugust|(S|s)eptember|(O|o)ktober|(N|n)ovember|(D|d)esember)\s(((18|19|20)[0-9]{2}|\d{2}))\b", score = 0.5)
# month e.g. februar
month_pattern = Pattern(name="month_pattern",regex=r"\b((J|j)anuar|(F|f)ebruar|(M|m)ars|(A|a)pril|(M|m)ai|(J|j)uni|(J|j)uli|(A|a)ugust|(S|s)eptember|(O|o)ktober|(N|n)ovember|(D|d)esember)\b", score = 0.5)
# DD. month e.g. 20. januar 
date_month_pattern = Pattern(name="date_month_pattern",regex=r"\b(([1-9]|0[1-9]|[1-2][0-9]|3[0-1])\.\s((J|j)anuar|(F|f)ebruar|(M|m)ars|(A|a)pril|(M|m)ai|(J|j)uni|(J|j)uli|(A|a)ugust|(S|s)eptember|(O|o)ktober|(N|n)ovember|(D|d)esember))\b", score=0.5)
 # YYYY/YY-årene/tallet/åra e.g. 80-tallet, 1890-årene
decade_pattern = Pattern(name="norwegian_years_pattern",regex=r"(\b(((18|19|20)[0-9]0|[1-9]0)-(årene|åra|tallet))\b)", score = 0.5)


norwegian_date_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[date_month_year_pattern, date_month_year_pattern_2, month_year_pattern, date_month_pattern, month_pattern, decade_pattern])
analyzer.registry.add_recognizer(norwegian_date_recognizer)


# quantity looking like years e.g. 2000 (kroner)
quantity_pattern = Pattern(name="quantity",regex=r"\b(18|19|20)[0-9]{2}\b", score = 0.4)

quantity_recognizer = PatternRecognizer(supported_entity="QUANTITY", supported_language="nb", patterns=[quantity_pattern], context=["kroner", "meter", "omtrent", "km", "kilometer", "millimeter", "mil", "dollar", "euro", ""])
analyzer.registry.add_recognizer(quantity_recognizer)

# YYYY will take years from 1800-2099
norwegian_year_pattern = Pattern(name="norwegian_year_pattern",regex=r"\b(18|19|20)[0-9]{2}\b", score = 0.5)

norwegian_year_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_year_pattern])
analyzer.registry.add_recognizer(norwegian_year_recognizer)


# years in letter fromat e.g. nittenåttifire, tjuetjueto
norwegian_year_letter_pattern = Pattern(name="norwegian_year_letter_pattern", regex=r"\b(((A|t)ten|(N|n)itten|(T|t)jue)(null|ti|ellve|tolv|tretten|fjorten|femten|seksten|sytten|atten|nitten|tjue|tretti|førti|femti|seksti|sytti|åtti|nitti)(en|to|tre|fire|fem|seks|sju|åtte|ni)?)\b", score=0.5)

norwegian_year_letter_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_year_letter_pattern])
analyzer.registry.add_recognizer(norwegian_year_letter_recognizer)

# years in letter format but long version e.g. attenhundreogfjorten, totusenogfjorten
norwegian_year_letter_pattern_long = Pattern(name="norwegian_year_letter_pattern_long", regex=r"\b(((A|a)tten|(N|n)itten)hundre|(T|t)otusen)(og)?(en|to|tre|fire|fem|seks|syv|sju|åtte|ni|ti|ellve|tolv|tretten|fjorten|femten|seksten|sytten|atten|nitten|tjue|tretti|førti|femti|seksti|sytti|åtti|nitti)?(en|to|tre|fire|fem|seks|sju|åtte|ni|ti)?\b", score=0.5)

norwegian_year_letter_recognizer_long = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_year_letter_pattern_long])
analyzer.registry.add_recognizer(norwegian_year_letter_recognizer_long)

# years in letter format but the "old way" e.g. nittenniognitti, tyvetoogtyve
norwegian_year_letter_pattern_old = Pattern(name="norwegian_year_letter_pattern_old", regex=r"\b(atten|nitten|tyve)(en|to|tre|fire|fem|seks|syv|åtte|ni)(og)(tyve|tretti|førti|femti|seksti|sytti|åtti|nitti)\b", score = 0.5)
norwegian_year_letter_recognizer_old = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_year_letter_pattern_old])
analyzer.registry.add_recognizer(norwegian_year_letter_recognizer_old)

# age in numbers e.g. 12-år gammle or 10 år gammel (from 1-199)
norwegian_age_number_pattern = Pattern(name="norwegian_age_number_pattern",regex=r"\b([1-9]{1,2}[0-9]{0,1})(\s|-)(år|årene|måneder|måned|månedene|dagene|dager|uker|uke)\s(gammel|gamle)\b", score = 0.5)
# age or time period e.g. 20 år, 10 måneder
norwegian_age_number_pattern_2 = Pattern(name="norwegian_age_number_pattern_2",regex=r"\b([1-9]{1,2}[0-9]{0,1})(\s|-)(år|årene|måneder|måned|månedene|dagene|dager|uker|uke)\b", score = 0.5)
norwegian_age_number_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_age_number_pattern, norwegian_age_number_pattern_2, decade_pattern])
analyzer.registry.add_recognizer(norwegian_age_number_recognizer)

# age in letters e.g. "tjueen år" fom 1-119år or 12 måneder gammel
norwegian_age_letter_pattern = Pattern(name="norwegian_age_letter_pattern",regex=r"\b((E|e|é)n|(E|e)tt|(T|t)o|(T|t)re|(F|f)ire|(F|f)em|(S|s)eks|(S|s)yv|(S|s)ju|(Å|å)tte|(N|n)i|(T|t)i|(E|e)llve|(T|t)olv|(T|t)retten|(F|f)jorten|(F|f)emten|(S|s)eksten|(S|s)ytten|(A|a)tten|(N|n)itten|(T|t)jue|(T|t)retti|(F|f)ørti|(F|f)emti|(S|s)eksti|(S|s)ytti|(Å|å)tti|(N|n)itti|(H|h)undre)(og)?(en|to|tre|fire|fem|seks|syv|åtte|ni|ti|ellve|tolv|tretten|fjorten|femten|seksten|sytten|atten|nitten)?\s(år|årene|måneder|måned|månedene|dagene|uker|uke)\s(gammel|gamle)\b", score = 0.5)
norwegian_age_letter_pattern_2 = Pattern(name="norwegian_age_letter_pattern_2",regex=r"(\b((E|e|é)n|(E|e)tt|(T|t)o|(T|t)re|(F|f)ire|(F|f)em|(S|s)eks|(S|s)yv|(S|s)ju|(Å|å)tte|(N|n)i|(T|t)i|(E|e)llve|(T|t)olv|(T|t)retten|(F|f)jorten|(F|f)emten|(S|s)eksten|(S|s)ytten|(A|a)tten|(N|n)itten|(T|t)jue|(T|t)retti|(F|f)ørti|(F|f)emti|(S|s)eksti|(S|s)ytti|(Å|å)tti|(N|n)itti|(H|h)undre)(og)?(en|to|tre|fire|fem|seks|syv|åtte|ni|ti|ellve|tolv|tretten|fjorten|femten|seksten|sytten|atten|nitten)?\s(år|årene|måneder|måned|månedene|dagene|uker|uke)\b)", score = 0.5)
norwegian_age_letter_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_age_letter_pattern_2, norwegian_age_letter_pattern])
analyzer.registry.add_recognizer(norwegian_age_letter_recognizer)

# weekdays e.g. søndag or Søndag 
norwegian_nb_weekday_pattern = Pattern(name="norwegian_nb_weekday_pattern",regex=r"\b((M|m)an|(T|t)irs|(O|o)ns|(T|t)ors|(F|f)re|(L|l)ør|(S|s)øn)dag\b", score = 0.5)
norwegian_nb_weekday_recognizer = PatternRecognizer(supported_entity="DATE", supported_language="nb", patterns=[norwegian_nb_weekday_pattern])
analyzer.registry.add_recognizer(norwegian_nb_weekday_recognizer)



# loading anonymizer engine 
anonymize_engine=AnonymizerEngine()

# splitting text into more pieces as Presidio analyzer cannot take more than 1 mill characters at once 
no_text = [norwegian_text[i:i + 8445] for i in range(0, len(norwegian_text), 8445)] 

anonymized_results = []
count = 1
for part in no_text:
    dataset = ' '.join(part)
    results_nb = analyzer.analyze(text=dataset, language="nb", score_threshold=0.3) # analyze text to find PIIs
    nb_anonymize = anonymize_engine.anonymize(text = dataset, analyzer_results=results_nb) # anonymize the analyzed text 
    anonymized_results.append([nb_anonymize.text])
    print("Anonymized part ", count, "/", len(no_text))
    count += 1
   
# flatten lists of results 
anonymized_text = [sent for sentence in anonymized_results for sent in sentence]
json_anonymization = json.dumps(anonymized_text, ensure_ascii=False)

with open(output_file, "w") as file:
    file.write(json_anonymization)

print("\nAnonymization completed. Anonymized version was written to: "+output_file)

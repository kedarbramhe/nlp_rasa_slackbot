# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os

from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])


class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = translator.translate(query_lang, dest='en').text
            query_lang = query_lang.lower().capitalize()
            print(query_lang)

            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "La lingua %s appartiene alla famiglia %s\n con Genus as %s\n e ha il codice ISO %s\n Hai trovato quello che cercavi?" % (translator.translate(
                    out_row["Name"], dest='en').text, translator.translate(out_row["Family"], dest='en').text, translator.translate(out_row["Genus"], dest='en').text, translator.translate(out_row["ISO_codes"], dest='en').text)
                dispatcher.utter_message(text=out_text)
            else:
                dispatcher.utter_message(
                    text="Scusate! Non abbiamo record per la lingua %s" % query_lang)

        return []


class ActionCountrySearch(Action):

    def name(self) -> Text:
        return "action_country_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)

        data_path2 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "walslanguage.csv")
        wals_data2 = pd.read_csv(data_path2)

        data_path3 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "countrylanguage.csv")
        wals_data3 = pd.read_csv(data_path3)

        data_path4 = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "country.csv")
        wals_data4 = pd.read_csv(data_path4)

        entities = list(tracker.get_latest_entity_values("language"))
        print(entities)

        if len(entities) > 0:
            query_lang = entities.pop()
            # translator = google_translator()
            #query_lang = translator.translate(query_lang, lang_tgt='en')

            # query_lang = str(translator.translate(query_lang, lang_tgt='en'))

            #query_lang = str(google_translate(query_lang))
            # query_lang = query_lang.lower().capitalize().strip()

            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
            print(out_row)
            out_row2 = wals_data2[wals_data2["ascii_name"] == query_lang.lower()].to_dict("records")
            #print(out_row2[0]["pk"])
            out_row3 = wals_data3[wals_data3["language_pk"] == out_row2[0]["pk"]].to_dict("records")
            print(out_row3)
            out_row4 = wals_data4[wals_data4["pk"] == out_row3[0]["country_pk"]].to_dict("records")
            print(out_row4)

            if len(out_row) > 0:
                out_row = out_row[0]
                # import pdb;pdb.set_trace()
                out_text = "lingua "+out_row["Name"]+" è parlata in "+out_row4[0]["name"]+" \n Hai trovato quello che cercavi?"
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Scusate! Non abbiamo record per la lingua %s" % query_lang)

        return []

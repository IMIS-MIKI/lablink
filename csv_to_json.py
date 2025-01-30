import pandas as pd
import json

# Pfade zu den Dateien
csv_file_path = '/Users/.../.csv'
loinc_file_path = '/Users/.../.csv'

# CSV-Dateien einlesen
df = pd.read_csv(csv_file_path)
loinc_df = pd.read_csv(loinc_file_path, sep=',')  # Komma als Separator angeben

# Filter: Nur Zeilen, in denen "Interne Laborbezeichnung" und "LOINC" gefüllt sind
df_filtered = df.dropna(subset=["Interne Laborbezeichnung", "LOINC"])

# LOINC-Komponenten als Dictionary (Mapping LOINC_NUM -> COMPONENT)
loinc_mapping = dict(zip(loinc_df["LOINC_NUM"], loinc_df["LONG_COMMON_NAME"]))

# Template für die Concept Map
concept_map = {
    "resourceType": "ConceptMap",
    "id": "ukshlabor-loinc",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2025-01-01T00:00:00.000+00:00"
    },
    "url": "http://uksh.de/klinischechemie/fhir/ConceptMap/labor-loinc",
    "version": "20210517",
    "name": "UkshLaborLoinc",
    "title": "Lokale Laborcodes - LOINC [UKSH]",
    "status": "draft",
    "publisher": "Universitätsklinikum Schleswig Holstein",
    "contact": [
        {
            "name": "[Name]",
            "telecom": [
                {
                    "system": "email",
                    "value": "[mailadresse]"
                }
            ]
        }
    ],
    "description": "Mapping von lokalen Laborcodes auf LOINC. Quelle: LabIndex_Scrapper_V01",
    "sourceUri": "http://uksh.de/klinischechemie/fhir/ValueSet/Laborparameter",
    "targetUri": "http://uksh.de/klinischechemie/fhir/ValueSet/loinc-kc",
    "group": [
        {
            "source": "http://uksh.de/klinischechemie/fhir/CodeSystem/Laborparameter",
            "target": "http://loinc.org",
            "element": []
        }
    ]
}

# Elemente aus der gefilterten CSV-Datei hinzufügen
for _, row in df_filtered.iterrows():
    loinc_code = row["LOINC"]
    loinc_display_name = loinc_mapping.get(loinc_code, "LOINC Display Name nicht gefunden")  # Display Name nachschlagen

    element = {
        "code": row["Interne Laborbezeichnung"],  # Lokale Laborbezeichnung als Code
        "display": row["Titel"],  # Deutscher Titel der Laboruntersuchung
        "target": [
            {
                "extension": [
                    {
                        "url": "http://ontoserver.csiro.au/snapper/map-extensions",
                        "extension": [
                            {
                                "url": "map-status",
                                "valueString": "Draft"
                            }
                        ]
                    }
                ],
                "code": loinc_code,  # LOINC-Code
                "display": loinc_display_name,  # LOINC Long Common Name aus loinc.csv
                "equivalence": "equivalent"
            }
        ]
    }
    concept_map["group"][0]["element"].append(element)

# Ausgabe der Concept Map als JSON
output_file_path = '/Users/.../LOINC_Conceptmap_v1.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(concept_map, json_file, ensure_ascii=False, indent=2)

print(f"Concept Map wurde erfolgreich erstellt: {output_file_path}")

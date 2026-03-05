import re
from spellchecker import SpellChecker

def clean_ocr_text(file_path, use_spellcheck=False):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    ligatures = {
        "ﬁ": "fi",
        "ﬀ": "ff",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl"
    }

    for k, v in ligatures.items():
        text = text.replace(k, v)

    text = text.replace("|", "I")
    text = text.replace("_", " ")

    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    text = re.sub(r'[ \t]+', ' ', text)

    text = re.sub(r'\n{3,}', '\n\n', text)

    if use_spellcheck:
        spell = SpellChecker()
        tokens = re.findall(r'\w+|[^\w\s]', text)

        corrected = []
        for token in tokens:
            if token.isalpha():
                suggestion = spell.correction(token)
                if suggestion:
                    if token.istitle():
                        suggestion = suggestion.capitalize()
                    corrected.append(suggestion)
                else:
                    corrected.append(token)
            else:
                corrected.append(token)

        text = ''.join(
            w if re.match(r'[^\w\s]', w) else ' ' + w for w in corrected
        ).strip()

    return text


input_file = "Parliamentarydebates_01-031962.txt"
output_file = "cleaned_output.txt"

cleaned_text = clean_ocr_text(input_file, use_spellcheck=False)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Cleaning complete.")
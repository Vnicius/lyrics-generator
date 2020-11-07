import re
import argparse
import json

def preprocess_lyric(lyric: str) -> str:
    text = lyric.lower().strip()
    text = re.sub(r'([.:?!+(),]+)', r' \1 ', text)
    text = re.sub(r'(^|(?<=\W))(-)(?=\w)', r' \2 ', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

if __name__ == '__main__':
    parser =  argparse.ArgumentParser()
    parser.add_argument('-f','--files', help='JSON files from scraper', type=str, nargs='+', required=True)
    parser.add_argument('-o','--output', help='Output file', type=str, required=True)
    args = parser.parse_args()

    with open(args.output, 'w', encoding='utf-8') as out_file:
        
        for file_name in args.files:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)

                for d in data:
                    lyrics = ""
                    for v in d['verses']:
                        if len(v.strip()) > 0:
                            lyrics += preprocess_lyric(v) + " # "
                    
                    if len(lyrics.strip()) > 0:
                        out_file.write(lyrics.strip() + "\n")
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
    parser.add_argument('json_file', help='JSON file from scrapper', type=str)
    parser.add_argument('out_file', help='Output file', type=str)
    args = parser.parse_args()

    with open(args.json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

        with open(args.out_file, 'w', encoding='utf-8') as out_file:
            for d in data:
                lyrics = ""
                for v in d['verses']:
                    if len(v.strip()) > 0:
                        lyrics += preprocess_lyric(v) + " # "
                
                out_file.write(lyrics.strip() + "\n")
# 🎼 Lyrics Generator 🎼

Generation lyrics using **[textgenrnn](https://github.com/minimaxir/textgenrnn)**.

## Getting the data

Get the data using the scraper for _[letras.mus.br](https://www.letras.mus.br/)_

Example:

For

```
    https://www.letras.mus.br/[ARTIST]
```

Do

```
    $ python scraper.py ARTIST
```

The output file will be `ARTIST.json`.

## Preprocessing the data

You can preprocess the data using the provided script.

```
    $ python preprocess.py -f ARTIST.json ARTIST2.json -o output.txt
```

## Train and use example

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Vnicius/lyrics-generator/blob/main/lyrics-generator.ipynb)

Open the [Jupyter Notebook](./lyrics-generator.ipynb).

```python
from textgenrnn import textgenrnn

textgen = textgenrnn(name="new_model")
textgen.reset()

# Tranning
textgen.train_from_file(data_path, num_epochs=10,
                        gen_epochs=2, new_model=True,
                        word_level=True, rnn_bidirectional=True,
                        rnn_size=64, dim_embeddings=300)

# Generating
for verse in textgen.generate(n=1, temperature=0.5, return_as_list=True)[0].split('#'):
  text = verse.strip()
  if len(text) > 0:
    print(text.capitalize())
```

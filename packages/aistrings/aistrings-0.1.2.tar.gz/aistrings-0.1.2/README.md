# AI Strings

AiStrings uses language models to build a string API that is aware of semantics.
The built in string APIs operate on syntax or morphology.
For example matching two strings with a regex or a fuzzy string matching algorithm will never match
2 strings that essentially mean the same but look completely different.

AiStrings provides semantics aware string APIs with a familiar interface.

```python
from dotenv import load_dotenv
from aistrings import AiStrings

load_dotenv()

astr = AiStrings(provider_name="openai", model_name="gpt-3.5-turbo-0125")

targets = [
    "The cat sleeps too much",
    "The dog jumps over the fence",
    "The cat jumps over the fence",
    "I am so happy"
]
query = "The cat is very agile!"

response, index = astr.match(query, targets)
print(f"Option at index {index} is the best: \"{response}\"")
```

```
Option at index 2 is the best: "The cat jumps over the fence"
```

Keep track of the costs with:

```python
astr.log_history()
# or
print("Total Cost: ", astr.cumulative_cost)
```

```
History
----------------------
  Action: match
  Input: The cat is very agile!
  Output: The cat jumps over the fence
  Cost: 4.35e-05
  Time: 2024-05-14 14:50:25.698692

Total Cost: 4.35e-05
----------------------
# or
Total Cost: 4.35e-05
```

Currently available operations:

- astr.summarize
- astr.match
- astr.split

coming soon:
- astr.replace
- astr.substr
- astr.translate
- astr.answer
- astr.is_factual
- astr.make_verbose
- astr.elaborate
- astr.correct_grammar
- astr.detect_lang
- astr.detect_sentiment

## More Examples

### Split

```python
from dotenv import load_dotenv

from aistrings import AiStrings

load_dotenv()

astr = AiStrings(provider_name="openai", model_name="gpt-4-0125-preview", temperature=1)

text = "I have never seen Saturn through a telescope, but I would really love to see it once."
criterion = "Split the text using names of planets of the solar system as separators."
response = astr.split(text, criterion)
astr.log_history()
print(response)
```

```
['I have never seen ', ' through a telescope, but I would really love to see it once.']
```

### Join

```python
from dotenv import load_dotenv

from aistrings import AiStrings

load_dotenv()

astr = AiStrings(provider_name="openai", model_name="gpt-4-0125-preview")

text_list = [
    "The cat sleeps too much during the day, so it wakes up in the night and wants to play.",
    "When the cat wakes up in the night and wants to play it usually starts walking across my pillow.",
]
criterion = "Join the texts and remove duplicate information and use as few words as possible."

response = astr.join(text_list, criterion)
print(response)
```

```
The cat sleeps too much during the day, so it wakes up in the night and wants to play, usually starting by walking across my pillow.
```

### Summarize

```python
from dotenv import load_dotenv

from aistrings import AiStrings

load_dotenv()

astr = AiStrings(provider_name="openai", model_name="gpt-3.5-turbo-0125")
response = astr.summarize(
    "Mars is the fourth planet from the Sun. The surface of Mars is orange-red because it is covered in iron(III) oxide dust, giving it the nickname 'the Red Planet'.[21][22]"
    " Mars is among the brightest objects in Earth's sky, and its high-contrast albedo features have made it a common subject for telescope viewing. "
    "It is classified as a terrestrial planet and is the second smallest of the Solar System's planets with a diameter of 6,779 km (4,212 mi). "
    "In terms of orbital motion, a Martian solar day (sol) is equal to 24.5 hours, and a Martian solar year is equal to 1.88 Earth years (687 Earth days). "
    "Mars has two natural satellites that are small and irregular in shape: Phobos and Deimos. "
)
print(response)

```

Output:

```
Mars is the fourth planet from the Sun, known as the Red Planet due to its orange-red surface covered in iron(III) oxide dust. 
It is a terrestrial planet with a diameter of 6,779 km and has a solar day of 24.5 hours and a solar year of 1.88 Earth years. 
Mars has two small, irregular-shaped natural satellites: Phobos and Deimos.
```




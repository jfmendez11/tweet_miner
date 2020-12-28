import re
import string
import stanza
from spacy_stanza import StanzaLanguage
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords


class TextCleaner:
  nlp = {}
  
  def __init__(self):
    snlp = stanza.Pipeline(lang="es")
    self.nlp = StanzaLanguage(snlp)
  
  # Calls the clean function and tokenizes specially for Tweets (removes mentions, keep hashtags)
  def tokenize_tweet(self, tweet):
    tknzr = TweetTokenizer(strip_handles=True)
    cleaned_tweet = self.clean_text(tweet)
    return tknzr.tokenize(cleaned_tweet)
  
  # Checks if the given character is punctuation or not, excluding Twitter special chaarcters (@, #)
  def is_not_punctuation(self, char):
    is_punctuation = char not in string.punctuation and not char == "¡" and not char == "¿"
    return is_punctuation or char == "@" or char == "#"
  
  # Removes numbers, emojis, punctuation, whitespaces and lowers all characters
  def clean_text(self, text):
    # remove numbers
    text_nonum = re.sub(r'\d+', '', text)
    # remove emojis
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        u"\U00002500-\U00002BEF"  # chinese char
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        u"\U0001f926-\U0001f937"
                                        u"\U00010000-\U0010ffff"
                                        u"\u2640-\u2642"
                                        u"\u2600-\u2B55"
                                        u"\u200d"
                                        u"\u23cf"
                                        u"\u23e9"
                                        u"\u231a"
                                        u"\ufe0f"  # dingbats
                                        u"\u3030"
                                        "]+", flags=re.UNICODE)
    text_noemoji = regrex_pattern.sub(r'', text_nonum)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char.lower() for char in text_noemoji if self.is_not_punctuation(char)])
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_no_doublespace
  
  # Removes stopwords based on nltk spanish stopwords and https://github.com/stopwords-iso/stopwords-es/blob/master/stopwords-es.txt
  def remove_stopwords(self, tweet):
    tokens = self.tokenize_tweet(tweet)
    return [self.join_hashtag(tokens, i) for i in range(0, len(tokens)) if not tokens[i] in stopwords.words('spanish2') and not tokens[i].startswith("https") and not tokens[i] == "am" and not tokens[i] == "pm"]
  
  # Case when the hashtag is separated from the text
  def join_hashtag(self, tokens, i):
    if tokens[i] == "#" and len(tokens[i]) == 1:
      return tokens[i] + tokens[i+1]
    else:
      return tokens[i]
    
  # Lemmatizes the remaining words, based on stanza's spanish NLP and using spacy-stanza NLP
  def lemmatize(self, tweet):
    tokens = self.remove_stopwords(tweet)
    for i in range(0, len(tokens)):
      doc = self.nlp(tokens[i])
      for token in doc:
        tokens[i] = token.lemma_
    print(tokens)
    return tokens
  
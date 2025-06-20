
from transformers import pipeline
import re

# Trie Node and Trie
_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline("text-classification", model="bert-base-uncased")
    return _classifier
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.category = None

class BadWordTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, phrase, category):
        node = self.root
        for word in phrase.lower().split():
            if word not in node.children:
                node.children[word] = TrieNode()
            node = node.children[word]
        node.is_end = True
        node.category = category

    def detect(self, tokens):
        for i in range(len(tokens)):
            node = self.root
            j = i
            while j < len(tokens) and tokens[j] in node.children:
                node = node.children[tokens[j]]
                if node.is_end:
                    if i > 0 and tokens[i-1] in ["not", "don't", "didn't", "no"]:
                        return False, None, None
                    return True, node.category, " ".join(tokens[i:j+1])
                j += 1
        return False, None, None

# Alert logic
def send_alert_to_parent(message):
    print(f"\n🚨 ALERT: {message}")

def continue_typing():
    print("✅ No alert. Continue typing.")

# Categories and phrases
categories = {

    "Sexual Content": [
        "sex", "sexual", "porn", "naked", "nude", "boobs", "penis", "vagina", "dildo",
        "masturbation", "orgasm", "horny", "fuck", "blowjob", "anal", "intercourse",
        "sexting", "slut", "asshole", "erection", "cum", "pussy", "gay sex", "lesbian", "shemale",
        "tit", "dick", "cock", "milf", "pornstar", "cumshot", "stripper", "prostitute", "hooker",
        "threesome", "bondage", "fetish", "bdsm", "erotic", "xxx", "handjob", "creampie", "fisting",
        "pegging", "spank", "voyeur", "whore", "chest", "breasts", "penis", "clitoris",
    ],
    "Mental Health": [
        "depression", "depressed", "anxiety", "panic attack", "suicidal", "suicide",
        "kill myself", "want to die", "end my life", "hopeless", "worthless",
        "cut myself", "self-harm", "overdose", "feeling alone", "crying", "can't sleep",
        "numb", "empty inside", "feel dead", "no hope", "scared", "panic", "anxious",
        "stress", "overwhelmed", "breakdown", "self injury", "hurt myself", "kill yourself",
        "i want to die", "kill yourself", "cut myself", "end my life", "panic attack",
        "i don't want to live anymore", "i don't want to live", "i want to end it", "i can't live anymore",
        "nervous breakdown", "suicide attempt", "feeling hopeless", "dark thoughts",
        "want to disappear", "feeling trapped", "worthless life", "feeling rejected",
    ],
    "Violence": [
        "kill", "murder", "fight", "abuse", "beat", "assault", "weapon", "gun", "knife", "bomb",
        "shoot", "stab", "attack", "hit", "bullying", "harass", "threat", "violence", "hurt",
        "torture", "choke", "kill you", "kill him", "kill her", "shoot you", "rape", "terrorist",
        "massacre", "slap", "punch", "kick", "child abuse", "domestic violence", "gang violence",
    ],
    "Substance Abuse": [
        "drugs", "drug abuse", "cocaine", "heroin", "marijuana", "weed", "pot", "smoking",
        "vaping", "alcohol", "drunk", "overdose", "addict", "addiction", "meth", "crack",
        "pill", "xanax", "ecstasy", "lsd", "drug dealer", "smoke crack", "inject drugs",
        "buy drugs", "drug overdose", "intoxicated", "get high", "rehab",
    ],
    "Hate Speech": [
        "bitch", "idiot", "dumb", "retard", "faggot", "slut", "whore", "fag", "nigger", "chink",
        "kike", "gook", "spic", "racist", "bigot", "sexist", "homophobic", "hate", "racism",
        "discriminate", "terrorist", "extremist", "supremacist", "islamophobe", "anti-semitic",
        "nazi", "hate speech", "kill all", "go back", "dirty", "trash", "scum", "lowlife"
    ]
}



# Build the Trie
trie = BadWordTrie()
for category, phrases in categories.items():
    for phrase in phrases:
        trie.insert(phrase, category)

# ML Pipelines
toxic_classifier = pipeline("text-classification", model="unitary/toxic-bert")
sentiment_analyzer = pipeline("sentiment-analysis")
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# Tokenizer
def tokenize(text):
    return re.findall(r'\w+', text.lower())

# ML detection
def ml_check(text):
    toxicity = toxic_classifier(text[:512])[0]
    sentiment = sentiment_analyzer(text[:512])[0]
    emotion = emotion_analyzer(text[:512])[0][0]

    flagged = toxicity["label"] == "LABEL_1" and toxicity["score"] > 0.6
    explanation = {
        "toxic": toxicity,
        "sentiment": sentiment,
        "emotion": emotion
    }
    return flagged, explanation

def detect_content(text):
    tokens = tokenize(text)
    trie_found, category, matched_phrase = trie.detect(tokens)

    if trie_found:
        return True, {
            "reason": f"Matched phrase: '{matched_phrase}'",
            "category": category,
            "source": "Trie"
        }

    ml_flag, explanation = ml_check(text)
    if ml_flag:
        return True, {
            "reason": f"Toxicity Score: {explanation['toxic']['score']:.2f}",
            "category": "Toxic Content",
            "source": "ML Model",
            "sentiment": explanation["sentiment"],
            "emotion": explanation["emotion"]
        }

    return False, None
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('chunkers/maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class KeywordExtractor:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.stop_words = set(stopwords.words('english'))

    def extract_numerical_data(self, text):
        """Extract years, dates, numbers, and monetary values from text"""
        numerical_keywords = []
        
        # Extract years (1900-2100)
        years = re.findall(r'\b(19|20)\d{2}\b', text, re.IGNORECASE)
        numerical_keywords.extend(years)
        
        # Extract monetary values (e.g., $1M, 1 billion, 500k)
        monetary = re.findall(r'\$?\d+(?:\.\d+)?[bBmMkK]?\b', text, re.IGNORECASE)
        numerical_keywords.extend(monetary)
        
        # Extract dates (MM/DD/YYYY, DD-MM-YYYY, etc.)
        dates = re.findall(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text)
        numerical_keywords.extend(dates)
        
        # Extract month names and quarters
        months = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Q[1-4])\b', 
                          text, re.IGNORECASE)
        numerical_keywords.extend(months)
        
        # Extract percentages
        percentages = re.findall(r'\d+(?:\.\d+)?%', text)
        numerical_keywords.extend(percentages)
        
        return list(set(numerical_keywords))  # Remove duplicates

    def extract_multi_word_phrases(self, text):
        """Extract multi-word phrases and compound keywords"""
        phrases = []
        
        # Extract quoted phrases (e.g., 'No Kings')
        quoted = re.findall(r"['\"]([^'\"]+)['\"]", text)
        phrases.extend(quoted)
        
        # Extract compound keywords with hyphens or "and"
        # Handle patterns like "anti-Donald Trump", "North America", etc.
        compound_patterns = [
            r'\b(?:anti|pro|ex|non|pre|post)[-\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',  # anti/pro+name
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',  # Proper nouns (capitalized multi-word)
        ]
        
        for pattern in compound_patterns:
            matches = re.findall(pattern, text)
            phrases.extend(matches)
        
        return phrases

    def extract_named_entities(self, text):
        """Extract named entities like locations, people, organizations"""
        entities = []
        
        try:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Use named entity chunking
            ne_tree = ne_chunk(pos_tags, binary=False)
            
            # Extract entities
            for subtree in ne_tree:
                if hasattr(subtree, 'label'):
                    entity = ' '.join([word for word, tag in subtree.leaves()])
                    entities.append(entity)
        except Exception as e:
            # Fallback if NER fails
            pass
        
        return entities

    def extract_important_nouns(self, text):
        """Extract nouns that are important for news scraping"""
        important_nouns = []
        
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Extract proper nouns (NNP) and nouns (NN, NNS)
            for word, tag in pos_tags:
                if tag in ['NN', 'NNS', 'NNP', 'NNPS']:  # Singular, Plural, Proper nouns
                    if word.lower() not in self.stop_words and len(word) > 2:
                        important_nouns.append(word)
        except Exception as e:
            pass
        
        return important_nouns

    def clean_text(self, text):
        """Clean text for TF-IDF analysis"""
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove quoted phrases temporarily to analyze remaining text
        text = re.sub(r"['\"]([^'\"]*)['\"]", '', text)
        # Keep alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    def calculate_dynamic_top_k(self, text):
        """Dynamically calculate number of keywords based on text length"""
        text_length = len(text.split())
        
        if text_length <= 5:
            return 3
        elif text_length <= 10:
            return 5
        elif text_length <= 20:
            return 7
        elif text_length <= 40:
            return 10
        else:
            return 12

    def extract_keywords(self, text):
        """
        Extract comprehensive keywords from text including:
        - Numerical data (years, dates, months, percentages)
        - Named entities (people, locations, organizations)
        - Multi-word phrases
        - Important nouns
        - TF-IDF based keywords
        """
        top_k = self.calculate_dynamic_top_k(text)
        keywords_dict = {}  # Use dict to store keywords with scores
        
        # 1. Extract numerical data (highest priority)
        numerical_keywords = self.extract_numerical_data(text)
        for kw in numerical_keywords:
            keywords_dict[kw] = 10
        
        # 2. Extract quoted phrases and multi-word phrases
        phrases = self.extract_multi_word_phrases(text)
        for phrase in phrases:
            if phrase.strip():
                keywords_dict[phrase.strip()] = 9
        
        # 3. Extract named entities
        entities = self.extract_named_entities(text)
        for entity in entities:
            if entity.strip() and entity.lower() not in self.stop_words:
                keywords_dict[entity.strip()] = 8
        
        # 4. Extract important nouns
        nouns = self.extract_important_nouns(text)
        for noun in nouns:
            if noun not in keywords_dict:
                keywords_dict[noun] = 6
        
        # 5. Extract TF-IDF based keywords from cleaned text
        clean = self.clean_text(text)
        if clean.strip():
            try:
                tfidf = self.vectorizer.fit_transform([clean])
                scores = zip(
                    self.vectorizer.get_feature_names_out(),
                    tfidf.toarray()[0]
                )
                
                sorted_words = sorted(scores, key=lambda x: x[1], reverse=True)
                
                for word, score in sorted_words[:top_k]:
                    if word not in keywords_dict and word not in self.stop_words:
                        keywords_dict[word] = float(score) * 5  # Scale TF-IDF scores
            except:
                pass
        
        # Sort by priority score and return top keywords
        sorted_keywords = sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True)
        final_keywords = [kw for kw, score in sorted_keywords[:top_k]]
        
        return final_keywords


# Example usage
if __name__ == "__main__":
    extractor = KeywordExtractor()
    
    # Get single tweet input from user
    tweet = input("Enter a tweet: ").strip()
    
    if tweet:
        keywords = extractor.extract_keywords(tweet)
        print(f"\nTweet: {tweet}")
        print(f"\nKeywords extracted ({len(keywords)}): {keywords}")
        print("\nKeywords (one per line):")
        for i, kw in enumerate(keywords, 1):
            print(f"  {i}. {kw}")
    else:
        print("No tweet provided.")
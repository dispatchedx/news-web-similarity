import scrapy
import nltk
from nltk.tokenize import word_tokenize
import re



class Spidey(scrapy.Spider):
    name = 'Articles'
    allowed_domains = ['eu.usatoday.com']


    def start_requests(self):
        start_urls = ['http://eu.usatoday.com/news',
                      'https://eu.usatoday.com/news/factcheck',
                      'https://eu.usatoday.com/news/politics',
                      'https://eu.usatoday.com/news/race-in-america',
                      'https://eu.usatoday.com/sports/nfl',
                      'https://eu.usatoday.com/sports/mlb',
                      'https://eu.usatoday.com/sports/ncaaf',
                      'https://eu.usatoday.com/sports/nba',
                      'https://eu.usatoday.com/sports/nhl',
                      'https://eu.usatoday.com/sports/tennis',
                      'https://eu.usatoday.com/sports/ncaab',
                      'https://eu.usatoday.com/news/coronavirus',
                      'http://eu.usatoday.com/sports',
                      'http://eu.usatoday.com/entertainment',
                      'https://eu.usatoday.com/entertainment/music',
                      'https://eu.usatoday.com/entertainment/tv',
                      'https://eu.usatoday.com/entertainment/movies',
                      'https://eu.usatoday.com/entertainment/music',
                      'https://eu.usatoday.com/entertainment/books',
                      'https://eu.usatoday.com/life/health-wellness',
                      'https://eu.usatoday.com/humankind',
                      'https://eu.usatoday.com/problemsolved',
                      'https://eu.usatoday.com/shopping/back-to-school',
                      'http://eu.usatoday.com/tech',
                      'https://eu.usatoday.com/tech/gaming',
                      'https://eu.usatoday.com/tech/tips',
                      'https://eu.usatoday.com/tech/reviews',
                      'http://eu.usatoday.com/travel',
                      'https://eu.usatoday.com/travel/destinations',
                      'https://eu.usatoday.com/travel/experience-america',]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        item = {}
        url = "https://eu.usatoday.com"
        content = response.css('#section-stories')
        for article_link in content.xpath('.//a').xpath('.//@href').extract():
            if 'https' not in article_link:
                item['article_url'] = url+article_link
                yield(scrapy.Request(url=url+article_link,callback=self.parse_articles))

    def parse_articles(self, response):

        stuff = {}
        # Get article text from response
        text = ''.join(response.css('#truncationWrap p::text').extract())
        url = response.request.url

        # download pos tagger
        nltk.download('averaged_perceptron_tagger')

        # Remove punctuation from text
        tagged_text = ''.join([re.sub('[!@#$%&()*+,\\/:.;”“<=>?\"[\]^_—`{|}~\d…]', ' ', word) for word in text])

        # Tokenize text
        tokenized_text = word_tokenize(tagged_text)

        # POS Tagging
        tagged_text = nltk.pos_tag(tokenized_text)

        # Closed tag categories
        closed_tag_categories = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO',
                                 'UH', 'WDT',
                                 'WP', 'WP$', 'WRB']

        Lemmatizer = nltk.stem.WordNetLemmatizer()
        # Transform words to lowercase lemmas, and remove closed tag categories
        tagged_text = [(Lemmatizer.lemmatize(word[0].lower()), word[1]) for word in tagged_text if word[1] not in closed_tag_categories]

        # Create frequency distribution
        TF = nltk.FreqDist(word[0] for word in tagged_text)
        stuff[url] = TF
        # Save to Articles.json
        yield stuff


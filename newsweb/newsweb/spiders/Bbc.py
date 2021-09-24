import scrapy
import nltk
from nltk.tokenize import word_tokenize
import re

class Spidey_bbc(scrapy.Spider):
    name = 'Bbc'
    allowed_domains = ['www.bbc.com']

    def start_requests(self):
        start_urls = ['https://www.bbc.com/news/world',
                      "https://www.bbc.com/news",
                      "https://www.bbc.com/news/business-15521824",
                      "https://www.bbc.com/news/business/global_car_industry",
                      "https://www.bbc.com/news/business-12686570",
                      "https://www.bbc.com/news/business/business_of_sport",
                      "https://www.bbc.com/news/business-11428889",
                      "https://www.bbc.com/news/business/market-data",
                      "https://www.bbc.com/news/business-22434141",
                      "https://www.bbc.com/news/localnews",
                      "https://www.bbc.com/news/business/companies",
                      "https://www.bbc.com/news/business-45489065",
                      "https://www.bbc.com/news/business/economy",
                      "https://www.bbc.com/news/politics",
                      "https://www.bbc.com/news/world/europe/isle_of_man",
                      "https://www.bbc.com/news/world/europe/guernsey",
                      "https://www.bbc.com/news/politics/parliaments",
                      "https://www.bbc.com/news/world/europe/jersey",
                      "https://www.bbc.com/news/education",
                      "https://www.bbc.com/news/disability",
                      "https://www.bbc.com/naidheachdan",
                      "https://www.bbc.com",
                      "https://www.bbc.com/cymrufyw",
                      "https://www.bbc.com/news/politics/uk_leaves_the_eu",
                      "https://www.bbc.com/news/wales",
                      "https://www.bbc.com/news/scotland",
                      "https://www.bbc.com/news/business/your_money",
                      "https://www.bbc.com/news/education-46131593",
                      "https://www.bbc.com/news/northern_ireland",
                      "https://www.bbc.com/news/world/asia/china",
                      "https://www.bbc.com/news/have_your_say",
                      "https://www.bbc.com/news/england",
                      "https://www.bbc.com/news/world/us_and_canada",
                      "https://www.bbc.com/news/world/europe",
                      "https://www.bbc.com/news/newsbeat",
                      "https://www.bbc.com/news/world/africa",
                      "https://www.bbc.com/news/world/australia",
                      "https://www.bbc.com/news/world/middle_east",
                      "https://www.bbc.com/news/world/asia",
                      "https://www.bbc.com/news/world_radio_and_tv",
                      "https://www.bbc.com/news/reality_check",
                      "https://www.bbc.com/news/the_reporters",
                      "https://www.bbc.com/news/world/latin_america",
                      "https://www.bbc.com/news/stories",
                      "https://www.bbc.com/news/in_pictures",
                      "https://www.bbc.com/news/technology",
                      "https://www.bbc.com/news/av/10462520",
                      "https://www.bbc.com/news/health",
                      "https://www.bbc.com/news/business",
                      "https://www.bbc.com/news/science_and_environment",
                      "https://www.bbc.com/news/coronavirus",
                      "https://www.bbc.com/news/uk",
                      "https://www.bbc.com/news/entertainment_and_arts",
                      ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        url = "https://www.bbc.com"
        content = response.css('a.qa-heading-link.lx-stream-post__header-link')

        for article_link in content.xpath('.//@href').extract():

            if 'https' not in article_link:

                item['article_url'] = url+article_link

                yield(scrapy.Request(url=url+article_link, callback=self.parse_articles))

    def parse_articles(self, response):

        stuff = {}

        text = ' '.join(response.css('p ::text').extract())
        url = response.request.url

        # nltk.download('averaged_perceptron_tagger')
        tagged_text = ''.join([re.sub('[!@#$%&()*+,\\/:.;”“<=>?\"[\]^_—`{|}~\d…]', ' ', word) for word in text])
        tokenised_text = word_tokenize(tagged_text)

        # POS Tagging
        tagged_text = nltk.pos_tag(tokenised_text)
        # Remove closed tag categories
        closed_tag_categories = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO',
                                 'UH', 'WDT',
                                 'WP', 'WP$', 'WRB']

        Lemmatizer = nltk.stem.WordNetLemmatizer()
        # Transform words to lowercase lemmas, and remove closed tag categories
        tagged_text = [(Lemmatizer.lemmatize(word[0].lower()), word[1]) for word in tagged_text if
                       word[1] not in closed_tag_categories]

        # Create frequency distribution
        TF = nltk.FreqDist(word[0] for word in tagged_text)
        stuff[url] = TF
        # yeet to Articles.json
        yield stuff

import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'narutospider'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        # Make sure the selector finds the container
        containers = response.css('.smw-columnlist-container')
        if containers:
            for href in containers[0].css("a::attr(href)").extract():
                extracted_data = scrapy.Request(
                    url="https://naruto.fandom.com" + href,
                    callback=self.parse_jutsu
                )
                yield extracted_data

        # Follow pagination links if they exist
        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)

    def parse_jutsu(self, response):
        # Safely extract jutsu name
        jutsu_name = response.css("span.mw-page-title-main::text").extract_first(default='').strip()
        
        div_selector = response.css("div.mw-parser-output")
        if not div_selector:
            return
        
        div_html = div_selector.extract_first()
        
        soup = BeautifulSoup(div_html, 'html.parser').find('div')
        
        jutsu_type = ""
        
        # Check if aside exists before trying to parse it
        aside = soup.find('aside') if soup else None
        if aside:
            for cell in aside.find_all('div', {'class': 'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == "Classification":
                        jutsu_type = cell.find('div').text.strip()

            # Remove aside from the description
            aside.decompose()
        
        # Extract and clean jutsu description
        jutsu_description = soup.text.strip() if soup else ''
        jutsu_description = jutsu_description.split('Trivia')[0].strip()
        
        # Return the structured data
        yield {
            'jutsu_name': jutsu_name,
            'jutsu_type': jutsu_type,
            'jutsu_description': jutsu_description
        }

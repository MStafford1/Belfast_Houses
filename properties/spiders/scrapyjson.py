from pathlib import Path
import json
import scrapy


class PropertySpider(scrapy.Spider):
    name = "propertyjson"
    start_urls = [
            "https://www.propertypal.com/property-for-sale/belfast",
            "https://www.propertypal.com/property-for-sale/belfast/page-2",
        ]

    def parse(self, response):
        raw_json = json.loads(response.css('[id="__NEXT_DATA__"]::text').get())
        props = raw_json.get('props', {})
        page_props = props.get('pageProps', {})
        initial_state = page_props.get('initialState', {})
        properties = initial_state.get('properties', {})
        datanest = properties.get('data', {})
        results = datanest.get('results', {})
        
        for property in results:
            account = property.get('account', {})
            coordinates = property.get('coordinate', {})
            style = property.get('style', {})
            status = property.get('status', {})
            price = property.get('price', {})

            yield {
                'title': property.get('title'),
                'path': property.get('path'),
                'full_address': property.get('displayAddress'),
                'address_line_1': property.get('addressLine1'),
                'postcode': property.get('postcode'),
                'latitude': coordinates.get('latitude'),
                'longitude': coordinates.get('longitude'),
                'agent': account.get('organisation'),
                'development': property.get('development'),
                'type': property.get('property'),
                'property_class': property.get('propertyType'),
                'house_type': style.get('text'),
                'num_bedrooms': property.get('numBedrooms'),
                'num_bathrooms': property.get('numBathrooms'),
                'sale_status': status.get('text'),
                'price': price.get('price'),
                'epc': property.get('epc'),
                'listing_updated_dt': property.get('listingUpdatedTime'),
                'activation_time': property.get('activationTime')
                }
            
        next_page = datanest.get('nextUrl')
        print(next_page)
        try:
            full_url = "https://www.propertypal.com/" + next_page
            if full_url:
                yield response.follow(full_url, callback=self.parse)
        except:
            return









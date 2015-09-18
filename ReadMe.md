# Scrapy Spiderman #


A web interface that allows you to control your [Scrapy](http://scrapy.org/) spiders.
It allows you to start, stop and monitor your spiders' progress (similar to [scrapinghub](http://www.scrapinghub.com/)).

It uses Django/PostgreSQL for the backend and Celery to run the spiders in the background.

It'll automatically generate models from your spider's items. But you'll need to [modify your spiders](#modify-your-spiders).

## Usage ##
    
### Manual Method ###

1. Install the required Python packages:
   
   
    pip install -r requirements.txt

2. Install [RabbitMQ Server](https://www.rabbitmq.com/) and start it's service.
3. Install [Celery](http://www.celeryproject.org/) and start it's worker (See [supervisord.conf](scrapy-spiderman/supervisord.conf)
file for the full command).
4. Install PostgreSQL and create a `scrapypanel` database.
5. Start the django server


### Using [Vagrant](https://www.vagrantup.com/) ###

1. Install vagrant
2. cd into the project directory
3. do:
    
        vagrant up

Wait until the command is done. You'll have the web interface accessible at `http://localhost:8080`

### Update the Settings ###

There's currently one required setting: `SPIDER_DIRS`.
It should be a list of disk directories on your system. Each can contain one or more Scrapy projects (created with the 
`startproject` command.

Then your need to run:

    python manage.py collect_spiders

## Modify Your Spiders ##

To create django models (tables) that store your items, you'll need to add an attribute to your spider class:
`ITEM_CLASS`.

Like so:

    class MySpider(CrawlSpider):
        name = ...
        allowed_domains = ...
        
        ...
    
        ITEM_CLASS = MyScrapedItem

The `ITEM_CLASS` is the usual [Scrapy Item](http://doc.scrapy.org/en/latest/topics/items.html#scrapy.item.Item).

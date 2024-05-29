from scrapy import cmdline

name = 'espider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())

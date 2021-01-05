from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import config
import re
from urllib.parse import urlparse, urlunparse
from urlextract import URLExtract
import requests



def trim_utm(url):
    parsed_url = list(urlparse(url))
    parsed_url[4] = '&'.join(
        [x for x in parsed_url[4].split('&') if not re.match(r'utm_', x) 
                                            and not re.match(r'spm', x) 
                                            and not re.match(r'productIds', x)
                                            and not re.match(r'scm', x)
                                            and not re.match(r'scm_id', x)
                                            and not re.match(r'scm-url', x)
                                            and not re.match(r'pvid', x)
                                            and not re.match(r'gps-id', x)
                                            and not re.match(r'ad_pvid', x)
                                            and not re.match(r'go-pvid', x)
                                            and not re.match(r'algo-pvid', x)
                                            and not re.match(r'algo_pvid', x)
                                            and not re.match(r'algo_expid', x)
                                            and not re.match(r'btsid', x)
                                            and not re.match(r'ws_ab_test', x)
                                            and not re.match(r'sku_id', x)
                                            and not re.match(r'_nc_.*', x)
                                            and not re.match(r'_ga', x)])
    utmless_url = urlunparse(parsed_url)
    return utmless_url

def unshort_url(url):
    r = requests.head(url, allow_redirects=True)
    return r.url

def message(update: Update, context: CallbackContext) -> None:
    extractor = URLExtract()
    if extractor.has_urls(update.message.text):
        result_text = update.message.text
        for url in extractor.gen_urls(update.message.text):
            print(f"Url found: {url}")
            unshorten_url = unshort_url(url)
            print(f"Unshorten: {unshorten_url}")
            sanitized_url = trim_utm(unshorten_url)
            print(f"Sanitized: {sanitized_url}")
            if url != sanitized_url:
                result_text = result_text.replace(url, sanitized_url)
        if result_text != update.message.text:
            update.message.reply_text(result_text)



updater = Updater(config.BOT_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, message))
updater.start_polling()
updater.idle()
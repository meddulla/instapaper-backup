Instapaper Backup

Fetches the given rss url (your instapaper's rss) and for each article url saves the actual content to disk. Change settings.py with your own instapaper feed url and the path to save the html downloaded files to.
Can also parse the csv given by the Export option in the instapaper site and fetch the corresponding urls.
So even if the links go dead or the instapaper service itself dies you'll still have your saved articles.

Just set this up in cron (see the script and change paths accordingly).

Of course, it could also work for any rss and/or csv (that follows the same structure: URL, Title, Selection, Folder).


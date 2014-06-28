pinboardlinkspost
=================

A quick script to go through your saved links on Pinboard and turn them into a blog post in Markdown format


## Installing

  > pip install -r requirements.txt

## Using

  > newlinkspost.py

Type your username and password, then how many links you want to look at, and then follow the prompts for each link, and either add it to your new post or ignore it.
Either way, it is marked as seen in a file ./seen.txt, and you won't be asked about it on future runs.

If the saved link doesn't have enough information for you to decide whether to include it, the 'o' key will load it in a browser for you to look again.

If you want to edit the extended description to provide some commentary, or fix some tags, 'ee' or 'et' let you do that inline, and will save your changes back to pinboard.

## Ideas for improvement

There's a reason this section is bigger than the others :shrug:

* General code cleanup and making it more than a hacky script
** use getopt or something similar for options

* Use something less dumb for persisting seen links, to allow for extra state (e.g. a link that is seen but you want to save it for a later post)

* Avoid getting all the links by saving date of last access (via API) and sending that to the API

* Better editing UI? There's lots of room for ideas here

* Allow customization of output file path and other things

* Support for item and page templates

* Support other bookmarking services?

* Support importing new posts from Tumblr, etc?

* Make it work with octopress as well as nikola (*note*, contact Mike first if you want to do this, I have a very slightly rotted version that did this)
# pyct: Python + CrowdTangle

`pyct` is a Python wrapper to retrieve data from the [CrowdTangle API](https://github.com/CrowdTangle/API).

See [pyct-demo.ipynb](https://github.com/simonlindgren/pyct/blob/main/pyct-demo.ipynb) for a tutorial. If you are not already familiar with CrowdTangle, you may have to read the rest of this README.

## Background to CrowdTangle

CrowdTangle (CT) was created as a social monitoring tool and was initially mostly used by journalists and media people to monitor certain issues, brands or events. It is a “content discovery and social analytics tool”. CT was acquired by Facebook in 2016 -- and was then presented as being targeted also towards academics -- as a controlled way of getting access to research data from Facebook and Instagram. CT is a bit convoluted, and sometimes hard to get your head around as an academic researcher. Used in the right ways, however, it gives access to quite rich data in ways that have not been possible since before the Cambridge Analytica data scandal. Needless to say, with CT data as with any data, ethical issues must be actively engaged with.

## What data are we dealing with?

CT is not *all* of Facebook, or *all* of Instagram. Nor is it all of the public accounts and posts on these platforms. CT is a database. Some things are added automatically to the database, such as:

- Public pages and public groups with 100k+ likes/followers/members
- US public groups with 2000+ members
- Public Instagram accounts with 75k+ followers
- All ‘verified’ profiles

In addition to this, any individual user of CT can contribute to the database by adding in more content to be tracked. Any public page or group can be added, and once this is done CT will start tracking the group, as well as put all of its history (excluding any deleted posts) into the database. A page or group is added to CT if you add it to one of your Lists (see below). 

A major shortcoming of CrowdTangle is that it does not give access to comments, only to posts. This strongly affects the kind of research that can be done with it.

## Using CrowdTangle to collect data

In CT, you organise your research in *dashboards*. It is a good idea to start a new dashboard for each defined research task that you take on. I think of a dashboard as a data collection job. Dashboards can be created by logging in to [crowdtangle.com](https://crowdtangle.com) using a Facebook account.

Once on the new and empty dashboard, you can start adding in data through the menus on the left. Dashboards are platform specific, either for Facebook or Instagram.


For a Facebook data dashboard:

- Data is added either as ‘Lists’ or as ‘Saved Searches’. Lists can be of either Facebook Pages or Facebook Groups. The same goes for saved searches, where a single saved search targets either lists or groups. Note that CT does not do wildcard* searches.

For an Instagram data dashboard:

- Data is added either as ‘Lists’ or as ‘Saved Searches’. Lists are of Instagram accounts. Saved Searches return keyword matches across Instagram in the CT database.

## Collecting Facebook data for a project

1. Create a Facebook dashboard for the project.
2. Create a List of relevant Pages, and a list of relevant Groups for your project. To add a page or group that does not appear when searching for its name, you can paste its url into the search field for it to appear. If you already know of a large number of pages/groups that you want to add, CT has a batch upload function for csv files [see gear icon]. 
3. Create any relevant Facebook Saved Searches. Remember that these search in the CT database, not in Facebook as a whole.

## Collecting Instagram  data for a project

1. Create an Instagram dashboard for the project.
2. Create a List of relevant accounts.
3. Create any relevant Saved Searches.

## Web interface

Looking at CT lists and searches while logged into CT in the browser can be interesting for some exploration. This can be done for example by viewing the ‘Leaderboard’ for a list or saved search, or by playing around with the ‘Intelligence’ or ‘Live Displays’ tools [top menu bar].

The ‘Search’ tool [top menu bar] is very good for high-level overviews and explorations.

It is also possible to download csv files of data (10,000 lines maximum/each) via the CT website. But API is better for this (see below).

A powerful function which is website only, is the possibility to get historical data in batches of ~300,000 posts (rather than just 10k). Go to [gear icon] >> 'Historical Data'. Here, as with other downloads, the key to building larger datasets is to make several queries sliced by date.


## CrowdTangle API

With the searches and lists set up, we can leave the web interface behind and use the API to retrieve data.

See [pyct-demo.ipynb](https://github.com/simonlindgren/pyct/blob/main/pyct-demo.ipynb) for tutorial. 

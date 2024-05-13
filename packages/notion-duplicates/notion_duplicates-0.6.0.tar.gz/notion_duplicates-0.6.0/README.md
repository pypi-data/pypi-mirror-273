## Purpose

**Detect the duplicated pages in a Notion database and optionally delete the dupes**

### What's a duplicated page?
It's a page with the both same _title_ and _last_edited_time_ as another document.

### Motivation
I recently decided to move away from Evernote (after being a subsciber since 2008). 
My reason? They started to jack up their price to a level that wasn't justifiable to me.

The price of the yearly subscription went from $35 in 2022, to $50 in 2023 and for this year they want **$130!** 
`</RANT>`

After I imported many pages from Evernote, I ended up with 100s if not 1000s of duplicated pages.

This script solved the problem! 

## Install

```sh
pip install notion-duplicates
```

## Prerequisites

You first need to create an *integration* from Notion that will create a *token*:

- Go to https://www.notion.so/my-integrations
- Click on **[ + New Integration ]**
- Specify the name say: **notion_duplicates**
- Click on Show under *Internal Integration Secret* and copy the *secret* which looks like:

  - `secret_WhGbvv7jUxt88WXYZDlhxoiBtgtzGXBqPrVSA00aaBo`
- That's the value to use as NOTION_TOKEN

Next, you need to connect the **notion_duplicates** integration with your Notion database:

- Navigate to your Notion database such as: https://www.notion.so/a769a042d8f544ce860ba408d295ab28?v=8603013e8753451cb46496a62e6ac55f
- Click on the **. . .** at the top right of the page
- Select **Connect To** and select **notion_duplicates** from the list, and confirm

Finally, you need your **database_id** that can easily be extracted from your database URL:

It's the 32 characters from the / to the ?. See the example below where the database_id=a769a042d8f544ce860ba408d295ab28

```commandline
https://www.notion.so/a769a042d8f544ce860ba408d295ab28?v=8603013e8753451cb46496a62e6ac55f
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

## Usage

### Help (-h)

```commandline
notion_duplicates -h
usage: notion_duplicates [-h] [-m [MAX_PAGE_COUNT]] [-D] [-M [MAX_DELETE_PAGE_COUNT]] database_id

Detect duplicated pages in a Notion database and optionally delete them

positional arguments:
  database_id           Notion database on which to conduct the duplicate search. See README.md for more details

optional arguments:
  -h, --help            show this help message and exit
  -m [MAX_PAGE_COUNT], --max_page_count [MAX_PAGE_COUNT]
                        Maximum number of pages to scan for duplicated pages (default: None)
  -D, --delete          Do the actual deletion (set in_trash=True) (default: False)
  -M [MAX_DELETE_PAGE_COUNT], --max_delete_page_count [MAX_DELETE_PAGE_COUNT]
                        Maximum number of pages to delete (default: None)
```

### Example with no duplicate
```commandline
notion_duplicates a769a042d8f544ce860ba408d295ab28
Iterated over 3 pages in the database:a769a042d8f544ce860ba408d295ab28. Found 0 duplicated page(s) and deleted 0 page(s)
Elapased time:0.12 seconds
```

### Example showing duplicates only (no deletion)
```commandline
notion_duplicates 5ae487a972e345b09450c181150a7AAA
Scanned 100 in 0.61 secs or 164 pages/sec
Scanned 200 in 1.52 secs or 131 pages/sec
Scanned 300 in 2.22 secs or 135 pages/sec
Scanned 400 in 3.02 secs or 132 pages/sec
Scanned 500 in 3.63 secs or 138 pages/sec
This page is a dupe -> title:(1) Facebook | last_edited:2013-07-05T01:34:00.000Z | url:https://www.notion.so/1-Facebook-a7df306435694572be8460ac45b75950
This page is a dupe -> title:Patio Lounger RE 11.2in Nicollet : Target | last_edited:2013-07-04T23:09:00.000Z | url:https://www.notion.so/Patio-Lounger-RE-11-2in-Nicollet-Target-706e30effb4345b4b50ee0db3328ebbb
This page is a dupe -> title:ÄPPLARÖ Drop-leaf table - IKEA | last_edited:2013-07-04T23:03:00.000Z | url:https://www.notion.so/PPLAR-Drop-leaf-table-IKEA-9fe474b0f5424c499f3fe78aeb005deb
Reached max page count
Iterated over 521 pages in the database:5ae487a972e345b09450c181150a77b2. Found 3 duplicated page(s) and deleted 0 page(s)
Elapased time:4.52 seconds
```

### Example deleting duplicates (use -D)
```commandline
notion_duplicates -D 5ae487a972e345b09450c181150a7AAA
Scanned 100 in 0.61 secs or 164 pages/sec
Scanned 200 in 1.52 secs or 131 pages/sec
Scanned 300 in 2.22 secs or 135 pages/sec
Scanned 400 in 3.02 secs or 132 pages/sec
Scanned 500 in 3.63 secs or 138 pages/sec
DELETING dupe page -> title:(1) Facebook | last_edited:2013-07-05T01:34:00.000Z | url:https://www.notion.so/1-Facebook-a7df306435694572be8460ac45b75950
DELETING dupe page -> title:Patio Lounger RE 11.2in Nicollet : Target | last_edited:2013-07-04T23:09:00.000Z | url:https://www.notion.so/Patio-Lounger-RE-11-2in-Nicollet-Target-706e30effb4345b4b50ee0db3328ebbb
DELETING dupe page -> title:ÄPPLARÖ Drop-leaf table - IKEA | last_edited:2013-07-04T23:03:00.000Z | url:https://www.notion.so/PPLAR-Drop-leaf-table-IKEA-9fe474b0f5424c499f3fe78aeb005deb
Iterated over 521 pages in the database:5ae487a972e345b09450c181150a7AAA. Found 3 duplicated page(s) and deleted 3 page(s)
Elapased time:4.77 seconds
```




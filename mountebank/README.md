# mountebank

## Introduction

This directory contains EJS scripts to enabling Mountebank to mock different
server scenarios. The intent is to configure Mountebank so that "live" runs of
the "caia" application can be demonstrated.

Note that the files in this directory are distinct from the use of Mountebank
for the unit/integration tests in the "tests" subdirectory. The tests have
their own set of Mountebank-related files.

## Usage

Assuming that Mountebank is installed (see
[docs/DevelopmentSetup.md](../docs/DevelopmentSetup.md), run Mountebank from the
project root directory using the following command:

```
> npx mb --allowInjection --localOnly --configfile <EJS_FILE>
```

where <EJS_FILE> is the file containing the imposters to set up.

The ".env" file of the "caia" application should then be configured with the
URLs specified in the selected imposters configuration. 

## Imposters configuration (EJS Files)

### mountebank/circrequests_success.ejs

A successful "circrequests" session with one item.

* CIRCREQUESTS_SOURCE_URL: http://localhost:4545/circrequests/source
* CIRCREQUESTS_DEST_URL: http://localhost:6565/circrequests/dest

### mountebank/circrequests_denied_keys.ejs

A successful "circrequests" session with one denied item (barcode: 
"denied_item") and one allowed item (barcode: "allowed_item").

* CIRCREQUESTS_SOURCE_URL: http://localhost:4545/circrequests/source
* CIRCREQUESTS_DEST_URL: http://localhost:6565/circrequests/dest

### mountebank/items_success.ejs

A successful "items" session with two new items and two updated items.

* ITEMS_SOURCE_URL: http://localhost:4545/items/source
* ITEMS_DEST_NEW_URL: http://localhost:6565/items/dest/incoming
* ITEMS_DEST_UPDATES_URL: http://localhost:6565/items/dest/updates

### mountebank/items_success_multiple_iterations.ejs

A successful "items" session where a "nextitem" in the first response
triggers a second iteration of queries to the source URL:

* ITEMS_SOURCE_URL: http://localhost:4545/items/source
* ITEMS_DEST_NEW_URL: http://localhost:6565/items/dest/incoming
* ITEMS_DEST_UPDATES_URL: http://localhost:6565/items/dest/updates

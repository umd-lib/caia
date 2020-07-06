# storage/items 

This directory contains intermediate results from running items jobs,
including:

* items_last_success.txt - Contains the filepath to the source response of
    the last successful job.
* the response body from the source URL
* the request bodies that were sent to the destination URL for the new and
  update requests
* the response bodies that wre received from the destination URL for the
  new and update requests

None of these files is required. If the "items_last_success.txt" file
does not exist, if will be created pointing to the
"etc/items_FIRST.json" file.

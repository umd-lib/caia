# storage/circrequests 

This directory contains intermediate results from running circrequest jobs,
including:

* circrequests_last_success.txt - Contains the filepath to the source response of
    the last successful job.
* the response body from the source URL
* the "diff result" between the last successful job and the current job
* the request body that was sent to the destination URL
* the response body that was received for the destination URL

None of these files is required. If the "circrequests_last_success.txt" file
does not exist, if will be created pointing to the
"storage/etc/circrequests_FIRST.json" file.


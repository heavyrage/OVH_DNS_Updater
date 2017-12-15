# OVH_DNS_Updater

I needed a solution to update my OVH DNS entry for accessing my NAS from Internet, because my ISP provides a dynamic IP address...

## Installation
Simply copy the content to a folder.
Edit the updateDNS.py and insert your OVH-Manager credentials, and your domain.
You can also edit the location of the log file.

At first time, run the build_oldIP.py to store your current IP within a file.
Then you can run the updateDNS.py.

It is recommended to create a cron to execute the script every 5 minutes, so every IP renewal will be registered automatically.

# HamAlert_On_Desktop
Python script to display HamAlert notifications on desktop using ntfy.sh

# Dependencies
- Python 3.x
- Account on HamAlert with triggers set up
- Account / topic set up on https://ntfy.sh or a different ntfy.sh server (M0YNG runs a one for hams on the fediverse. Use it and drop him a few bucks!)

Python libraries:
 - requests
 - json
 - rich
 - urllib.parse

# Prerequisites

In HamAlert, under the "Destinations" tab, enter the ntfy.sh server and topic URL you are using as the destination for a POST request, and be sure to have that topic and URL already set up in ntfy.sh.
Under "Triggers", be sure to configure each trigger you want showing up in this script to have "URL" as a destination in addition to the app.

This python script opens a stream to the JSON endpoint of the aforementioned ntfy.sh topic, and displays HamAlert notifications you have set according to your triggers into your terminal.

The script has a number of parameters, including colors, a list of callsigns that you want hilighted in the notificaitons (presuming they will appear as per your triggers), SOTA summit associations you want highlighted (again: presuming they are in your triggers).  See comments in the script for explanations.

This script is primarily set up to display how I use HamAlert. Non POTA and SOTA notifications are lumped together, color-wise, and there is no differentiation of digital modes.  Feel free to fork, download, and alter as you see fit!

This script also could be tidied up using functions at some point.  This is a quick and dirty verison.

# Things to know:

- The U.S. state displayed is the state that the callsign is registered in for SOTA, and possibly RBN, DXCC, and PSKReporter spots.  It's the state the park is in for POTA.  See the HamAlert parameters explanation on the hamalert.org website, under the Destinations tab.
- I have not yet tested this with non U.S. callsigns or non U.S. summits and parks.  Come to think of it, I probably should.  Yikes.

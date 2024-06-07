# Script to (1) consume a JSON feed from nfty.sh
# (2) Parse the URL hash from HamAlert contained therein to something human readable
# (3) Print that out in a pretty way to the terminal
# As is, time listed is currently in UTC.  Will give option to convert to local time later.
# Script by KC1SRI - June 2024

# ---- Import all the libraries
import requests
import json
from rich import print as rprint
from urllib.parse import unquote, parse_qsl

# ---- Parameters

# Dump the list here, with callsigns separated by a comma and a space, so you can just copy and paste from the callsign field in your callsign trigger.
mastodon_callsigns = ""
local_sota = [""] # Python list of your local SOTA summit association that is also in HamAlert, to differentiate these in the alert from your other triggers, if you have a separate trigger just for certain summit associations.

# Colors for the rich library can be found at https://rich.readthedocs.io/en/stable/appendix/colors.html
# Note: If any of these are empty or don't match colors above, script will abort and throw errors
# Note: Your terminal, or the font you choose for your terminal, may not support italics or bold. It's your terminal- choose the colors you see fit!

time_color = "grey42" # For now, time is listed in UTC
callsign_color = "sky_blue1"
frequency_color = "orange1"
mode_color = "dark_orange"
sota_color = "turquoise2"
summit_ref_color = "deep_sky_blue1"
summit_name_color = "dodger_blue1"
pota_color = "spring_green3"
park_ref_color = "green4"
park_name_color = "green3"
rbn_psk_dx_color = "medium_orchid3"
state_color = "grey42"
mastodon_color = "italic sky_blue1"
local_sota_color = "italic turquoise2"
separator_color = "grey35"
separator_char = " - "
comment_color = "grey27"

# ---- Parse the list of Mastodon Callsigns into Python list
mastodon_list = mastodon_callsigns.split(", ")
# print(mastodon_list)

# ---- Spin up the stream from https://ntfy.sh server you're using
resp = requests.get("", stream=True) #URL of the JSON endpoint for the ntfy server you are using  It's the URL of your subscribed topic with /json appended to the end

# ---- Process the stream from nfty and print out to your terminal
for line in resp.iter_lines():
    if line:
        data = json.loads(line) # parses the JSON from nfty into a Python dictionary
        # rprint(data)
        if data['event'] == "keepalive":
            pass # silences the keepalive messages from nfty
        elif data['event'] == "open":
            rprint("\n[italic dark_orange]Opening HamAlert Feed[/italic dark_orange]\n[orange3]---------------------[orange3]\n") # Just a nice startup message when feed opens up
        elif data['event'] == "message": # If it's a nfty message (usually from HamAlert) begin to parse it.  I should probably make this a function.
            msg = unquote(data['message']) # Since the message from HamAlert is a URL hash with quoted/escape ASCII characters, we have to convert that back to readable text
            parsed_msg = dict(parse_qsl(msg)) # Since HamAlert sends the data in the form of a URL query, we can parse that into a Python dictionary, but, we have to parse it into a list first or else the dictionary values will all be single item lists which are a PITA to work with for something like this
            # rprint(parsed_msg)

            time = "[" + time_color + "]" + parsed_msg['time'] + "[/" + time_color + "]"
            callsign = "[" + callsign_color + "]" + parsed_msg['callsign'] + "[/" + callsign_color + "]"
            for i in mastodon_list:
                if i == parsed_msg['callsign']:
                    callsign = "[" + mastodon_color + "]" + parsed_msg['callsign'] + "[/" + mastodon_color + "]"
            frequency = "[" + frequency_color + "]" + parsed_msg['frequency'] + "[/" + frequency_color + "]"
            mode = "[" + mode_color + "]" + parsed_msg['modeDetail'] + "[/" + mode_color + "]"
            separator = "[" + separator_color + "]" + separator_char + "[/" + separator_color + "]"

            if "sotawatch" in parsed_msg['source']:
                source = "[" + sota_color + "]" + "SOTA" + "[/" + sota_color + "]"
                if "state[0]" in parsed_msg.keys():
                    state = "[" + state_color + "]" + parsed_msg['state[0]'] + "[/" + state_color + "]"
                elif "state" in parsed_msg.keys():
                    state = "[" + state_color + "]" + parsed_msg['state'] + "[/" + state_color + "]"
                for i in local_sota:
                    if i in parsed_msg['summitRef']:
                        source = "[" + local_sota_color + "]" + "SOTA" + "[/" + local_sota_color + "]"
                    else:
                        pass
                summit_ref = "[" + summit_ref_color + "]" + parsed_msg['summitRef'] + "[/" + summit_ref_color + "]"
                summit_name = "[" + sota_color + "]" + parsed_msg['summitName'] + "[/" + sota_color + "]"
                if "comment" in parsed_msg.keys():
                    comment = "[" + comment_color + "]" + parsed_msg['comment'] + "[/" + comment_color + "]"
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + separator + summit_name + " " + summit_ref + " " + state + separator + comment)
                else:
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + separator + summit_name + " " + summit_ref + " " + state)

            elif parsed_msg['source'] == "pota":
                source = "[" + pota_color + "]" + "pota" + "[/" + pota_color + "]"
                park_ref = "[" + park_ref_color + "]" + parsed_msg['wwffRef'] + "[/" + park_ref_color + "]"
                park_name = "[" + park_name_color + "]" + parsed_msg['wwffName'] + "[/" + park_name_color + "]"
                if "state[0]" in parsed_msg.keys():
                    state = "[" + state_color + "]" + parsed_msg['state[0]'] + "[/" + state_color + "]"
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + separator + park_name + " " + park_ref + " " + state)
                elif "state" in parsed_msg.keys():
                    state = "[" + state_color + "]" + parsed_msg['state'] + "[/" + state_color + "]"
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + separator + park_name + " " + park_ref + " " + state)
                else:
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + separator + park_name + " " + park_ref)

            else:
                source = "[" + rbn_psk_dx_color + "]" + parsed_msg['source'] + "[/" + rbn_psk_dx_color + "]"
                state = "[" + state_color + "]" + parsed_msg['state'] + "[/" + state_color + "]"
                if "comment" in parsed_msg.keys():
                    comment = "[" + comment_color + "]" + parsed_msg['comment'] + "[/" + comment_color + "]"
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source  + " " + state + " " + comment)
                else:
                    rprint(time + separator + callsign + separator + frequency + " " + mode + separator + source + " " + state)
# FGF-Bot
A Discord WebHook bot that finds free games on IsThereAnyDeal.com using it's API and posts it directly to your discord server in a particular channel <br/>
## Instructions:
Make sure you have Python 3 installed, and download the code to your machine. <br/>

Install the needed libraries: `pip install Discord-Webhooks`<br/>

Create an "app" to get an API Key from [IsThereAnyDeal](https://isthereanydeal.com/apps/).<br/>

[Get a Discord webhook set up on your server](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) and edit `settings.json` with your information. <br/>

### Recommended:
You can also optionally use Task Scheduler in Windows to run this script only once a day. <br/>

#### PLEASE NOTE
The deafult version excludes itch.io games, since they are many - and often bad games that overshadow more polished Steam games. Edit `settings.json` to get rid of this restriction.

# unofficial-valorant-api (v.0.0.1)
:warning: This is *very* much a work in progress. Use at your discretion.

Unofficial Python SDK for the Unofficial Valorant API from HenrikDev (https://docs.henrikdev.xyz/valorant.html).

Pending distribution on PYPI.

To get in touch with Henrik, the original API Author, you can find the community Discord here:

<a href="https://discord.gg/X3GaVkX2YN" target="_blank"><img src="https://discordapp.com/api/guilds/704231681309278228/widget.png?style=banner2"/></a>

# Before using this API
Please make sure that the User has giving his consent to using his data. Analytic services where the user haven't giving his consent are not supportet and will be banned if found out

# Authentication and Rate Limits
All rate limits are the same for every endpoint, so in general you have **250 Requests every 2.5 Minutes**. Your rate limit is based on your IP so you don't need an API Key for authentication.
If you exceed rate limit you will get following JSON with 429 Status Code:
```json
{
    "status": 429,
    "message": "You reached your Rate Limit, please try again later"
}
```
**Important:**
The API will move in the future to a key based system, no application and therefore no waittime is required. When this change will go live is unknown yet, it's expected to happen in summer 2022. This change will happen because of large botting attacks which impacts all other developers.

# Status 403 - Forbidden
If you receive this status code, please ping my on the support discord or contact me over my mail or discord that are linked on the bottom of this page.

# Status
See the current status of the API here: https://status.henrikdev.xyz/

# Documentation
The documentation for the API is available under https://docs.henrikdev.xyz/valorant.html

# Legal
This API isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

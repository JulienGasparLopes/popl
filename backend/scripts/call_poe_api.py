import os

import requests
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    poe_sess_id = os.getenv("POESESSID")
    account_name = os.getenv("POE_ACCOUNT_NAME")  # Should be encoded to utf-8
    league = os.getenv("POE_LEAGUE")

    realm = "pc"
    tabs = "0"
    tab_index = "0"

    cookies = {
        "POESESSID": poe_sess_id,
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "priority": "u=1, i",
        # "referer": "https://www.pathofexile.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS) AppleWebKit (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    guild_id = 64913
    url = f"https://www.pathofexile.com/api/guild/{guild_id}/stash/history"
    # url = f"https://www.pathofexile.com/character-window/get-guild-stash-items?accountName={account_name}&realm={realm}&league={league}&tabs={tabs}&tabIndex={tab_index}"

    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    print(response.json())


if __name__ == "__main__":
    main()

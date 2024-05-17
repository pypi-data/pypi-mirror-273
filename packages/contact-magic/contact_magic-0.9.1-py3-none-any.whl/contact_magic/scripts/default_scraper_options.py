import pandas as pd

fallback_description = """
Replaces a text pattern Ex:'P.S {first_name}
what did you think?' with data from the contact. In this example, {first_name}
would be swapped with the column value of 'first_name' in your contact data.
"""

historic_data_description = """
Doesn't perform any scrape and uses
the current contact data and any scraped data
to generate a sentence using Copyfactory.
"""

default_scraper_options = pd.DataFrame(
    data=[
        {
            "Workflow": "FALLBACK",
            "Notes": fallback_description,
        },
        {
            "Workflow": "USE_HISTORIC_DATA",
            "Notes": historic_data_description,
        },
    ]
)

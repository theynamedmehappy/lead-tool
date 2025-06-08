import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API key from env
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

# Simple fallback patterns if no contact found
DEFAULT_PATTERNS = [
    "info@{}",
    "contact@{}",
    "hello@{}",
    "support@{}",
    "sales@{}"
]

def enrich_leads(df, max_leads_to_enrich=10):
    emails = []
    linkedin_urls = []

    for i, website in enumerate(df['Website']):  # Adjust column name if needed
        if i >= max_leads_to_enrich:
            emails.append("")
            linkedin_urls.append("")
            continue

        if website:
            try:
                domain = website.replace("https://", "").replace("http://", "").split("/")[0]

                # Apollo Contacts API — search for key person
                url = "https://api.apollo.io/v1/mixed_people/search"

                headers = {
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json"
                }

                payload = {
                    "api_key": APOLLO_API_KEY,
                    "q_organization_domains": [domain],
                    "person_titles": [
                        "Founder", "CEO", "Owner", "Managing Director",
                        "CMO", "Marketing Director", "President"
                    ],
                    "page": 1,
                    "per_page": 1
                }

                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('people'):
                        person = data['people'][0]
                        email = person.get('email', "")
                        linkedin = person.get('linkedin_url', "")
                        print(f"[{domain}] Found: {email}, {linkedin}")

                        emails.append(email if email else "")
                        linkedin_urls.append(linkedin if linkedin else "")
                    else:
                        # No person found → fallback
                        fallback_email = DEFAULT_PATTERNS[0].format(domain)
                        print(f"[{domain}] No person found — fallback email: {fallback_email}")
                        emails.append(fallback_email)
                        linkedin_urls.append("")

                else:
                    print(f"[{domain}] API Error {response.status_code}: {response.text}")
                    fallback_email = DEFAULT_PATTERNS[0].format(domain)
                    emails.append(fallback_email)
                    linkedin_urls.append("")

                # Respect API rate limits (very important!)
                time.sleep(1)

            except Exception as e:
                print(f"[{domain}] Error: {e}")
                fallback_email = DEFAULT_PATTERNS[0].format(domain)
                emails.append(fallback_email)
                linkedin_urls.append("")
        else:
            emails.append("")
            linkedin_urls.append("")

    # Add to DataFrame
    df['Email'] = emails
    df['LinkedIn'] = linkedin_urls

    return df

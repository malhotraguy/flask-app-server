import sys
from datetime import datetime

import pandas as pd

from brands_setup_tools.linkedin_id_and_posts_extractor.constants import (
    COLORSTART,
    COLOREND,
    AFFILIATED_COMPANIES_RESULTS,
    ENTITY_URN,
    UNIVERSAL_NAME,
    COMPANY_PAGE_URL,
    HEADQUARTER,
    URL,
    CITY,
    EXIT,
)
from brands_setup_tools.linkedin_id_and_posts_extractor.linkedin_tool_helpers import (
    get_company_name,
    get_linkedin_object,
)


def get_company_info(company_detail):
    company_urn = company_detail.get(UNIVERSAL_NAME)
    if ENTITY_URN not in company_detail:
        raise Exception(f"There is no entityUrn present for {company_urn}")
    urn_id = company_detail[ENTITY_URN].split(":")[-1]
    linkedin_url = company_detail.get(URL)
    headquarter = company_detail.get(HEADQUARTER, {}).get(CITY)
    company_url = company_detail.get(COMPANY_PAGE_URL)
    print(f"Universal Name= {company_urn}")
    print(f"URN ID= {urn_id}")
    print(f"Linkedin url= {linkedin_url}")
    print(f"Company Page Url= {company_url}")
    print(f"Headquarter= {headquarter}")
    company_info = {
        "Universal Name": company_urn,
        "URN ID": urn_id,
        "Linkedin Url": linkedin_url,
        "Company Page Url": company_url,
        "Headquarter": headquarter,
    }
    return company_info


def get_linkedin_id(company_name, linkedin_object):
    if company_name == EXIT:
        sys.exit("Quiting the Tool!!")

    try:
        company = linkedin_object.get_company(company_name)

    except KeyError:
        print(f"There is no Company with this name :{company_name}")
        print("=" * 160)
        return True
    df_table = pd.DataFrame()
    if company.get(AFFILIATED_COMPANIES_RESULTS):
        for item in company[AFFILIATED_COMPANIES_RESULTS]:
            print("=" * 60)
            print("Related Companies:-")
            company_item = company[AFFILIATED_COMPANIES_RESULTS].get(item, {})
            company_info = get_company_info(company_detail=company_item)
            df_table = df_table.append(company_info, ignore_index=True)
    print("=" * 160)
    print(COLORSTART)
    print("Original Result:-")
    original_company_info = get_company_info(company_detail=company)
    df_table = df_table.append(original_company_info, ignore_index=True)
    print(COLOREND)
    return df_table


def linkedin_setup():
    start_time = datetime.now()
    linkedin_object = get_linkedin_object()
    user_input = input("Enter the name of company or type 'exit' to exit: ").strip()
    company_universal_name = get_company_name(user_input)
    get_linkedin_id(company_universal_name, linkedin_object=linkedin_object)
    print(f"Total Time={datetime.now() - start_time}")
    print("=" * 160)
    return linkedin_setup()


if __name__ == "__main__":
    # execute only if run as a script
    linkedin_setup()

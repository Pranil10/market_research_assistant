

def build_user_prompt(user_input: str, mode: str) -> str:
    if mode == "Company Profile":
        return (
        f"Create a detailed company profile for {user_input} primarily using the company's official website. "
        f"The profile should include the following sections:\n\n"
        f"1. **Company Overview** - Brief intro, headquarters, founding year, core mission.\n"
        f"2. **Business Overview** - Key business segments, industries served, markets operated in.\n"
        f"3. **Financial Information** - Revenue, growth rate, or any financial data available on the website.\n"
        f"4. **Product Landscape** - Major products, services, or solutions offered.\n"
        f"5. **SWOT Analysis** - Based only on website information (no assumptions).\n"
        f"6. **Recent Developments** - Any news, events, or updates published on the website.\n"
        f"7. **Sources of the Data** - Include direct links or page references from the company website where each piece of information was found.\n\n"
        f"If a section cannot be completed based on official site content, clearly mention that."
    )

    else:
        return user_input

# linkedin-user-scrape

`linkedin-user-scrape` is a Python package for scraping user profile data from LinkedIn.

## Installation

You can install `linkedin-user-scrape` via pip:

```bash
pip install linkedin-user-scrape
```

## Example Usage
```bash
from linkedin_user_scrape import *
import json

email = "<your_email>"
password = "<your_password>"
cookie = "<your_cookie>"

userId = "<linkedin_user_id>"

user_details = get_user_profile_data(userId, cookie, email, password)

print(json.dumps(user_details, indent=4))
```


### How to Obtain the LinkedIn Cookie (li_at)
To use the `get_user_profile_data` function, you need to provide a LinkedIn cookie (li_at). You can obtain this cookie by following these steps:

1. Open LinkedIn in your web browser and log in.
2. Right-click on the page and select "Inspect" (or press Ctrl + Shift + I).
3. Go to the "Application" tab (in Chrome) or "Storage" tab (in Firefox).
4. Expand the "Cookies" dropdown and select the LinkedIn URL.
5. Locate the li_at cookie and copy its value.

## Response Format
The `get_user_profile_data` function returns a dictionary with the following structure:

```bash
{
    "Basic Details": basic_details,
    "Work Experience Details": work_experience_details,
    "Education Details": education_details,
    "Project Details": projects_details,
    "Recommendations": recommendations
}
```

- `basic_details`: Contains basic information about the LinkedIn user. (Name, Title, Summary)
- `work_experience_details`: Contains details of the user's work experience (Title, Company, Duration).
- `education_details`: Contains details of the user's education (Institure, Course, Duration, Summary).
- `projects_details`: Contains details of the user's projects.
- `recommendations`: Contains recommendations received by the user.
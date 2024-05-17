import re
from .utils import *
from bs4 import BeautifulSoup

def get_user_basic_details(driver, user_id, cookie, email, password):
    """
    Retrieves basic user details from a LinkedIn profile using the provided WebDriver.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        user_id (str): The user's LinkedIn ID.
        cookie (str) : li_at linkedin cookie
        email (str) : Email address for linkedin login
        password (str) : Password for linkedin login


    Returns:
        dict: A dictionary containing the user's basic details (name, title, summary, location).
    """

    if not driver:
        driver = get_webdriver(cookie, email, password)

    url = f"https://www.linkedin.com/in/{user_id}"
    src = get_driver_data(driver, url)
    soup = BeautifulSoup(src, 'lxml')

    details = {}
    selectors = {
        "name": 'h1',
        "title": 'div',
        "summary": 'div',
        "location": 'span'
    }
    classes = {
        "name": {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'},
        "title": {'class': 'text-body-medium break-words'},
        "summary": {'class': 'display-flex ph5 pv3'},
        "location": {'class': 'text-body-small inline t-black--light break-words'}
    }

    for field, selector in selectors.items():
        try:
            element = soup.find(selector, attrs=classes.get(field))
            details[field] = element.text.strip() if element else ""
        except Exception as e:
            details[field] = ""

    return details

def get_work_experience_detais(driver, userId, cookie, email, password):
    """
    Retrieves work experience details from a LinkedIn profile using the provided WebDriver.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        user_id (str): The user's LinkedIn ID.

    Returns:
        list: A list of dictionaries, each containing work experience details (title, company, duration, summary).
    """

    if(not driver):
        driver = get_webdriver(cookie, email, password)
    
    url = f"https://www.linkedin.com/in/{userId}/details/experience"
    src = get_driver_data(driver, url)
    
    soup = BeautifulSoup(src, 'lxml')
    
    soup = BeautifulSoup(src, 'html.parser')
    container_div = soup.find('div', class_='pvs-list__container')
    companyCache = ""

    workExperience = []

    # Check if the 'div' element is found
    if container_div:
        
        list_items = container_div.find_all('div', class_='display-flex flex-column full-width align-self-center')
        cleaned_list = []
        # Loop through each 'li' element
        for item in list_items:
            title = ""
            duration = ""
            company = ""
            try:
                job_details = item.find('div', {'class': 'display-flex flex-row justify-space-between'})
                
                title = job_details.find('div', {'class' : 'display-flex align-items-center mr1 t-bold'}).text.strip()
                company = job_details.find('span', {'class' : 't-14 t-normal'}).text.strip().split(' · ')[0]
                duration = job_details.find('span', {'class' : 't-14 t-normal t-black--light'}).text.strip().split(' · ')[0]
            except Exception as e:
                try:
                    title = job_details.find('div', {'class' : 'display-flex align-items-center mr1 hoverable-link-text t-bold'}).text.strip()
                    duration = job_details.find('span', {'class' : 't-14 t-normal t-black--light'}).text.strip().split(' · ')[0]
                    company = ""
                except Exception as e2:
                    print(e2)
            pattern = r"\b[A-Z][a-z]{2} \d{4}\b"  # Matches "MMM YYYY" format
            match = re.search(pattern, duration)
        
            title = split_at_caps(title)
            titleUnique = ""
            for i in title:
                if i not in titleUnique:
                    titleUnique = titleUnique +" " + i
            if company:
                company = split_at_caps(company)
                companyUnique = ""
                for i in company:
                    if i not in companyUnique:
                        companyUnique = companyUnique +" " + i
            else:
                companyUnique = companyCache

            try:
                job_summary = item.find('div', {'class': 'pvs-entity__sub-components'}).text.strip()
            except Exception as e:
                job_summary = ""

            if(bool(match)):
                workExperience.append(
                    {
                        "Title" : titleUnique,
                        "Company" : companyUnique,
                        "Duration" : duration,
                        "Summary" : job_summary
                    }
                )
            else:
                companyCache = titleUnique

    return workExperience

def get_education_details(driver, userId, cookie, email, password):
    """
    Retrieves education details from a LinkedIn profile using the provided WebDriver (if credentials provided) or potentially cached data (if cookie provided).

    Args:
        driver (Optional[WebDriver]): An instance of the WebDriver (used if no cookie provided). Defaults to None.
        user_id (str): The user's LinkedIn ID.
        cookie (Optional[str]): A valid LinkedIn session cookie for the target user (avoids login if provided). Defaults to None.
        email (Optional[str]): The user's email address (required for login if no cookie provided). Defaults to None.
        password (Optional[str]): The user's password (required for login if no cookie provided). Defaults to None.

    Returns:
        List[Dict]: A list of dictionaries, each containing education details (institute, course, duration, summary).
    """
    education = []
    if(not driver):
        driver = get_webdriver(cookie, email, password)
    
    url = f"https://www.linkedin.com/in/{userId}/details/education"
    src = get_driver_data(driver, url)
    
    soup = BeautifulSoup(src, 'html.parser')
    container_div = soup.find('div', class_='pvs-list__container')

    if container_div:
  
        list_items = container_div.find_all('div', class_='display-flex flex-column full-width align-self-center')
        for item in list_items:

            try: 
                edu_details = item.find('div', {'class': 'display-flex flex-row justify-space-between'})
                
                try:
                    institute = edu_details.find('div', {'class' : 'display-flex align-items-center mr1 hoverable-link-text t-bold'})
                    instituteDetails = institute.find('span', {'class' : 'visually-hidden'}).text.strip()
                except:
                    instituteDetails = ""

                try:
                    course = edu_details.find('span', {'class' : 't-14 t-normal'})
                    courseDetails = course.find('span', {'class' : 'visually-hidden'}).text.strip()
                except:
                    courseDetails = ""

                try:
                    duration = edu_details.find('span', {'class' : 'pvs-entity__caption-wrapper'}).text.strip()
                except:
                    duration = ""
            except:
                instituteDetails = ""
                courseDetails = ""
                duration = ""

            try:            
                edu_summary = item.find('div', {'class': 'pvs-entity__sub-components'})
                summaryDetails = edu_summary.find_all('span', {'class' : 'visually-hidden'})
            except:
                summaryDetails = ""

            summaryDetailsData = ""
            for data in summaryDetails:
                summaryDetailsData = summaryDetailsData + " " + data.text.strip()
            
            education.append(
                {
                    "Institute" : instituteDetails,
                    "Course" : courseDetails,
                    "Duration" : duration,
                    "Summary" : summaryDetailsData
                }
            )
    return education

def get_project_details(driver, userId, cookie, email, password):
    projects = []
    return projects

def get_recommendations(driver, userId, cookie, email, password):
    recommendations = []

    return recommendations

def get_user_profile_data(userId, cookie, email, password):
    """
    Retrieves user profile data from LinkedIn using a WebDriver (if credentials provided) or a cached version (if cookie provided).

    Args:
        user_id (str): The user's LinkedIn ID.
        cookie (str, optional): A valid LinkedIn session cookie for the target user (avoids login if provided). Defaults to None.
        email (str, optional): The user's email address (required for login if no cookie provided). Defaults to None.
        password (str, optional): The user's password (required for login if no cookie provided). Defaults to None.

    Returns:
        dict: A dictionary containing user profile data with sections for basic details, work experience, education, projects, and recommendations.
    """

    driver = get_webdriver(cookie, email, password)

    basic_details = get_user_basic_details(driver, userId, cookie, email, password)
    work_experience_details = get_work_experience_detais(driver, userId, cookie, email, password)
    education_details = get_education_details(driver, userId, cookie, email, password)
    projects_details = get_project_details(driver, userId, cookie, email, password)
    recommendations = get_recommendations(driver, userId, cookie, email, password)

    if driver:
        driver.quit()

    return {
        "Basic Details" : basic_details,
        "Work Experience Details" : work_experience_details,
        "Education Details" : education_details,
        "Project Details" : projects_details,
        "Recommendations" : recommendations
    }



from bs4 import BeautifulSoup
from .utils import *

def getUserBasicDetails(driver, userId):
    if(not driver):
        driver = getWebDriver(cookie, email, password)
    
    url = f"https://www.linkedin.com/in/{userId}"
    src = getDriverData(driver, url)
    
    soup = BeautifulSoup(src, 'lxml')

    try:
        name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()
    except Exception as e:
        name = ""
    
    try:
        title = soup.find('div', {'class': 'text-body-medium break-words'}).text.strip()
    except Exception as e:
        title = ""

    try:
        summary = soup.find('div', {'class':'display-flex ph5 pv3'}).text.strip()
    except Exception as e:
        summary = ""

    try:
        location = soup.find('span', {'class' : 'text-body-small inline t-black--light break-words'}).text.strip()
    except Exception as e:
        location = ""

    return {
        "Name" : name,
        "Title" : title,
        "Summary" : summary,
        "Location" : location
    }

def getWorkExperienceDetails(driver, userId):
    if(not driver):
        driver = getWebDriver(cookie, email, password)
    
    url = f"https://www.linkedin.com/in/{userId}/details/experience"
    src = getDriverData(driver, url)
    
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
                workExperience.append([
                    {
                        "Title" : titleUnique,
                        "Company" : companyUnique,
                        "Duration" : duration,
                        "Summary" : job_summary
                    }]
                )
            else:
                companyCache = titleUnique

    return workExperience

def getEducationDetails(driver, userId):
    education = []
    if(not driver):
        driver = getWebDriver(cookie, email, password)
    
    url = f"https://www.linkedin.com/in/{userId}/details/education"
    src = getDriverData(driver, url)
    
    soup = BeautifulSoup(src, 'lxml')
    
    soup = BeautifulSoup(src, 'html.parser')
    container_div = soup.find('div', class_='pvs-list__container')

    if container_div:
  
        list_items = container_div.find_all('div', class_='display-flex flex-column full-width align-self-center')
        cleaned_list = []
        # Loop through each 'li' element
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
            
            education.append([
                    {
                        "Institute" : instituteDetails,
                        "Course" : courseDetails,
                        "Duration" : duration,
                        "Summary" : summaryDetailsData
                    }]
                )
    return education

def getProjectDetails(driver, userId):
    projects = []
    return projects

def getRecommendations(driver, userId):
    recommendations = []

    return recommendations

def getUserProfileData(userId, cookie, email, password):
    driver = getWebDriver(cookie, email, password)

    # Get Basic Details
    basic_details = getUserBasicDetails(driver, userId)

    # Get Work Experience
    work_experience_details = getWorkExperienceDetails(driver, userId)

    # Get Education
    education_details = getEducationDetails(driver, userId)

    # Get Projects
    projects_details = getProjectDetails(driver, userId)

    # Get Recommendations
    recommendations = getRecommendations(driver, userId)


    return {
        "Basic Details" : basic_details,
        "Work Experience Details" : work_experience_details,
        "Education Details" : education_details,
        "Project Details" : projects_details,
        "Recommendations" : recommendations
    }



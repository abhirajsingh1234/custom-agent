def fetch_linkedin_details(username):
    

    import warnings
    warnings.filterwarnings('ignore')

    import os
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    from dotenv import load_dotenv
    load_dotenv()
    experience = []

    try:
        driver = webdriver.Chrome()
    except:
        print('error opening chrome')

    try:
        driver.get('https://www.linkedin.com/login/')
    except:
        print('error fetching login page')

    driver.title

    try:
        email = driver.find_element(By.ID, 'username')
        email.send_keys(os.environ['LINKEDIN_MAIL_ID'])
        password = driver.find_element(By.ID, 'password')
        password.send_keys(os.environ['LINKEDIN_PASSWORD'])
        password.submit()
    except:
        print('error logging in account')

    try:
    #     username = 'abhiraj-singh-rajpurohit-9647b427b/'
        url = f"https://www.linkedin.com/in/{username}"
        # url = f"https://www.linkedin.com/in/laxmimerit"
        driver.get(url)
        time.sleep(4)
    except:
        print('error reaching user account')

    profile_data ={}
    driver.title

    page_source = driver.page_source
    time.sleep(2)
    soup = BeautifulSoup(page_source, 'lxml')
    time.sleep(4)
    name = soup.find('h1','wtDWyXKFOUjAaodDuTSsnqoIZVMTs inline t-24 v-align-middle break-words')
    time.sleep(5)
    name = name.get_text().strip()
    profile_data['name']=name
    profile_data['url'] = url

    try:
        headline = soup.find('div','text-body-medium break-words')
        time.sleep(2)
        headline = headline.get_text().strip()
        profile_data['bio'] = headline
    except:
        profile_data['bio'] = None

    try:
        about = soup.find('div','SvoPApEanFEUJUXblOuMoAKMcXKnOpBlLCo full-width t-14 t-normal t-black display-flex align-items-center')
        about = about.get_text().strip()
        profile_data['about'] = about
    except:
        profile_data['about'] = None

    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'lxml')
    sections = soup.find_all('section',{'class':'artdeco-card pv-profile-card break-words mt2'})
    time.sleep(2)
    try:
        experience = None
        for sec in sections:
            if sec.find('div',{'id':'experience'}):
                experience = sec

        try:
            experience = experience.find_all('div',{'class':'nkuPpOPwqIooGCaBXuqZNVaxWBdnJXJXTXCyY EosmbAbFIoCeldPQMQSdhtwXadLngZfVcTW EVHJaKueawvwsbizlikIjleWFPNylcbZVtySzQnJY'})
        except:
            print('error at experience')
            return profile_data

        def get_exp(exp):

            exp_dict={}
            name = exp.find('div',{'class':'display-flex flex-wrap align-items-center full-height'})
            time.sleep(1)
            name = name.find('span',{'class':'visually-hidden'})
            time.sleep(2)
            name = name.get_text().strip()

            duration = exp.find('span',{'class':'t-14 t-normal'})
            time.sleep(1)
            duration = duration.find('span',{'class':'visually-hidden'})
            time.sleep(2)
            duration = duration.get_text().strip()

            exp_dict['company_name'] = name
            exp_dict['duration'] = duration

            designations = exp.find_all('div',{'class':'nkuPpOPwqIooGCaBXuqZNVaxWBdnJXJXTXCyY'})
            item_list=[]
            for position in designations:
                span = position.find_all('span',{'class':'visually-hidden'})
                time.sleep(1)
                item_dict ={}
                try:
                    item_dict['designation'] = span[0].get_text().strip()
                except:
                    item_dict['designation'] = None
                try:
                    item_dict['duration'] = span[1].get_text().strip()
                except:
                    item_dict['duration'] = None
                try:
                    item_dict['location'] = span[2].get_text().strip()
                except:
                    item_dict['location'] = None
                try:
                    item_dict['projects'] = span[3].get_text().strip()
                except:
                     item_dict['projects'] = None
                item_list.append(item_dict)
            exp_dict['designations']=item_list
            return exp_dict
    
        item_list=[]
        
        for exp in experience:
            item_list.append(get_exp(exp))
    except:
        print('error at fetching experience')
        return profile_data
    item_list
    try:
        for sec in sections:
            if sec.find('div',{'id':'education'}):
                educations = sec

        items = educations.find_all('div',{'class':'nkuPpOPwqIooGCaBXuqZNVaxWBdnJXJXTXCyY EosmbAbFIoCeldPQMQSdhtwXadLngZfVcTW EVHJaKueawvwsbizlikIjleWFPNylcbZVtySzQnJY'})


        def get_edu(item):
            item_dict = {}
            spans = item.find_all('span',{'class':'visually-hidden'})
            try:
                item_dict['college'] = spans[0].get_text().strip()
            except:
                    item_dict['college'] = None
            try:
                item_dict['degree'] = spans[1].get_text().strip()
            except:
                    item_dict['degree'] = None
            try:
                item_dict['duration'] = spans[2].get_text().strip()
            except:
                    item_dict['duration'] = None
            try:
                item_dict['project'] = spans[3].get_text().strip()
            except:
                    item_dict['project'] = None
            return item_dict

        item_list =[]
        for item in items:
            item_list.append(get_edu(item))

        profile_data['education'] = item_list
    except:
        print('error at fetching education')
        return profile_data

    return f"linkidin data for ||username:{username}||: {profile_data}"

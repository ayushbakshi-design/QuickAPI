import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://clients.quickcontractors.com',
    'Pragma': 'no-cache',
    'Referer': 'https://clients.quickcontractors.com/Login.html?v=2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'XCode' : '6189'
}

payload = {
    'username': 'triplegems',
    'password': 'Quick2021@',
    'auth': '',
    'status': '',
    'url': '',
}

# Starting a session with QC
requested_session = requests.session()

try:
    login_responce = requested_session.post(
        url="https://clients.quickcontractors.com/webapi/AccountsApi/LoginUser", data=payload)
    print('login Successful \n')
except Exception as e:
    print('login failed')

# Getting the Job Ids from the Calender request

try:
    # Variables
    contractor_calender_url = "https://clients.quickcontractors.com/Contractor/WebServices/ContractorWebService.asmx/Get_ContractorCalendar"
    contractor_calender_payload = "{contractorId: 6189, startdate: '7/13/2023' , enddate: '7/14/2023'}"
    print("Fetched Calender Data Successfully \n")

    # Fetching Data here
    get_calender_data = requested_session.post(
        url=contractor_calender_url, data=contractor_calender_payload, cookies=login_responce.cookies, headers=headers)

    print('Calender data : \n' + get_calender_data.text)
except Exception as e:
    print("failed to get calender")

# Sorting the Calender Data Gibrish to Proper list of Job ID's
locations = []
job_ids = []
all_jobs = []
today_jobs = []
start_point = 0
has_more_data = True

while has_more_data:
    result = get_calender_data.text.find('id', start_point)
    if result != -1:
        locations.append(result)
        start_point = locations[-1] + 1
    else:
        has_more_data = False

for i in locations:
    job_ids.append(get_calender_data.text[i+7:i+14])


print(f" {len(job_ids)} Job ID's are sorted now \n")
print(job_ids)

# Getting the data using the job id's one by one

cx_name = ''
cx_address = ''
cx_email = ''
cx_alternate_phone = ''
cx_mobile_phone = ''
cx_job_status = ''


print('Cx data one by one \n')

for index, job in enumerate(job_ids):
    cx_job_data = []

    job_data_url = f"https://clients.quickcontractors.com/Contractor/JobSearch/ManageJobs.aspx?XCode={job}"

    get_job_data = requested_session.get(
        job_data_url, cookies=login_responce.cookies, headers=headers, data={'XCode': job})
    job_soup = BeautifulSoup(get_job_data.content, 'html.parser')

    # Fetching Data from the Collected Soup
    try:
        cx_name = job_soup.find(
            id='ctl00_ContentPlaceHolder1_txt_CustomerInfo')['value']
    except Exception as e:
        print(f'{index + 1} Cx name didnt found \n')
        print(e)

    try:
        cx_address = job_soup.find(
            id="ctl00_ContentPlaceHolder1_txt_Address1")['value']
    except Exception as e :
        print(f'{index + 1} Cx address didnt found \n')
        print(e)

    try:
        cx_home_phone = job_soup.find(
            id="ctl00_ContentPlaceHolder1_txt_HomePhone")['value']
    # cx_alternate_phone = job_soup.find(id="ctl00_ContentPlaceHolder1_txt_AlternatePhone")['value']
    # cx_mobile_phone = job_soup.find(id="ctl00_ContentPlaceHolder1_txt_MobilePhone")['value']
    except Exception as e:
        print(f'{index + 1} Cx phone numbers didnt found \n')
        print(e)

    try:

        cx_email = job_soup.find(
            id="ctl00_ContentPlaceHolder1_txt_CustomerEmail")['value']
    except Exception as e:
        print(f'{index + 1} Cx Email didnt found  \n')
        print(e)

    try:
        cx_job_status = job_soup.find(id="ctl00_ContentPlaceHolder1_DD_JobStatus").select_one(
            'option[selected="selected"]').text
    except Exception as e:
        print(f'{index + 1} Cx job status didnt found \n')
        print(e)

    try:
        stillJobs = True
        job_number = 0

        #To delete the services of pervious job before adding new once 

        while stillJobs: 
            cx_first_job = job_soup.find(id=f"ctl00_ContentPlaceHolder1_rpt_LoadMultipleProducts_ctl0{job_number}_DD_PaymentType").select_one('option[selected="selected"]').text
            if cx_first_job: 
                cx_job_data.append(cx_first_job)
            else:
                stillJobs = False
            
            job_soup.find(id=f"ctl00_ContentPlaceHolder1_rpt_LoadMultipleProducts_ctl0{job_number}_DD_PaymentType").select_one('option[selected="selected"]').decompose()
            
            job_number += 1



    except Exception as e:
        print(f"{index + 1} Cx job data didn't found")
        print(e)


    all_jobs.append({
        'name' : cx_name,
        'address' : cx_address,
        'phone' : cx_home_phone,
        'email' : cx_email,
        'status' : cx_job_status,
        'jobs' : cx_job_data
    })

#Finding today jobs only 
for job in all_jobs: 
    if job['status'] == 'Booked': 
        today_jobs.append(job)


print(len(today_jobs) , "jobs are there for today \n")
for job in today_jobs: 
    print(job)


# adding data to the excel
with open('output.csv', 'w') as output: 
    today_qc_jobs = csv.writer(output)

    today_qc_jobs.writerow(['Name', 'Address', 'phone', 'Email', 'job Status', 'jobs'])

    for job in today_jobs: 
        today_qc_jobs.writerow([job['name'], job['address'], job['phone'], job['email'], job['status'] ,job['jobs']])

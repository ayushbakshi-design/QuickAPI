import requests
from bs4 import BeautifulSoup


# cookies = {
#     '_gid': 'GA1.2.150490177.1687920174',
#     '_ga_5HDYT3RPTX': 'GS1.1.1687920173.3.1.1687921558.0.0.0',
#     '_ga': 'GA1.1.1676204331.1687234333',
# }

# response_cookies = {
#     'ASP.NET_SessionId' : 'gxm0yq22babcpljgyyqnoejx',
#     'languageCookie' : 'en-US',
#     'createdcookie' : ''
# }

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': '_gid=GA1.2.150490177.1687920174; _ga_5HDYT3RPTX=GS1.1.1687920173.3.1.1687921558.0.0.0; _ga=GA1.1.1676204331.1687234333',
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
}

json_data = {
    'username': 'triplegems',
    'password': 'Quick2021@',
    'auth': '',
    'status': '',
    'url': '',
}

# response = requests.post(
#     'https://clients.quickcontractors.com/webapi/AccountsApi/LoginUser',
#     cookies=cookies,
#     headers=headers,
#     json=json_data,
# )


# homepage_url = "https://clients.quickcontractors.com/Contractor/AccountManagement/home.aspx"

# homepage_request = requests.get(homepage_url, cookies=response_cookies , headers=headers , timeout=5)

# soup = BeautifulSoup(homepage_request.content, 'html.parser')


# print(soup)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"username":"triplegems","password":"Quick2021@","auth":"","status":"","url":""}'
#response = requests.post(
#    'https://clients.quickcontractors.com/webapi/AccountsApi/LoginUser',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)



#Starting a session with QC
requested_session  = requests.session()
post = requested_session.post(url="https://clients.quickcontractors.com/webapi/AccountsApi/LoginUser", data=json_data)

#fetching the home page
try : 
    get_data = requested_session.get("https://clients.quickcontractors.com/Contractor/AccountManagement/home.aspx")
except : 
    print("session failed")


#Getting the Job Ids from the Calender request
contractor_calender_url = "https://clients.quickcontractors.com/Contractor/WebServices/ContractorWebService.asmx/Get_ContractorCalendar"
contractor_calender_payload = "{contractorId: 6189, startdate: '6/30/2023' , enddate: '7/1/2023'}"
try: 
    get_calender_data  = requested_session.post(contractor_calender_url, data=contractor_calender_payload ,cookies=post.cookies)

    print(get_calender_data)
except: 
    print("failed to get calender")

#Getting the data using the job id's one by one 
# current_job_id = '1832193'
# job_data_url = f"https://clients.quickcontractors.com/Contractor/JobSearch/ManageJobs.aspx?XCode={current_job_id}"
# try:
#     get_job_data = requested_session.get(job_data_url, cookies=post.cookies, headers=headers, data= {'XCode':current_job_id})
#     print(get_job_data.text)
# except:
#     print("Job data didn't found")

#adding data to the excel 









import time
import requests
from requests.auth import HTTPProxyAuth
import json


def call_upload(retryImport=True):
    project = "Philips.PIC"
    testsuite = "Single Patient View3 5.0"
    apikey = "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00"
    proxy = ""
    username = ""
    password = ""
    maxretrytime = 30
    
    payload = {
        "project_name": project,
        "testsuite_name": testsuite,
    }
    filepath = "example.txt"

    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]

    headers = {
        "Token": apikey,
    }
    apiurl = "http://40.69.156.67/fileimport/upload"

    print(headers)
    print(payload)
    print(apiurl)
    print("=======================================")

    retryCount = 3
    timetowait = (maxretrytime / 2) / retryCount

    if proxy == "":
        response = requests.post(apiurl, headers=headers, data=payload, files=files)

        for x in range(retryCount):
            if response.status_code == 200 or response.status_code == 201:
                break
            print(("Status code : [{0}] Retrying".format(response.status_code)))
            time.sleep(timetowait)
            # files = {
            #     "file": open(filepath, "rb"),
            # }
            files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
            response = requests.post(apiurl, headers=headers, data=payload, files=files)
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #    "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )
        except:
            print("Exception importing, retrying")
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl, headers=headers, data=payload, files=files, proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #     "file": open(filepath, "rb"),
                # }
                files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.post(
                    apiurl,
                    headers=headers,
                    data=payload,
                    files=files,
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.post(
                        apiurl,
                        headers=headers,
                        data=payload,
                        files=files,
                        proxies=proxies,
                        auth=auth,
                    )

    print("file upload sent")
    if response.status_code >= 500:
        if retryImport == True and "Parse error" in response.content.decode("utf-8"):
            print("retrying import after parsing errors")
            call_upload(retryImport=False)
            return
        else:
            print(
                (
                    "[!] [{0}] Server Error {1}".format(
                        response.status_code, response.content.decode("utf-8")
                    )
                )
            )
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: []".format(response.status_code)))
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        resultset = json.loads(response.content.decode("utf-8"))
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    if retryImport == True:
        if response.status_code != 200 and response.status_code != 201:
            print("retrying import")
            time.sleep(5)
            call_upload(retryImport=False)


def get_tests_file(retryImport=True):
    project = "Philips.PIC"
    testsuite = "Single Patient View3 5.0"
    apikey = "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00"
    proxy = ""
    username = ""
    password = ""
    maxretrytime = 30
    
    payload = {
        "project_name": project,
        "testsuite_name": testsuite,
    }

    headers = {
        "Token": apikey,
    }
    apiurl = "http://40.69.156.67/fileimport/download"

    print(headers)
    print(payload)
    print(apiurl)
    print("=======================================")

    retryCount = 3
    timetowait = (maxretrytime / 2) / retryCount

    if proxy == "":
        response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                )
       
        for x in range(retryCount):
            if response.status_code == 200 or response.status_code == 201:
                break
            print(("Status code : [{0}] Retrying".format(response.status_code)))
            time.sleep(timetowait)
            # files = {
            #     "file": open(filepath, "rb"),
            # }
            response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                )
    else:
        try:
            httpproxy = "http://" + proxy
            httpsproxy = "https://" + proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies
                )               
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #    "file": open(filepath, "rb"),
                    # }
                    
                    response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies = proxies
                )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                
                        proxies=proxies,
                        auth=auth,
                    )
        except:
            print("Exception importing, retrying")
            httpproxy = proxy
            httpsproxy = proxy
            proxies = {"http": httpproxy, "https": httpsproxy}
            if username == "":
                # files = {
                #    "file": open(filepath, "rb"),
                # }
                #files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                    proxies=proxies
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                
                        proxies=proxies,
                    )
            else:
                auth = HTTPProxyAuth(username, password)
                # files = {
                #     "file": open(filepath, "rb"),
                # }
                response = requests.get(
                    apiurl,
                    headers=headers,
                    params=payload,
                    timeout=600,
                
                    proxies=proxies,
                    auth=auth,
                )
                for x in range(retryCount):
                    if response.status_code == 200 or response.status_code == 201:
                        break
                    time.sleep(timetowait)
                    # files = {
                    #     "file": open(filepath, "rb"),
                    # }
                    #files = [("file", (filepath, open(filepath, "rb"), "text/xml"))]
                    response = requests.get(
                        apiurl,
                        headers=headers,
                        params=payload,
                        timeout=600,
                
                        proxies=proxies,
                        auth=auth,
                    )

    print("file sent")
    if response.status_code >= 500:
        if retryImport == True and "Parse error" in response.content.decode("utf-8"):
            print("retrying import after parsing errors")
            get_tests_file(retryImport=False)
            return
        else:
            print(
                (
                    "[!] [{0}] Server Error {1}".format(
                        response.status_code, response.content.decode("utf-8")
                    )
                )
            )
    elif response.status_code == 404:
        print(("[!] [{0}] URL not found: []".format(response.status_code)))
    elif response.status_code == 401:
        print(("[!] [{0}] Authentication Failed".format(response.status_code)))
    elif response.status_code == 400:
        print(
            (
                "[!] [{0}] Bad Request: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    elif response.status_code >= 300:
        print(("[!] [{0}] Unexpected Redirect".format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        #resultset = json.loads(response.content.decode("utf-8"))
        #print(response.content)
        return response.content.decode("utf-8")
    else:
        print(
            (
                "[?] Unexpected Error: [HTTP {0}]: Content: {1}".format(
                    response.status_code, response.content
                )
            )
        )
    if retryImport == True:
        if response.status_code != 200 and response.status_code != 201:
            print("retrying import")
            time.sleep(5)
            get_tests_file(retryImport=False)

#call_upload(True)
def compare_file_to_string(file_path, string):
    """
    Compares the contents of a file to a given string.
    Returns an array of lines from the file that were not found in the string.
    """
    lines_not_found = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line not in string:
                lines_not_found.append(line)

    return lines_not_found

values = "VerifyApplications\nFindPatient\nAdmittedPatientDataIsDisplayed\nDischargedPatientDataIsDisplayed\nServiceRunningBehavior\nServiceRestartBehavior\nestartMeCrashBehavior\nRestartMeRestartBehavior\nRestartAllCrashBehavior\nRestartAllRestartBehavior\nLoggingBehaviorForDBEngineHostWhenItCrashes\nLoggingBehaviorForDBEngineHostWhenItRestarts\nStartBehaviour_PrimaryServer\nStartBehaviour_Surveillance\nStartBehaviour_Overview\nStartBehaviour_Acquisition\nStartBehaviour_NotificationServer\nStartBehaviour_PhysioServer\nStartBehaviour_WebServer\nStartBehaviour_MobilityServer\nStartBehaviour_BaseNotificationServer\nApplicationHostBehaviour_Surveillance\nApplicationHostBehaviour_Overview\nCoreServiceRecovery_Variant0"
#values = get_tests_file(True)
#if values == "{\"message\":\"No file found\"}":
#    print("here")
#print(values)
new_tests = compare_file_to_string("example.txt",values)
for test in new_tests:
    print(test)
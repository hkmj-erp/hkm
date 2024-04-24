import frappe, requests, json
from ast import literal_eval
from datetime import datetime
import xml.etree.ElementTree as ET


@frappe.whitelist()
def fetch():
    api_auth = {"page_limit": 10000, "bio_user": "ESSL", "bio_pwd": "Hk@hr#123"}
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    url = "http://59.144.166.140:82/iclock/Default.aspx?op=GetTransactionsLog"

    payload = (
        """<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n
    <soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" 
    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" 
    xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    
    <soap:Body>\r\n        
        <GetTransactionsLog xmlns=\"http://tempuri.org/\">\r\n            
        <FromDate>{}</FromDate>\r\n            
        <ToDate>{}</ToDate>\r\n            
        <SerialNumber>AF39202660402</SerialNumber>\r\n            
        <UserName>%(bio_user)s</UserName>\r\n            
        <UserPassword>%(bio_pwd)s</UserPassword>\r\n            
        <strDataList>Attendance</strDataList>\r\n        
        </GetTransactionsLog>\r\n    
    </soap:Body>\r\n
    </soap:Envelope>""".format(
            today_str, today_str
        )
        % api_auth
    )
    headers = {"Content-Type": "text/xml"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

    root = ET.fromstring(response.text)
    strlist = root[0][0][1].text

    checkins = []
    print(strlist.splitlines())
    for rowstr in strlist.splitlines():
        splited = rowstr.split("\t", 1)
        attlog = {"user_id": splited[0], "log_at": splited[1]}
        print(attlog)
        checkins.append(attlog)
    return
    employees = frappe.get_all(
        "Employee", fields=["name", "company", "attendance_device_id"]
    )
    for employee in employees:
        if employee.attendance_device_id is not None:
            for checkin in checkins:
                if checkin["user_id"] == employee.attendance_device_id:
                    checkin_doc = frappe.get_doc(
                        {
                            "doctype": "Employee Checkin",
                            "employee": employee.name,
                            "time": checkin["log_at"],
                        }
                    )
                    checkin_doc.insert()

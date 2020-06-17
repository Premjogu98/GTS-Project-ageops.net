from selenium import webdriver
import time
import Global_var
import sys, os
from datetime import datetime
import requests
import urllib.request
import urllib.parse
import re
import html
import string


# def Translate(text_without_translate):
#     global a
#     a = False
#     while a == False:
#         string3 = ''
#         try:
#             String2 = str(text_without_translate)
#             url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#             response1 = requests.get(str(url))
#             response2 = response1.url
#             user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#             headers = {'User-Agent': user_agent, }
#             request = urllib.request.Request(response2, None, headers)  # The assembled request
#             time.sleep(1.2)
#             response = urllib.request.urlopen(request)
#             htmldata: str = response.read().decode('utf-8')
#             trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)', htmldata).group(0).strip()
#             trans_data = html.unescape(str(trans_data)).strip()
#             return trans_data
#
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type,
#                   "\n", exc_tb.tb_lineno)
#             a = False
#             # return string3  # If String Not Going to translate then Send a blank string3


def getsource():
    Json_Data1 = ''
    a = True
    while a == True:
        try:
            url = 'https://ageops.net/api/bidding-opportunities?page_size=100&page_index=0&lang=en'
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            headers = {'User-Agent': user_agent, }
            request = urllib.request.Request(url, None, headers)  # The assembled request
            response = urllib.request.urlopen(request)
            time.sleep(1.2)
            htmldata: str = response.read().decode('utf-8')
            htmldata = htmldata.partition("[")[2].partition("]")[0]
            Json_Data1 = [int(e) if e.isdigit() else e for e in htmldata.split('},')]
            a = False
        except Exception as e:
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                   exc_tb.tb_lineno)
            time.sleep(5)
            a = True
    tender_link_list = []
    b = True
    while b == True:
        try:
            for Json_Data in Json_Data1:
                start_date_en = Json_Data.partition('"start_date_en":')[2].partition(',"')[0].strip('').strip('"')
                datetime_object = datetime.strptime(start_date_en, "%Y-%m-%d")
                start_date_en = datetime_object.strftime("%Y-%m-%d")
                if start_date_en >= Global_var.From_Date:
                    ID = re.search(r"(?<=id\":).*?(?=,)", Json_Data).group(0).strip()
                    tender_link = "https://ageops.net/api/bidding-opportunities-details?id=" + str(ID) + "&lang=en"
                    tender_link_list.append(tender_link)
                else:
                    Scraping_data(tender_link_list)
            Scraping_data(tender_link_list)
            b = False
        except Exception as e:
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                   exc_tb.tb_lineno)
            time.sleep(5)
            b = True


def Scraping_data(tender_link_list):
    for tender_href in tender_link_list:
        d = True
        while d == True:
            try:
                SegField = []
                for data in range(45):
                    SegField.append('')
                Tender_Details = ''
                c = True
                while c == True:
                    try:
                        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                        headers = {'User-Agent': user_agent, }
                        request = urllib.request.Request(tender_href, None, headers)  # The assembled request
                        response = urllib.request.urlopen(request)
                        Tender_Details: str = response.read().decode('utf-8')
                        Tender_Details = Tender_Details.replace('\\n', '').replace('null', '').replace('\\r',' ')
                        c = False
                    except Exception as e:
                        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                               exc_tb.tb_lineno)
                        time.sleep(5)
                        c = True

                # =============================================================================================================

                description_en = Tender_Details.partition('"description_en":"')[2].partition('","')[0].strip('')
                if description_en != '':
                    if '\\u' in description_en:
                        description_en = description_en.encode('utf-8')
                        description_en = description_en.decode('unicode-escape')
                        description_en = re.sub(' +', ' ', str(description_en))
                        # description_en = Translate(description_en)
                        description_en = string.capwords(str(description_en))
                        SegField[19] = description_en.replace('\\','').replace('//',' ')

                    else:
                        # description_en = Translate(description_en)
                        if 'Title:' in description_en:
                            description_en = Tender_Details.partition('Title:')[2].partition(',')[0].strip(
                                '')
                        description_en = re.sub(' +', ' ', str(description_en))
                        description_en = string.capwords(str(description_en))
                        SegField[19] = description_en.replace('\\','').replace('//',' ')
                else:
                    description_da = Tender_Details.partition('description_da":"')[2].partition('","')[0].strip('')
                    if '\\u' in description_da:
                        description_da = description_da.encode('utf-8')
                        description_da = description_da.decode('unicode-escape')
                        # description_da = Translate(description_da)
                        if 'Title:' in description_da:
                            description_da = Tender_Details.partition('Title:')[2].partition(',')[0].strip(
                                '')
                        description_da = re.sub(' +', ' ', str(description_da))
                        description_da = string.capwords(str(description_da))
                        SegField[19] = description_da.replace('\\','').replace('//',' ')
                    else:

                        # description_da = Translate(description_da)
                        if 'Title:' in description_da:
                            description_da = Tender_Details.partition('Title:')[2].partition(',')[0].strip(
                                '')
                        description_da = re.sub(' +', ' ', str(description_da))
                        description_da = string.capwords(str(description_da))
                        SegField[19] = description_da.replace('\\/','')

                # =============================================================================================================
                procurement_entity_en = Tender_Details.partition('"procurement_entity_en":')[2].partition(',"')[
                    0].strip(
                    '').strip('"')
                if procurement_entity_en != "":
                    if '\\u' in procurement_entity_en:
                        procurement_entity_en = procurement_entity_en.encode('utf-8')
                        procurement_entity_en = procurement_entity_en.decode('unicode-escape')
                        # procurement_entity_en = Translate(procurement_entity_en)
                        SegField[12] = procurement_entity_en.upper().replace('\\','').replace('//',' ')
                    else:
                        # procurement_entity_en = Translate(procurement_entity_en)
                        SegField[12] = procurement_entity_en.upper().replace('\\','').replace('//',' ')
                else:
                    procurement_entity_da = Tender_Details.partition('"procurement_entity_da":')[2].partition(',"')[
                        0].strip(
                        '').strip('"')
                    # print(procurement_entity_da)
                    if '\\u' in procurement_entity_da:
                        procurement_entity_da = procurement_entity_da.encode('utf-8')
                        procurement_entity_da = procurement_entity_da.decode('unicode-escape')
                        # procurement_entity_da = Translate(procurement_entity_da)
                        SegField[12] = procurement_entity_da.upper().replace('\\','').replace('//',' ').strip()
                    else:
                        # procurement_entity_da = Translate(procurement_entity_da)
                        SegField[12] = procurement_entity_da.upper().replace('\\','').replace('//',' ').strip()

                # ========================================================================================================

                identification_number = Tender_Details.partition('"identification_number":')[2].partition(',"')[
                    0].strip(
                    '').strip('"').replace('\\', '')
                # print(identification_number)
                SegField[13] = identification_number

                # =============================================================================================================

                procurement_type_en = Tender_Details.partition('"procurement_type_en":')[2].partition(',"')[0].strip(
                    '').strip(
                    '"')
                if procurement_type_en != "":
                    if '\\u' in procurement_type_en:
                        procurement_type_en = procurement_type_en.encode('utf-8')
                        procurement_type_en = procurement_type_en.decode('unicode-escape')
                        # procurement_type_en = Translate(procurement_type_en)
                        procurement_type_en = string.capwords(str(procurement_type_en))
                        SegField[3] = procurement_type_en
                    else:
                        # procurement_type_en = Translate(procurement_type_en)
                        procurement_type_en = string.capwords(str(procurement_type_en))
                        SegField[3] = procurement_type_en
                else:
                    procurement_type_da = Tender_Details.partition('"procurement_type_da":"')[2].partition(',"')[
                        0].strip(
                        '').strip(
                        '"')
                    if '\\u' in procurement_type_da:
                        procurement_type_da = procurement_type_da.encode('utf-8')
                        procurement_type_da = procurement_type_da.decode('unicode-escape')
                        # procurement_type_da = Translate(procurement_type_da)
                        procurement_type_da = string.capwords(str(procurement_type_da))
                        SegField[3] = procurement_type_da
                    else:
                        # procurement_type_da = Translate(procurement_type_da)
                        procurement_type_da = string.capwords(str(procurement_type_da))
                        SegField[3] = procurement_type_da

                # ============================================================================================================

                procurement_method_en = Tender_Details.partition('"procurement_method_en":')[2].partition(',"')[
                    0].strip(
                    '').strip('"')
                if procurement_method_en != "":
                    if '\\u' in procurement_method_en:
                        procurement_method_en = procurement_method_en.encode('utf-8')
                        procurement_method_en = procurement_method_en.decode('unicode-escape')
                        # procurement_method_en = Translate(procurement_method_en)
                        procurement_method_en = string.capwords(str(procurement_method_en))
                        SegField[4] = procurement_method_en
                    else:
                        # procurement_method_en = Translate(procurement_method_en)
                        procurement_method_en = string.capwords(str(procurement_method_en))
                        SegField[4] = procurement_method_en
                else:
                    procurement_method_da = Tender_Details.partition('"procurement_method_da":')[2].partition(',"')[
                        0].strip(
                        '').strip('"')
                    if '\\u' in procurement_method_da:
                        procurement_method_da = procurement_method_da.encode('utf-8')
                        procurement_method_da = procurement_method_da.decode('unicode-escape')
                        # procurement_method_da = Translate(procurement_method_da)
                        procurement_method_da = string.capwords(str(procurement_method_da))
                        SegField[4] = procurement_method_da
                    else:
                        # procurement_method_da = Translate(procurement_method_da)
                        procurement_method_da = string.capwords(str(procurement_method_da))
                        SegField[4] = procurement_method_da

                # =============================================================================================================

                start_date_en = Tender_Details.partition('"start_date_en":')[2].partition(',"')[0].strip('').strip('"')
                datetime_object = datetime.strptime(start_date_en, "%Y-%m-%d")
                start_date_en = datetime_object.strftime("%Y-%m-%d")
                SegField[5] = start_date_en
                # =============================================================================================================

                end_date_en = Tender_Details.partition('"end_date_en":')[2].partition(',"')[0].strip('').strip('"')
                # print(end_date_en)
                end_date_en = datetime.strptime(end_date_en, "%Y-%m-%d")
                end_date_en = end_date_en.strftime("%Y-%m-%d")
                SegField[24] = end_date_en

                # =============================================================================================================

                bidding_document_download = Tender_Details.partition('"bidding_document_download":')[2].partition(',"')[
                    0].strip(
                    '').replace('\\', '').replace('[', '').replace(']', '').strip('"')
                # print(bidding_document_download)
                SegField[41] = bidding_document_download

                # =============================================================================================================

                amendment_document_download = \
                Tender_Details.partition('"amendment_document_download":')[2].partition(',"')[
                    0].strip(
                    '').replace('\\', '').replace('[', '').replace(']', '').strip('"')
                # print(amendment_document_download)
                SegField[42] = amendment_document_download

                # =============================================================================================================

                notices_document_download = Tender_Details.partition('"notices_document_download":')[2].partition('}')[
                    0].strip(
                    '').replace('\\', '').replace('[', '').replace(']', '').strip('"')
                # print(notices_document_download)
                SegField[43] = notices_document_download

                SegField[18] = str(SegField[19]) + '<br>\n تاریخ اعلام تدارکات: ' + str(
                    SegField[5]) + '<br>\n آخرین مهلت ارسال پیشنهاد: ' + str(
                    SegField[24]) + '<br>\n روش تهیه: ' + str(
                    SegField[4]) + '<br>\n نهاد تدارکاتی: ' + str(
                    SegField[12]).lower().strip() + '<br>\n نوع تدارکات: ' + str(SegField[3])

                ID = re.search(r"(?<=id\":).*?(?=,)", Tender_Details).group(0).strip()
                SegField[28] = 'https://ageops.net/en/procurement-procedure/announcement/bidding/' + str(ID) + ''

                SegField[31] = 'ageops.net'

                SegField[27] = "0"
                SegField[22] = "0"
                SegField[26] = "0.0"

                # =============================================== Notice_type ===================================================
                SegField[14] = '2'
                # =============================================== Ind_classification ===================================================
                SegField[16] = '1'
                # =============================================== MFA ===================================================
                SegField[17] = '0'

                SegField[7] = "AF"
                for Segdata in range(len(SegField)):
                    print(Segdata, end=' ')
                    print(SegField[Segdata])
                check_date(SegField)
                Global_var.Total += 1
                d = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type,
                      "\n", exc_tb.tb_lineno)
                time.sleep(5)
                d = True
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(
        Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
        Global_var.inserted) + "\n""Deadline Not given: " + str(
        Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
        Global_var.QC_Tender),"ageops.net", 1)
    Global_var.Process_End()
    sys.exit()


def check_date(SegField):
    a = 0
    while a == 0:
        tender_date = str(SegField[24])
        nowdate = datetime.now()
        date2 = nowdate.strftime("%Y-%m-%d")
        try:
            if tender_date != '':
                deadline = time.strptime(tender_date , "%Y-%m-%d")
                currentdate = time.strptime(date2 , "%Y-%m-%d")
                if deadline > currentdate:
                    from insert_on_database import insert_in_Local,create_filename
                    insert_in_Local(SegField)
                    a = 1
                else:
                    print("Tender Expired")
                    Global_var.expired += 1
                    a = 1
            else:
                print("Deadline was not given")
                Global_var.deadline_Not_given += 1
                a = 1
        except Exception as e:
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exc_type , exc_obj , exc_tb = sys.exc_info()
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , exc_tb.tb_lineno)
            a = 0
            time.sleep(5)


getsource()

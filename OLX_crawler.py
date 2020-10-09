from bs4 import BeautifulSoup
import requests, os, time

url = os.environ["OLX_URL"]
contact_number = os.environ["CONTACT_NUMBER"]
db_filename = "ad_id_list.txt"
domain_link = """. 

Link: https://www.olx.in"""

new_ad_list = []
new_ad_id_list = []
old_ad_id_list = []


def Crawler():
    global new_ad_list, new_ad_id_list, old_ad_id_list
    new_ad_list, new_ad_id_list = GetAdListFromOLX(url)
    old_ad_id_list = UpdateLocalDB(new_ad_id_list, db_filename)
    count = FindNumberOfNewUpdatesInAds(old_ad_id_list, new_ad_id_list)
    SendWhatsappMsg(count, contact_number, new_ad_list)


# get all the listed ads for ads from site
def GetAdListFromOLX(url):    
    page_res = requests.get(url)
    page_soup = BeautifulSoup(page_res.content, 'html.parser')
    ad_list_items = page_soup.findAll("li", {"class": "EIR5N"})

    ad_id_list = []
    # fetch updated db from OLX into new_ad_id_list
    for ad in ad_list_items:
        ad_element = ad.find("a")
        # print(ad_element.text)
        ad_id_list.append(str(ad_element['href'].split('-iid-')[1]))
    
    return ad_list_items, ad_id_list


# read last updated local db of ads in old_ad_id_list
def UpdateLocalDB(new_ad_list, db_filename):
    old_ad_list = []
    try:
        with open(db_filename, 'r') as f:
            for line in f: 
                old_ad_list.append(line.strip())          
    except Exception as e:
        print("Read is not done")
        print(e)
        
    # save new updated db in local from new_ad_id_list
    with open(db_filename, 'w') as f:
        for id in new_ad_list:
                f.write("%s\n" % id) 
    
    print("\n old list :" + str(old_ad_list))
    print("\n new list :" + str(new_ad_list))
    return old_ad_list


# compare the old db and the new sb to find if any updates have been made
def FindNumberOfNewUpdatesInAds(old_list, new_list):
    count = 0
    for id in old_ad_id_list:
        try:
            count = new_ad_id_list.index(id)
            print("\n ==> Most recent ad from db - " + str(id) + " found at index - " + str(count))
            break
        except Exception as e:
            print(e)
            continue
    return count


# send the updated ads to contact using whatsapp
def SendWhatsappMsg(count, contact_number, ad_list):
    if(count == 0):
        print("\n ==> No updates found.")
        return 0

    from twilio.rest import Client
    client = Client()
    from_whatsapp_number='whatsapp:+14155238886'
    to_whatsapp_number='whatsapp:' + contact_number
    msg = ""

    i = 0
    for ad in ad_list:
        ad_element = ad.find("a")
        msg = ad_element.text
        msg = msg + domain_link + ad_element['href']
        i = i+1

        print("Message is : \n")
        print(msg.encode('utf-8'))    
        client.messages.create(body=msg,
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)
        time.sleep(1)
        
        if(i>=count):
            break


if __name__ == '__main__':
    print("\n ==> The crawler has started.")
    Crawler()

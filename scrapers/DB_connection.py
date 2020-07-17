import mysql.connector
#pip install mysql-connector-python==8.0.17
from bs4 import BeautifulSoup
#pip3 install bs4
import requests



creds=open("creds.txt","r")
line=creds.readlines()
mydb = mysql.connector.connect(
  host=line[4].replace('\n',''),
  user=line[5].replace('\n',''),
  passwd=line[6].replace('\n',''),
  database=line[7].replace('\n','')
)

mycursor = mydb.cursor()

#mycursor.execute(sql, val)

def insert_congress_table(member):

    sql = """INSERT INTO example_congress 
    (first_name, last_name, contact, party, 
    district, state, house, website,imageLink,
    congress_num,congresslink,served) 
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()

def update_congress_table(member):

    sql = """UPDATE example_congress SET
    first_name=%s, last_name=%s, contact=%s, party=%s, 
    district=%s, state=%s, house=%s, website=%s,imageLink=%s,
    congress_num=%s,congresslink=%s,served=%s 
    WHERE congresslink= '{}'""".format(member[10])

    mycursor.execute(sql, member)
    mydb.commit()


def update_bills_table(bill):

    sql = "UPDATE example_bill SET name=%s,title=%s,progress=%s,link=%s,congress_num=%s,chamber=%s WHERE link = '" + bill[3] +"'"

    mycursor.execute(sql,bill)

    mydb.commit()

def insert_committee_table(member):

    sql = """INSERT INTO example_committee 
    (name, location, importance, address, 
    phone, link) 
    VALUES (%s,%s,%s,%s,%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()

def insert_bills_table(member):

    sql = """INSERT INTO example_bill 
    (name, title, progress, link, 
    congress_num,chamber) 
    VALUES (%s,%s,%s,%s,%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()


def insert_congress_bill_table(member):

    sql = """INSERT INTO example_congress_bills 
    (congress_id,bill_id) 
    VALUES (%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()

def insert_congress_cosponsored_table(member):
    sql = """INSERT INTO example_congress_cosponsored 
    (congress_id,bill_id) 
    VALUES (%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()

def insert_committee_members_table(member):
    sql = """INSERT INTO example_committee_members 
    (committee_id,congress_id) 
    VALUES (%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()

def insert_subcommittee_members_table(member):
    sql = """INSERT INTO example_sub_committee_members 
    (sub_committee_id,congress_id) 
    VALUES (%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()


def insert_sub_committee_table(member):

    sql = """INSERT INTO example_sub_committee 
    (name, committee_id, link) 
    VALUES (%s,%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()


def load_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
        

def load_senate_committees():
    senate = load_page("https://www.senate.gov/general/committee_membership/committee_memberships_SSAF.htm")
    options = senate.find(class_='contenttext')
    lists = options.find_all(class_='contenttext',value=True)
    

    for i in lists:
        
        name = i.get_text().replace("\n", "").replace("'", "").split(' on ')[::-1]
        #print(name[0])
        link = 'https://www.senate.gov' + i['value']
        #print(link)

        submition = []
        submition.append(name[0])
        submition.append(20)
        submition.append('N/A')
        submition.append('senate')
        submition.append('N/A')

        sql = "SELECT * FROM example_committee WHERE name='" + name[0] + "' AND location='senate'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if(not myresult):
            insert_committee_table(submition)
        else:
            print("present")


        main = load_page(link)
        temp = main.find(id='secondary_col2')

        try:
            sub = temp.find_all('a',href=True)
        except:
            pass
        try:
            sub.pop(0)
            sub.pop(0)
            sub.pop(0)
        except:
            pass
        #subcommittees
        print(name[0])
        for a in sub:

            sql = "SELECT * FROM example_committee WHERE name='" + name[0] + "' AND location='senate'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            id_start = myresult[0][0]
            subname = a.get_text().split(' on ')[::-1]

            submition1 = []
            submition1.append(subname[0].replace("\n", "").replace("'", ""))
            submition1.append(id_start)

            sql = "SELECT * FROM example_sub_committee WHERE name='" + subname[0].replace("\n", "").replace("'", "") + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            if(not myresult):
                insert_sub_committee_table(submition1)
            else:
                print("present")

            
            print('     ' + subname[0])
        


def load_bill(congress=116,source="legislation",chamber='',type_=''):
    link = 'https://www.congress.gov/search?q='
    search_parameters = {"source":source,"congress":congress}

    if(chamber):
        search_parameters["chamber"] = chamber

    if(type_):
        search_parameters["type"] = type_

    query = link + str(search_parameters).replace("'",'"')
    first = load_page(query)

    #getting the pages to iterate through
    page_numbers = first.find_all(class_='results-number')
    max_page = (page_numbers[1].get_text()).split(' ')[::-1]
    
    #incase theres only one page
    if(max_page[0] == ''):
        max_page[0] = 1

    for i in range(1,int(max_page[0]) + 1):
        page_url = query + '&page=' + str(i)
        page = load_page(page_url)

        group = page.find(class_='basic-search-results-lists expanded-view')
        bills = group.find_all(class_='expanded')

        for bill in bills:
            #some bills are reserved ???
            try:
                name = bill.find('a',href=True).get_text()
                link = bill.find('a',href=True)['href']
                sponsor = bill.find_all('a',href=True)[1]
                cosponsor = bill.find_all('a',href=True)[2]
                if(name[0] == 'H'):
                    chamber = 'House'
                else:
                    chamber = 'Senate'

                #print(name)
                #print(link)
                #print(sponsor['href'])
                #print(chamber)
                #print('########')
                
                #getting the title
                #page1 = load_page(link)
                #subsection = page1.find(class_='tabs_links')
                #link2 = subsection.find_all('a',href=True)[2]['href']


                #page2 = load_page(link2)
                #subsection = page1.find(class_='titles-row')
                #title = subsection.find('p').get_text()
                
                title = 'N/A'
                

                link = link.split('?')
                sql = "SELECT * FROM example_bill WHERE link='" + link[0] + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                #part of the link changes dynamically
                
                submition = []
                submition.append(name)
                submition.append(title)
                submition.append('N/A')
                submition.append(link[0])
                submition.append(congress)
                submition.append(chamber)

                #final check before submition or update
                if(not myresult):
                    insert_bills_table(submition)
                    print(name + " inserted")
                else:
                    update_bills_table(submition)

                    print(name + " updated")

                #linking bill to sponsor
                sql = "SELECT * FROM example_bill WHERE link='" + link[0] + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()

                #print(myresult)
                bill_id = myresult[0][0]
                sponsorlink = 'https://www.congress.gov' + sponsor['href']

                sql = "SELECT * FROM example_congress WHERE congresslink='" + sponsorlink + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                #print(myresult)
                sponsor_id = myresult[0][0]

                submition2 = []
                submition2.append(sponsor_id)
                submition2.append(bill_id)

                #checking if link present
                sql = "SELECT * FROM example_congress_bills WHERE congress_id='" + str(sponsor_id) + "' AND bill_id='" + str(bill_id) + "'"

                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                
                if(not myresult):
                    insert_congress_bill_table(submition2)
                    print(name + " link created")
                else:
                    print(name + " already existing combo")


                #creating/updating co sponsors
                
                if(int(cosponsor.get_text()) != 0):
                    copage = load_page(cosponsor['href'])
                    cotable = copage.find(class_='item_table')
                    copeople = cotable.find_all('a',href=True)
                    for co in copeople:
                        #print('     ' + co['href'])

                        sql = "SELECT * FROM example_congress WHERE congresslink='" + co['href'] + "'"
                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        co_id = myresult[0][0]

                        submition3 = []
                        submition3.append(co_id)
                        submition3.append(bill_id)



                        sql = "SELECT * FROM example_congress_cosponsored WHERE congress_id='" + str(co_id) + "' AND bill_id='" + str(bill_id) + "'"

                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()

                        if(not myresult):
                            insert_congress_cosponsored_table(submition3)
                            print("     " + co.get_text() + " cosponsor added")
                        else:
                            #print(name + " already existing cosponsor")
                            pass





                



            except:
                pass





def load_congress(congress = '116',chamber=''):
    link = 'https://www.congress.gov/members?q='
    search_parameters = {"congress":congress}

    if(chamber):
        search_parameters["chamber"] = chamber
    

    query = link + str(search_parameters).replace("'",'"')

    first = load_page(query)

    #getting the pages to iterate through
    page_numbers = first.find_all(class_='results-number')
    max_page = (page_numbers[1].get_text()).split(' ')[::-1]
    
    #incase theres only one page
    if(max_page[0] == ''):
        max_page[0] = 1

    for i in range(1,int(max_page[0]) + 1):
        page_url = query + '&page=' + str(i)
        page = load_page(page_url)

        group = page.find(class_='basic-search-results-lists expanded-view')
        members = group.find_all(class_='expanded')

        for person in members:
            header = person.find('a',href=True)

            congresslink = header['href']
            holder = header.get_text().split(' ',1)
            #determining if rep or senator
            if(holder[0] == 'Senator'):
                house = 0
            else:
                house = 1
            name = holder[1].split(', ',1)
            first_name = name[1].replace(',','').replace(' ','')
            last_name = name[0].replace(',','').replace(' ','')

            info1 = person.find_all(class_='result-item')
            state = info1[0].find('span').get_text()

            if(house):
                district = info1[1].find('span').get_text()
                party = info1[2].find('span').get_text()
                #some reps dont have districts
                try:
                    served = info1[3].find('span').get_text()
                except:
                    party = info1[1].find('span').get_text()
                    served = info1[2].find('span').get_text()
                    district = 0
            else:
                party = info1[1].find('span').get_text()
                served = info1[2].find('span').get_text().replace('\n','').replace('\t','')
                district = 0

            image = person.find('img')
            #some people dont have pics at all???
            try:
                pic = image['src']
            except:
                pic = ''

            personal_page = load_page(congresslink)
            info2 = personal_page.find(class_='standard01 nomargin')
            #print(info2)
            #some people dont have websites either?? even though the federal
            #government gives them to you for free?!?1
            try:
                website = info2.find('a',href=True)['href']
            except:
                website = 'N/A'
            #some people also dont have contact info
            try:
                contact = info2.find(class_='member_contact')
                contact_info = contact.find_next_sibling('td').get_text().replace('\n','').replace('\t','')
            except:
                contact_info = 'N/A'
            



            submition = []
            submition.append(first_name)
            submition.append(last_name)
            submition.append(contact_info)
            submition.append(party)
            submition.append(district)
            submition.append(state)
            submition.append(house)
            submition.append(website)
            submition.append(pic)
            submition.append(congress)
            submition.append(congresslink)
            submition.append(served)

            sql = "SELECT * FROM example_congress WHERE congresslink='" + str(congresslink) + "'"

            mycursor.execute(sql)
            myresult = mycursor.fetchall()
                
            if(not myresult):
                insert_congress_table(submition)
                print(first_name + ' ' + last_name + " added")
            else:
                update_congress_table(submition)
                print(first_name + ' ' + last_name + " updated")
                #update

            


            #print(first_name + ' ' + last_name)
            #print(contact_info)
            #print(party)
            #print(district)
            #print(state)
            #print(house)
            #print(pic)
            #print(website)
            #print(served)
            #print('###########')

#load_congress(115)

#sql = "DELETE FROM example_committee"
#mycursor.execute(sql)
#mydb.commit()


def load_congress_committee():
    directory = load_page('https://clerkpreview.house.gov/Committees/')
    committees = directory.find_all(class_='col-sm-11 col-xs-10 library-committeePanel-heading')
    #main committees
    for committee in committees:
        name = committee.get_text().replace('\n','').split('on ',1)[::-1]
        #print(name[0])
        link = committee.find('a',href=True)['href']
        link = "https://clerkpreview.house.gov" + link
        committee_page = load_page(link)



        address = committee_page.find(class_='address').get_text()
        phone = committee_page.find(class_='phone').get_text()
        #print('PHONE: ' + phone)
        #print('LOCATION: ' + address)
        submition1 = []
        submition1.append(name[0])
        submition1.append('house')
        submition1.append(0)
        submition1.append(address)
        submition1.append(phone)
        submition1.append(link)

        sql = "SELECT * FROM example_committee WHERE link='" + str(link) + "'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
                
        if(not myresult):
            insert_committee_table(submition1)
            print(name[0] + " added")

            sql = "SELECT * FROM example_committee WHERE link='" + str(link) + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        else:
            print(name[0] + ' Already exists')

        committee_id = myresult[0][0]



        try:
            #subcommittees
            sub_directory = committee_page.find(class_='subcommittees')
            subcommittee = sub_directory.find_all('a',href=True)
            print('     SUBCOMMITTEES: ')
            for sub in subcommittee:

                sublink = 'https://clerkpreview.house.gov' + sub['href']
                subname = sub.get_text()
                subpage = load_page(sublink)

                submition2 = []
                submition2.append(subname)
                submition2.append(committee_id)
                submition2.append(sublink)
                
                sql = "SELECT * FROM example_sub_committee WHERE link='" + str(sublink) + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                        
                if(not myresult):
                    insert_sub_committee_table(submition2)
                    print('         ' + subname + " added")

                    sql = "SELECT * FROM example_sub_committee WHERE link='" + str(sublink) + "'"
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                else:
                    print('         ' + subname + ' Already exists')
                subcommittee_id = myresult[0][0]


                try:
                    #members of sub committee
                    member_directory = subpage.find(class_='members')
                    submembers = member_directory.find_all('a',href=True)

                    sql = "DELETE FROM example_sub_committee_members WHERE sub_committee_id = {}".format(subcommittee_id)
                    mycursor.execute(sql)
                    mydb.commit()

                    for member in submembers:
                        #print(member['href'])
                        identifier = member['href'].split('/')[::-1]
                        
                        sql = "SELECT * FROM example_congress WHERE congresslink LIKE '%{}%'".format(identifier[0])

                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        congressmen_id = myresult[0][0]

                        submition4 = []
                        submition4.append(subcommittee_id)
                        submition4.append(congressmen_id)
                        insert_subcommittee_members_table(submition4)
                        
                except:
                    print("sub-members not listed")

        except:
            print('no subcommittee')

        print(' ')








        try:
            #members of main committee
            member_directory = committee_page.find(class_='members')
            members = member_directory.find_all('a',href=True)

            #cleaning previous members
            sql = "DELETE FROM example_committee_members WHERE committee_id = {}".format(committee_id)
            mycursor.execute(sql)
            mydb.commit()

            for member in members:
                #print(member['href'])
                identifier = member['href'].split('/')[::-1]
                
                sql = "SELECT * FROM example_congress WHERE congresslink LIKE '%{}%'".format(identifier[0])

                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                congressmen_id = myresult[0][0]

                submition3 = []
                submition3.append(committee_id)
                submition3.append(congressmen_id)
                insert_committee_members_table(submition3)
                #print(congressmen_id
        except:
            print("members not listed")
            
from xml.dom import minidom           

def load_senate_committee():
    pass
    direct = load_page('https://www.senate.gov/general/committee_membership/committee_memberships_SSAP.htm')
    listed = direct.find('form',class_='contenttext')
    links = listed.find_all(class_='contenttext',value=True)
    for link in links:
        xmllink = 'https://www.senate.gov/' + link['value'][:-3] + 'xml'
        print(xmllink)
    #load webpage
    #get all xml file names
    #port to bash to wget
    #call with minidom.parse
        

        

#load_bill(type_="bills")


#possible bill status solution https://stackoverflow.com/questions/54802990/beautifulsoup-find-class-contains-some-specific-words
#import re
#regex = re.compile('.*footer.*')
#soup.find_all("div", {"class" : regex})
#load_bill(type_="bills")

load_senate_committee()
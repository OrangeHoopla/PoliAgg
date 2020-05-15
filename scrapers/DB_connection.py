import mysql.connector
#pip install mysql-connector-python==8.0.17
from bs4 import BeautifulSoup
#pip3 install bs4
import requests

mydb = mysql.connector.connect(
  host="localhost",
  user="orange",
  passwd="19445715mK",
  database="demo"
)

mycursor = mydb.cursor()

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
dummy = ["John", "doe", "imaginary street","Democrat", 12, "Florida", 1,"www.google.com","image.com",115]
#mycursor.execute(sql, val)

#mydb.commit()
#https://www.w3schools.com/python/python_mysql_select.asp
#print(mycursor.rowcount, "record inserted.")


def generate_congress_table():
    columns ="""(
                first_name VARCHAR(255),
                last_name VARCHAR(255), 
                contact VARCHAR(255),
                party VARCHAR(255),
                district INT(255),
                state VARCHAR(255),
                house BOOL,
                website VARCHAR(255),
                imageLink VARCHAR(255),
                congress_num INT(255)
                )"""

    mycursor.execute("CREATE TABLE congress " + columns) 
    mycursor.execute("ALTER TABLE congress ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") 


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
    (name, importance, address, location, 
    phone) 
    VALUES (%s,%s,%s,%s,%s)"""

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


def insert_sub_committee_table(member):

    sql = """INSERT INTO example_sub_committee 
    (name, committee_id) 
    VALUES (%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()


#generate_congress_table();
#mycursor.execute("ALTER TABLE congress ADD congress_num INT(255)")
#insert_congress_table(dummy)
#mycursor.execute("DELETE FROM congress WHERE district=0")

def load_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
        




def load_house_committees():
    house = load_page("http://clerk.house.gov/committee_info/index.aspx")
    table = house.find(id='com_directory')
    lister = table.find_all('li')
    
    for i in lister:
        link = 'http://clerk.house.gov'
        try:
            link = link + i.find('a', href=True)['href']
        except:
            print(i.get_text() + " Skipped")
            submition = []
            submition.append(i.get_text().replace("\n", "").replace("'", ""))
            submition.append(5)
            submition.append("N/A")
            submition.append("N/A")
            submition.append("N/A")
            sql = 'SELECT * FROM example_committee WHERE name ="' + i.get_text().replace("\n", "").replace("'", "") + '"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            if(not myresult):
                insert_committee_table(submition)
            else:
                print(name[0].replace("'", "") + "already there")
            continue
            #some committees dont have a link

        #print(i.get_text().replace("\n", ""))
        commitee = load_page(link)
        main = commitee.find(id='com_display')

        name = main.find('h3').get_text().replace("\n", "").split(' on ')[::-1] # my magic
        print(name[0])
        location = 'house'
        address = main.find(id='address').get_text().replace("\n", "")
        phone = "N/A"
        submition1 = []
        submition1.append(name[0].replace("'", ""))
        submition1.append(0)
        submition1.append(address)
        submition1.append('house')
        submition1.append('N/A')

        sql = 'SELECT * FROM example_committee WHERE name ="' + name[0].replace("'", "") + '" AND location="house"'
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if(not myresult):
            insert_committee_table(submition1)
        else:
            print(name[0].replace("'", "") + "already there")
            

        #^^^ un comment to redo 


        #filling subcommittees

        #pulling id from committee
        sql = "SELECT * FROM example_committee WHERE name ='" + name[0].replace("'", "") + "' AND location='house'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        id_start = myresult[0][0]

        sub = main.find(id='subcom_list')
        subcommittees = sub.find_all('li')

        for j in subcommittees:
            #print('     ' + j.get_text().replace("\n", ""))
            group = 'http://clerk.house.gov'
            submition2 = []
            submition2.append(j.get_text().replace("\n", "").replace("'", "")) # name
            submition2.append(id_start)

            #checking if its in the table already
            sql = 'SELECT * FROM example_sub_committee WHERE name ="' + j.get_text().replace("\n", "").replace("'", "") + '"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            if(not myresult):
                insert_sub_committee_table(submition2)
            else:
                print(j.get_text().replace("\n", "") + "already there")
                

            #will need later for assigning members
            group = group + j.find('a', href=True)['href']

            #print(group)



#load_house_committees()


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
        
        
    
def load_bill_by_committee(congress,commitee):
    pass


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

#sql = "DELETE FROM example_bill"
#mycursor.execute(sql)
#mydb.commit()


load_bill(type_="bills")

#load_congress(116)

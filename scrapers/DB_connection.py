import mysql.connector
#pip install mysql-connector-python==8.0.17
from bs4 import BeautifulSoup
#pip3 install bs4
import requests

mydb = mysql.connector.connect(
  host="localhost",
  user="orange",
  passwd="",
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
    congress_num) 
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    mycursor.execute(sql, member)
    mydb.commit()




def insert_committee_table(member):

    sql = """INSERT INTO example_committee 
    (name, importance, address, location, 
    phone) 
    VALUES (%s,%s,%s,%s,%s)"""

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
mycursor.execute("DELETE FROM congress WHERE district=0")

def load_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup



def load_senate(congress):

    senate = load_page('https://www.congress.gov/members?pageSize=100&q={"congress":"' 
        + str(congress) + 
        '","chamber":"Senate"}')


    names = senate.find_all(class_='result-heading')

    for i in range(0,200,2):

        link = names[i].find('a', href=True)                # individual
        #print(link['href'])
        #print(link.get_text())  #link to individual page



        senator = load_page(link['href'])


        main = senator.find(class_='overview')
        pic = main.find('a', href=True)['href'] # link to image


        # needs to be reworked
        body = senator.find(class_='overview-member-column-profile member_profile')
        parts = body.find_all('td')


        other = senator.find(class_='standard01 nomargin')
        obj = other.find_all('td')




        state = parts[0].get_text().replace("\n", "") # works
        name = link.get_text().split() # works

        try:
            website = obj[0].get_text().replace("\n", "")
        except:
            website = "N/A"
        try:
            contact = obj[1].get_text().replace("\n", "")
        except:
            contact = "N/A"
            party = website
            website = "N/A"
        try:
            party = obj[2].get_text().replace("\n", "")
        except:
            party = obj[0].get_text().replace("\n", "")
        

        print(name[1][:-1])
        print(name[2])
        print(state)
        print(website)
        print(contact)
        print(party)
        print("#########")

        submition = []
        submition.append(name[2]) # first name
        submition.append(name[1][:-1]) # last name
        submition.append(contact)
        submition.append(party)
        submition.append(0)
        submition.append(state)
        submition.append(0)
        submition.append(website)
        submition.append(pic)
        submition.append(congress)


        insert_congress_table(submition)





def load_house(congress):
    #https://www.congress.gov/members?q={%22congress%22:%22115%22,%22chamber%22:%22House%22}&searchResultViewType=expanded&KWICView=false&pageSize=100&page=1
    house = load_page('https://www.congress.gov/members?pageSize=100&q={"congress":"' 
        + str(congress) + 
        '","chamber":"House"}')



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
        
        
    

        
load_house_committees()
load_senate_committees()




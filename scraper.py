from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# utf8 support
import codecs

# regex
import re

# for debugging
from pprint import pprint

import pymysql.err


from db import Db

class Scraper:
    def __init__(self,domain,connection):
        self.domain = domain
        self.connection = connection

    def scrape(self, uri):
        url      = self.domain + '/' + uri 
        source   = urlopen(url)
        pageHtml = source.read()
        source.close()

        listOfCars = []

        # html parsing
        pageSoup = soup(pageHtml,'html.parser',from_encoding='utf-8')

         # traverse the html
        cars = pageSoup.find_all("article", {'class':'f24'})

        for car in cars:
            try:
                model = car.find("img")['title'].replace(",","")
            except:
                model = 'unknown'

            try: 
                price = car.findAll("section")[1].findAll("div",{"class":"text-black"})[0].text.replace(",","")
            except:
                price = 'unknown'
            
            try:
                descr = car.find("p",{'class':'minh72'}).text.strip().replace(",","")
            except:
                descr = 'unknown'

            listOfCars.append({'model':model,'price':price,'description':descr})

        return listOfCars


    def saveToFile(self, file_name, cars):
        filename = './cars/' + file_name + '.csv'

        f = codecs.open(filename, 'w', 'utf-8')

        headers = 'model, price, description'
        f.write(headers)

        # Inside a loop
        for car in cars:
            f.write('\n' + car['model'] + ',' + car['price'] + ',' + car['description'])
        
        f.close()


    def getAll(self):
        try:
            with self.connection.cursor() as cursor:
                # Read all the records
                sql = "SELECT `id`, `model` FROM `cars` WHERE 1"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except pymysql.err.InternalError as e:
            print(e)


    def getById(self,id):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `model` FROM `cars` WHERE `id`=%s"
                cursor.execute(sql, (int(id)))
                result = cursor.fetchone()
                return result
        except pymysql.err.InternalError as e:
            print(e)


    def store(self,car):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `cars` (`model`, `price`, `description`) VALUES (%s, %s, %s)"
                
                # Sanitize the price
                price = re.sub("[^0-9]","",car['price'])
                price = int(price) if len(price)>0 else 0
                
                cursor.execute(sql, (car['model'], price, car['description']))

                id = cursor.lastrowid
        
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
            
            return id  
        except pymysql.err.InternalError as e:
            print(e)

            return 0

    
    def storeAll(self,cars):
        ids = []
        for car in cars:
            id = self.store(car)
            ids.append(id)

        return ids

    
    def update(self,id,car):
        try:
            with self.connection.cursor() as cursor:
                # Update a record
                sql = "UPDATE `cars` SET `model`=%s WHERE `id` = %s"  
                cursor.execute(sql,(car['model'],str(id)))
                self.connection.commit()
                return True
        except pymysql.err.InternalError as e:
            print(e)
            return False

    
    def delete(self,id):
        try:
            with self.connection.cursor() as cursor:
                # Delete a record
                sql = "DELETE FROM `cars` WHERE `id` = '%s' LIMIT 1"  
                cursor.execute(sql,(int(id)))
                self.connection.commit()
                return True
        except pymysql.err.InternalError as e:
            print(e)
            return False



file_name = "./web_addresses.txt" 

try:
    file = open(file_name, "r") 
    domain = file.read() 
    file.close()

    domain = "https://www.caranddriver.com"
    models = ["bmw","audi"]

    d   = Db(host='localhost',user='root',password='',db='test')
    con = d.connect()


    if con is not None:
        # Creating object out of the class
        s = Scraper(domain, con)

    #     ids = []
    #     for m in models:
    #         cars = s.scrape(m)
    #         s.saveToFile(m,cars)
    #         ids = s.storeAll(cars)

    #     pprint(ids)
        

        # Get a record by id
        # record = s.getById(24)
        # if record is not None:
        #     pprint(record)
        #     pprint(record['model'])
        # else:
        #     print('Not a record')


        # Get the list of records
        # records = s.getAll()
        # if records is not None:
        #     if len(records) > 0:
        #         for record in records:
        #             pprint(record['model'])
        #     else:
        #         print('No records')
        # else:
        #     print('Error in getting the list')


        # Delete a record
        # id = 24
        # if(s.delete(id)):
        #     record = s.getById(id)
        #     if record is not None:
        #         print("The record with the id of " + str(id) + " hasn't been deleted")
        #     else:
        #         print("The record with the id of " + str(id) + " doesn't exist as expected")
        # else:
        #     print("Problem in deleting the record")


        # Update a record
        id = 1
        car = {'model':'sussita','price':'4000','description':'The best Israeli car ever'}
        if(s.update(id,car)):
            record = s.getById(id)
            if record is not None:
                pprint(record)
            else:
                print("The record with the id of " + str(id) + " doesn't exist")
        else:
            print("Problem in updating the record id " + str(id))


        # Close he databse connection
        d.disconnect()

except:
    print('cannot open file' + file_name)






from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
# @cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
# @cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","+")
            amazon_url = "https://www.amazon.in/s?k=" + searchString +"&crid=28MRATZJYHLU3&sprefix=iphone+13%2Caps%2C350&ref=nb_sb_noss_2"
            uClient = uReq(amazon_url)
            amazonPage = uClient.read()
            uClient.close()
            amazon_html = bs(amazonPage, "html.parser")
            bigboxes = amazon_html.findAll("div", {"class": "puisg-col-inner"})
            del bigboxes[0:2]
            box = bigboxes[0]
            productLink = "https://www.amazon.in" + box.div.div.h2.a['href']
            prodRes = requests.get(productLink)
            # # prodRes = requests.get(productLink, verify=False)
            # prodRes = requests.get(productLink, verify='/path/to/certificate.pem')

            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find('div', {'id': "productOverview_feature_div"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Brand, operating_system, CPU_speed, Memory_storage_capacity, screen_size \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    Brand = commentbox.div.table.tbody.find('tr', {'class': 'a-spacing-small po-brand'}).text

                except:
                    Brand = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    operating_system = commentbox.div.table.tbody.find('tr', {'class': 'a-spacing-small po-operating_system'}).text


                except:
                    operating_system = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    CPU_speed = commentbox.div.table.tbody.find('tr', {'class': 'a-spacing-small po-cpu_model.speed'}).text
                except:
                    CPU_speed = 'No Comment Heading'
                try:
                    Memory_storage_capacity = commentbox.div.table.tbody.find('tr', {'class': 'a-spacing-small po-memory_storage_capacity'}).text
                    #custComment.encode(encoding='utf-8')
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                try:
                    screen_size=commentbox.div.table.tbody.find('tr', {'class': 'a-spacing-small po-display.size'}).text
                except:
                    screen_size="no screen"

                mydict = {"Brand": Brand, "operating_system": operating_system, "CPU_speed": CPU_speed, "Memory_storage_capacity": Memory_storage_capacity,
                          "screen_size": screen_size}
                reviews.append(mydict)
                reviews.append(mydict)
                reviews.append(mydict)
            return render_template('results2.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	# app.run(debug=True)
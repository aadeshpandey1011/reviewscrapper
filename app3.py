from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index2.html")


@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString=request.form['content'].replace(" ","+")
            website_url = "https://www.servcorp.com.au/en/blog/search/?q="+searchString+"&x=1&y=1"
            uClient = uReq(website_url)
            websitePage = uClient.read()
            uClient.close()
            website_html=bs(websitePage,"html.parser")
            output=website_html.find_all("div",{"class":"content-paging active"})

            box=output[0]
            productLink=box.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'

            prod_html = bs(prodRes.text, "html.parser")

            commentboxes = prod_html.find("p",{"style":"color:#8f8f8f"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Name \n"
            fw.write(headers)
            reviews = []

            try:
                # name.encode(encoding='utf-8')
                name = commentboxes.text

            except:
                name = 'No Name'

            try:
                # rating.encode(encoding='utf-8')
                rating = commentboxes.text


            except:
                rating = 'No Rating'

            try:
                # commentHead.encode(encoding='utf-8')
                commentHead = commentboxes.text

            except:
                commentHead = 'No Comment Heading'
            try:
                comtag = commentboxes.text
                # custComment.encode(encoding='utf-8')
                custComment = comtag[0]
            except Exception as e:
                print("Exception while creating dictionary: ", e)

            mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                      "Comment": custComment}
            reviews.append(mydict)
            reviews.append(mydict)
            reviews.append(mydict)

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index2.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	# app.run(debug=True)
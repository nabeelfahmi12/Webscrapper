import os
from flask import Flask , render_template , request , jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask ( __name__ )


@app.route ( '/' , methods = [ 'GET' ] )
def homePage( ) :
    return render_template ( "index.html" )


@app.route ( '/review' , methods = [ 'POST' , 'GET' ] )
def index( ) :
    if request.method == 'POST' :
        try :
            ProductName = request.form [ 'content' ].replace ( " " , "" )
            flipkart_url = "https://www.flipkart.com/search?q=" + ProductName
            uClient = uReq ( flipkart_url )
            flipkartPage = uClient.read ( )
            uClient.close ( )
            flipkart_html = bs ( flipkartPage , "html.parser" )
            bigboxes = flipkart_html.findAll ( "div" , { "class" : "bhgxx2 col-12-12" } )
            box = bigboxes [ 3 ]
            productLink = "https://www.flipkart.com" + box.div.div.div.a [ 'href' ]
            prodRes = requests.get ( productLink )
            prodRes.encoding = 'utf-8'
            prod_html = bs ( prodRes.text , "html.parser" )
            commentboxes = prod_html.find_all ( 'div' , { 'class' : "_3nrCtb" } )

            filename = ProductName + ".csv"
            fw = open ( filename , "w" )
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write ( headers )
            Reviews = [ ]
            for commentbox in commentboxes :
                try :
                    name = commentbox.div.div.find_all ( 'p' , { 'class' : '_3LYOAd _3sxSiS' } ) [ 0 ].text
                    name.encode(encoding='utf-8')

                except :
                    name = 'Flipkart User'

                try :
                    rating = commentbox.div.div.div.div.text
                    rating.encode(encoding='utf-8')


                except :
                    rating = "There is no Rating available"

                try :
                    commentHead = commentbox.div.div.div.p.text
                    commentHead.encode ( encoding = 'utf-8' )

                except :
                    commentHead = 'Comment Heading is not available'
                try :
                    comtag = commentbox.div.div.find_all ( "div" , { "class" : "" } )
                    custComment = comtag [ 0 ].div.text
                    custComment.encode(encoding='utf-8')
                except Exception as e :
                    print ( "Exception while creating dictionary: " , e )

                Rdict = dict ( Product = ProductName , Name = name , Rating = rating , CommentHead = commentHead ,
                               Comment = custComment )
                Reviews.append ( Rdict )
            return render_template ( "Result.html" , Reviews = Reviews [ 0 :(len ( Reviews ) - 1) ] )
        except Exception as e :
            print ( "The Exception message is: " , e )
            return "something went wrong"
        return render_template ( 'Result.html' )

    else :
        return render_template ( 'index.html' )


#port = int(os.getenv("PORT"))
if __name__ == "__main__" :
    #app.run(host='0.0.0.0', port=port)
    app.run ( debug = True )

import os
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
       #args = request.args
    #sel_level = args.get('level')
    #task = request.args.get("task")
    #returning back to index.html with all records from MySQL which are stored in variable data    
    return render_template("index.html")

@app.route('/record')
def record():      
    return render_template("record.html")


@app.route("/prediction", methods=["POST"])
#@app.route("/prediction")
def prediction():
    email=request.form['message'] 
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    model = pickle.load(open(dir_path+'/LogisticRegressionModel.pkl','rb'))
    cv=pickle.load(open(dir_path+'/vectorizer.pkl','rb'))
   
    data=[email]

    vec=cv.transform(data).toarray()
    result=model.predict(vec)

    #print (result)
  
    if result[0]==0:
        #not phishing 0
        message = ("This is a good email") #not_phishing 0	        		
    else:  
        #phishing 1
        message = ("This is a suspecious email, may be phishing email")
   
   
    print (message+" num="+str(result[0]))
    
    return render_template("index.html", msg=message, mail=email)
    
    

if __name__ == "__main__":
    app.run(debug=True)
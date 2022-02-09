from flask import Flask, jsonify, request
import db

app = Flask(__name__)

@app.route('/files', methods=['GET'])
def files():
   tags = request.args.get("tags")
   if tags is None: 
      tags = []
   else:
      tags = tags.split(",")    
   response = jsonify(db.list_files(tags))
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response



if __name__ == "__main__":
   app.run(debug=True, port=8000)
   

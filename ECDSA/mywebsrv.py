from flask import Flask
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cert',help='certificate')
parser.add_argument('--priv',help='private key')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    args = parser.parse_args()
    if args.cert and args.priv:
       print('HTTPS port=44330')
       app.run(ssl_context=(args.cert,args.priv),host='0.0.0.0',port=44330)
    else:
       print('HTTP port=8880')
       app.run(host='0.0.0.0',port=8880)

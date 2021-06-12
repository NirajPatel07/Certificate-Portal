from flask import Blueprint, app, flash, request, render_template, send_file
import hashlib
import datetime
from PIL import Image, ImageDraw, ImageFont
from .models import block_chain_data
from . import db
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

blockChain = Blueprint('blockChain', __name__)


class Block:
    def __init__(self, previous_block_hash, data, timestamp):
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = self.getHash()

    @staticmethod
    def createGenesisBlock():
        return Block("0", "0", datetime.datetime.now())

    def getHash(self):
        header_bin = (str(self.previous_block_hash) +
                       str(self.data) +
                       str(self.timestamp)).encode()

        innerHash = hashlib.sha256(header_bin).hexdigest().encode()
        outerHash = hashlib.sha256(innerHash).hexdigest()
        return outerHash


def GenerateCertificate(name, block, clg):
    font = ImageFont.truetype('arial.ttf', 80)
    font2 = ImageFont.truetype('arial.ttf', 50)
    font3 = ImageFont.truetype('arial.ttf', 40)

    img = Image.open(
        'C:/Users/asus/Desktop/Blockchain app/website/static/certificate.jpg')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(675, 480), text='{}'.format(name), fill=(0, 0, 0), font=font)
    draw.text(xy=(450, 810), text='{}'.format(clg), fill=(0, 0, 0), font=font2)
    draw.text(xy=(450, 1180), text='{}'.format(
        block), fill=(0, 0, 0), font=font3)
    img.save(
        'C:/Users/asus/Desktop/Blockchain app/website/static/SaveCertificate/{}.jpg'.format(name))


@blockChain.route('/downloadCertificate')
def downloadCertificate():
    name = request.args.get('my_var', None)
    file = 'C:/Users/asus/Desktop/Blockchain app/website/static/SaveCertificate/{}.jpg'.format(
        name)
    return send_file(file, as_attachment=True)


@blockChain.route('/block', methods=['GET', 'POST'])
def block():
    if request.method == "POST":
        fullName = request.form.get("fullName")
        clgName = request.form.get("clgName")
        BlockChainList = [Block.createGenesisBlock()]
        BlockChainList.append(
            Block(BlockChainList[-1].hash, fullName+clgName, datetime.datetime.now()))
        GenerateCertificate(fullName, BlockChainList[-1].hash, clgName)
        blockHash = BlockChainList[-1].hash

        new_data = block_chain_data(
            blockHash=blockHash, fullName=fullName, clgName=clgName)
        db.session.add(new_data)
        db.session.commit()

        data = {"Name": fullName,
              "College Name": clgName,
              "Block Hash": blockHash
              }
        return render_template("downloadCertificate.html", data=data)

    return render_template("createCertificate.html")


@blockChain.route('/verifyBlock', methods=['GET', 'POST'])
def verifyBlock():
    blockHash = request.form.get("block")

    blockCheck = block_chain_data.query.filter_by(blockHash=blockHash).first()
    if blockCheck:
        data={"Status":"Certificate Valid" ,"Block Hash": blockHash, "Name": blockCheck.fullName, "College Name": blockCheck.clgName}
        return render_template("verifiedDetails.html", data=data)       
    else:
        data={"Status":"Certificate Invalid"}
        return render_template("verifiedDetails.html", data=data) 
    

def sendEmail(email, name):
    
    fromaddr = "yourMail"
    toaddr = email
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "BlockSign Certificate"
    body = "Cetificate"

    msg.attach(MIMEText(body, 'plain'))

    filename = name+".jpg"
    attachment = open("C:/Users/asus/Desktop/Blockchain app/website/static/SaveCertificate/"+filename, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "YourPassword")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


@blockChain.route('/fileCertificate', methods=['GET', 'POST'])
def fileCertificate():
    if request.method == "POST":
        f = request.files['file']
        csv = pd.read_csv(f)
        data=[]
        for index,j in csv.iterrows():
            fullName = j['name']
            clgName = j['clg_name']
            email = j['email']
            
            BlockChainList = [Block.createGenesisBlock()]
            BlockChainList.append(
                Block(BlockChainList[-1].hash, fullName+clgName, datetime.datetime.now()))
            GenerateCertificate(fullName, BlockChainList[-1].hash, clgName)
            blockHash = BlockChainList[-1].hash 
            new_data = block_chain_data(
            blockHash=blockHash, fullName=fullName, clgName=clgName)
            db.session.add(new_data)
            db.session.commit()
            
            dictData = {"sr":index+1,
              "Name": fullName,
              "College Name": clgName,
              "Block Hash": blockHash
              }
            
            data.append(dictData)
            GenerateCertificate(fullName, blockHash, clgName)
            sendEmail(email, fullName)
            
            
        return render_template("showDetails.html", data=data)
  


    

   

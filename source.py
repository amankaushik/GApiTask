from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from ftplib import FTP
import configparser
import sys
import StringIO

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = ['csv']

class Product():
	def __init__(self, prodDetail):
		self.storeId = prodDetail[0]
		self.articleId = prodDetail[1]
		self.price = prodDetail[2]
		self.availability = prodDetail[3]
		self.stock = prodDetail[4] 
		self.validCode = self.checkValidCode(prodDetail)	

	def checkValidCode(self, prodDetail):
		if not prodDetail[0] or not prodDetail[1]:
			return 3
		if not prodDetail[2] or not prodDetail[3] or not prodDetail[4]:
			return 4
		else:
			return 1

def makeListofProducts(content):
		contentList = content.split("\n")
		prodList = []
		f = open('output.txt', 'w')
		#f.write(content)
		for prodDetail in contentList:
			f.write(str(prodDetail.split(',')))
			f.write("\n")
			prodList.append(Product(prodDetail.split(',')))
		f.close()
		return prodList	


def validateFileAndUpload(csVFile):
	if validate(csVFile):
		return {'isValid': 'Yes'}
		#uploadToFTP(csVFile)
	else:
		return {'Error': 'Wrong Format'}

def uploadToFTP(csVFile):
	config = configparser.ConfigParser()
	config.read('config.ini')
	ftpProperty = config['FTP']
	session = ftplib.FTP(ftpProperty['FTP_URL'],ftpProperty['FTP_USERNAME'],ftpProperty['FTP_PASSWORD'])
	fileFTP = open(ftpProperty['RESOURCE_DIRECTORY'] + csVFile.filename,'rb')                  
	session.storbinary(csVFile, fileFTP)
	fileFTP.close()      
	session.quit()

def validate(csVFile):
	content = csVFile.getvalue()
	prodList = makeListofProducts(content)
	for product in prodList:
		if product.validCode != 1:
			return False
	return True


class FileType():
	pass

class Validator():
	pass

class UploadFile(Resource):
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.ini')
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('filename', required = True, type = FileStorage, location = 'files')

	def post(self):
		args = self.parser.parse_args()
		#file = request.files['files']
		#return {'args': args}
		file = args['filename']
		fileExtension = file.filename.rsplit('.')[1].lower()
		# Check File Extension
		if fileExtension not in ALLOWED_EXTENSIONS:
			abort(404, message="File extension not allowed")

		csVFile = StringIO.StringIO()
		file.save(csVFile)

		return validateFileAndUpload(csVFile)
		

		#return {'filename': file.filename}
        # Upload to FTP
        #uploadToFTP(file)

	def get(self):
		return {'thisGet': 'working'}


class Check(Resource):
    def get(self):
        return {'this': 'working'}


api.add_resource(UploadFile, '/upload')

if __name__ == '__main__':
    app.run(debug = True)
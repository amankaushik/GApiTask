from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from ftplib import FTP
import configparser
import sys
import StringIO



sys.stdout = open('output.log', 'w')
sys.stdout = sys.__stdout__
app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = ['csv']




def validateFileAndUpload(csVFile):
	if validate(csVFile):
		#uploadToFTP(csVFile)
		pass
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
	#content = StringIO.StringIO()
	content = csVFile.getvalue()
	print content
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

		validateFileAndUpload(csVFile)
		

		return {'filename': file.filename}
        # Upload to FTP
        #uploadToFTP(file)

	def get(self):
		return {'thisGet': 'working'}


class Check(Resource):
    def get(self):
        return {'this': 'working'}


#api.add_resource(Check, '/')
api.add_resource(UploadFile, '/upload')
#parser = reqparse.RequestParser()
#parser.add_argument('filename', required = True, type = FileStorage)

if __name__ == '__main__':
    app.run(debug = True)
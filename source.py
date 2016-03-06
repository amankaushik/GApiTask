from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
from ftplib import FTP


app = Flask(__name__)
api = Api(app)

RESOURCE_DIRECTORY = '/amankaushik/'
ALLOWED_EXTENSIONS = ['csv']
FTP_URL = ''
FTP_USERNAME = ''
FTP_PASSWORD = ''

def uploadToFTP(file):
	ftp = FTP(FTP_URL)
	ftp.login()
	ftp.quit()
	pass

class FileType():
	pass

class Validator():
	pass

class UploadFile(Resource):
	def post(self):
		args = parser.parse_args()
		file = args['filename']
		fileExtension = file.filename.rsplit('.')[1].lower()
		# Check File Extension
		if fileExtension not in ALLOWED_EXTENSIONS:
			abort(404, message="File extension not allowed")

		csVFile = StringIO()
		file.save(csVFile)
		return {'filename': file.filename}
        # Upload to FTP
        #uploadToFTP(file)

	def get(self):
		return {'thisGet': 'working'}


class Check(Resource):
    def get(self):
        return {'this': 'working'}


api.add_resource(Check, '/')
api.add_resource(UploadFile, '/upload')
parser = reqparse.RequestParser()
parser.add_argument('filename', required = True, type = FileStorage)

if __name__ == '__main__':
    app.run(debug = True)
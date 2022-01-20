from flask import Flask
from service import user_service,ef_service,member_service, monthly_service
import os


app = Flask(__name__)

app.register_blueprint(ef_service.ef_apis)
app.register_blueprint(user_service.user_apis)
app.register_blueprint(member_service.member_apis)
app.register_blueprint(monthly_service.monthly_apis)

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=False)
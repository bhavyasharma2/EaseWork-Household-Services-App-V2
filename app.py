from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_caching import Cache
from Code.models import db, User, ServiceRequest
from celery import Celery
from flask_migrate import Migrate  
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_security import SQLAlchemyUserDatastore
from datetime import datetime
import os


app = Flask(__name__, static_folder='Code/static')
CORS(app, origins=["http://localhost:8080"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"])


app.config['SECURITY_PASSWORD_SALT'] = '0b9f4a6d3e8c7d21c53f1a9b2e6d5f08'  

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'household_services.db')


app.config.update(
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',  
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    broker_url='redis://localhost:6379/0',  
    result_backend='redis://localhost:6379/0'  
)


app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  



app.config['JWT_SECRET_KEY'] = 'VbKxPa3uV-v8wHZdtiP4iTLv88TO0QG7ChR9mKH-P-RcM-Mv2g6P1pINk7z3HZtR'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False 

jwt = JWTManager(app)


cache = Cache(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bhavya22shar@gmail.com'
app.config['MAIL_PASSWORD'] = 'arhc ihwh fgph tfbo'
app.config['MAIL_DEFAULT_SENDER'] = 'bhavya22shar@gmail.com'
mail = Mail(app)


from Code.models import db 
db.init_app(app) 

from Code.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

migrate = Migrate(app, db)  


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["broker_url"],
        backend=app.config["result_backend"],
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        "send-daily-reminders-every-minute": {
            "task": "Code.app.send_daily_reminders",
            "schedule": 60.0,  
        },
        "send-monthly-reports-every-minute": {
            "task": "Code.app.send_monthly_activity_report",
            "schedule": 60.0,  
        },
    }
    return celery


celery = make_celery(app)


from Code.admin_dashboard_routes import admin_dashboard_bp
from Code.customer_dashboard_routes import customer_dashboard_bp
from Code.professional_dashboard_routes import professional_dashboard_bp
from Code.login_and_logout_routes import login_and_logout_bp  
from Code.register_routes import register_bp


app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
app.register_blueprint(customer_dashboard_bp, url_prefix='/customers')
app.register_blueprint(professional_dashboard_bp, url_prefix='/professional')
app.register_blueprint(login_and_logout_bp, url_prefix='/auth')  
app.register_blueprint(register_bp, url_prefix='/register')


@app.route('/')
def home():
    return "Flask API is running. Please access the appropriate routes."


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.email), 200

@app.before_request
def before_first_request():
    from Code.models import init_db
    init_db()


@celery.task
def send_daily_reminders():
    with app.app_context():
        from Code.models import db, User, ServiceRequest
        try:
            professionals = (
                db.session.query(User)
                .join(ServiceRequest, User.id == ServiceRequest.professional_id)
                .filter(User.role == "professional", ServiceRequest.status == "Pending")
                .distinct()
            )

            if professionals.count() == 0:
                print("No pending requests found.")
                return

            summary_message = "Daily Reminder: Pending Service Requests\n\n"
            for professional in professionals:
                summary_message += f"Professional: {professional.full_name} (Email: {professional.email})\n"
                pending_requests = ServiceRequest.query.filter_by(
                professional_id=professional.id, status="Pending"
                ).all()
                for request in pending_requests:
                    summary_message += f"- Request ID: {request.id}, Service: {request.service.name}, Requested Date: {request.requested_date}\n"
                summary_message += "\n"

            msg = Message(
                subject="Daily Summary: Pending Service Requests",
                recipients=["bhavya22shar@gmail.com"],
                body=summary_message,
            )
            mail.send(msg)
            print("Reminder email sent successfully to bhavya22shar@gmail.com")

        except Exception as e:
            print(f"Error in send_daily_reminders task: {e}")

@celery.task
def send_monthly_activity_report():
    with app.app_context():
        from Code.models import ServiceRequest
        today = datetime.today()
        start_date = today.replace(day=1)
        end_date = (
            today.replace(month=today.month + 1, day=1)
            if today.month < 12
            else today.replace(year=today.year + 1, month=1, day=1)
        )

        services_requested = ServiceRequest.query.filter(
            ServiceRequest.requested_date >= start_date,
            ServiceRequest.requested_date < end_date,
        ).count()
        services_closed = ServiceRequest.query.filter(
            ServiceRequest.completion_date >= start_date,
            ServiceRequest.completion_date < end_date,
        ).count()

        html_report = render_template_string(
            """
            <h2>Monthly Activity Report</h2>
            <p><strong>Services Requested:</strong> {{ services_requested }}</p>
            <p><strong>Services Closed:</strong> {{ services_closed }}</p>
            """,
            services_requested=services_requested,
            services_closed=services_closed,
        )

        msg = Message(
            subject="Monthly Activity Report",
            recipients=["bhavya22shar@gmail.com"],
            html=html_report,
        )
        mail.send(msg)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, send_daily_reminders.s(), name="Send reminders every 1 mins")
    sender.add_periodic_task(60.0, send_monthly_activity_report.s(), name="Send activity report every 1 mins")



if __name__ == '__main__':
    app.run(debug=True)







from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, default=True)
    full_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    pin_code = db.Column(db.String(20))  
    mobile_number = db.Column(db.String(20))
    experience = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0)
    documents_path = db.Column(db.String(255))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))
    is_blocked = db.Column(db.Boolean, default=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)

    service = relationship('Service', backref='professionals')
    service_type = relationship('ServiceType', backref='professionals')
    
    customer_requests = relationship('ServiceRequest', 
                                     foreign_keys='ServiceRequest.customer_id',
                                     back_populates='customer')
    
    professional_requests = relationship('ServiceRequest', 
                                         foreign_keys='ServiceRequest.professional_id',
                                         back_populates='professional')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.email}>'


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    service_types = relationship('ServiceType', backref='service', lazy=True, cascade='all, delete-orphan')


class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    type_name = db.Column(db.String(255), nullable=False)


class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=True)  
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requested_date = db.Column(db.String(50), nullable=False)
    completion_date = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Pending')

    customer = relationship('User', foreign_keys=[customer_id], back_populates='customer_requests')

    professional = relationship('User', foreign_keys=[professional_id], back_populates='professional_requests')

    service = relationship('Service', backref='service_requests', lazy=True)


class PendingRegistration(db.Model):
    __tablename__ = 'pending_registrations'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(20), nullable=False)  
    mobile_number = db.Column(db.String(20), nullable=False)
    documents_path = db.Column(db.String(255))


def init_db():
    db.create_all()

    admin_role = Role(name='admin')
    customer_role = Role(name='customer')
    professional_role = Role(name='professional')

    if not Role.query.filter_by(name='admin').first():
        db.session.add(admin_role)
    if not Role.query.filter_by(name='customer').first():
        db.session.add(customer_role)
    if not Role.query.filter_by(name='professional').first():
        db.session.add(professional_role)

    db.session.commit()

    if not Service.query.first():  
        services = [
            Service(name='Cleaning Services', price=1000, time_required=2, description='Professional cleaning and maintenance.'),
            Service(name='Plumbing', price=500, time_required=1, description='Plumbing repair and maintenance.'),
            Service(name='Electrical Work', price=600, time_required=1, description='Installation and repair of electrical systems.')
        ]
        db.session.add_all(services)
        db.session.commit()

    if not ServiceType.query.first():
        service_types = [
            ServiceType(service_id=1, type_name='Carpet Cleaning'),
            ServiceType(service_id=1, type_name='Kitchen Cleaning'),
            ServiceType(service_id=2, type_name='Leak Repair'),
            ServiceType(service_id=2, type_name='Pipe Installation'),
            ServiceType(service_id=3, type_name='Fixture Installation'),
            ServiceType(service_id=3, type_name='Wiring Repair')
        ]
        db.session.add_all(service_types)
        db.session.commit()

    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(email='admin@example.com', role='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
    
    if not User.query.filter_by(email='iambhavyaa@gmail.com').first():
        customer1 = User(email='iambhavyaa@gmail.com', role='customer', full_name='Bhavya Sharma', address='123 Main St, City', pin_code='12345', mobile_number='9876543210')
        customer1.set_password('customer1')
        db.session.add(customer1)
    
    if not User.query.filter_by(email='customer2@example.com').first():
        customer2 = User(email='customer2@example.com', role='customer', full_name='Krishna Pareek', address='456 Elm St, City', pin_code='54321', mobile_number='9876543211')
        customer2.set_password('customer2')
        db.session.add(customer2)
    
    if not User.query.filter_by(email='21f2000707@ds.study.iitm.ac.in').first():
        professional1 = User(email='21f2000707@ds.study.iitm.ac.in', role='professional', full_name='Bhanu Pratap', address='789 Oak St, City', pin_code='12345', mobile_number='9876543212', experience=5, rating=4, service_id=1, service_type_id=1)
        professional1.set_password('prof1')
        db.session.add(professional1)
    
    if not User.query.filter_by(email='professional2@example.com').first():
        professional2 = User(email='professional2@example.com', role='professional', full_name='Raghu Tank', address='101 Pine St, City', pin_code='54321', mobile_number='9876543213', experience=7, rating=5, service_id=2, service_type_id=2)
        professional2.set_password('prof2')
        db.session.add(professional2)

    db.session.commit()



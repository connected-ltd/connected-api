from app import db
from app.numbers.model import *

class Areas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    numbers = db.relationship('Numbers', backref='area')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None):
        self.name = name or self.name
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_all_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_numbers_per_area(cls):
        result = db.session.query(
            Areas.name.label('area_name'),
            func.coalesce(func.count(Numbers.id), 0).label('number_count')  # Handle zero counts
        ).outerjoin(  # Use outerjoin to include areas without any numbers
            Numbers, Numbers.area_id == Areas.id
        ).filter(
            Areas.is_deleted == False  # Don't need to filter Numbers here as we'll handle NULL counts
        ).group_by(Areas.id).all()

        return [{'area_name': area_name, 'number_count': number_count} for area_name, number_count in result]
    
    @classmethod
    def create(cls, name):
        areas = cls(name=name)
        areas.save()
        return areas
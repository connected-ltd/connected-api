from app import db
from sqlalchemy import func

class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True, nullable=False)
    language = db.Column(db.String, nullable=False, default="english")
    is_set = db.Column(db.Boolean, default=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, number=None, language=None, area_id=None, is_set=False):
        self.number = number or self.number
        self.language = language or self.language
        self.area_id = area_id or self.area_id
        self.is_set = is_set or self.is_set
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
    def get_all_number_only(cls):
        return cls.query.with_entities(cls.number).filter_by(is_deleted=False).all()
    
    @classmethod
    def get_all_by_area_id(cls, area_id):
        return cls.query.filter_by(area_id=area_id, is_deleted=False).all()
    
    @classmethod
    def get_all_numbers_only_by_area_id(cls, area_id):
        return cls.query.with_entities(cls.number).filter_by(area_id=area_id, is_deleted=False).all()
    
    @classmethod
    def get_by_phone(cls, number):
        # print(number)
        return cls.query.filter(cls.number.ilike(f"%{number[1:]}%")).first()
    
    @classmethod
    def get_language_by_number(cls, number):
        user = cls.query.filter_by(number=number, is_deleted=False).first()
        return user.language if user else 'english'
    
    @classmethod
    def check_if_number_exists(cls, number):
        return cls.query.filter_by(number=number).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_numbers_stats(cls):
        stats = db.session.query(
            cls.language,
            func.count(cls.id).label('count')
        ).filter_by(is_deleted=False).group_by(cls.language).all()

        # Create a dictionary with all languages, defaulting to 0
        all_stats = {'english': 0, 'hausa': 0, 'yoruba': 0, 'igbo': 0}

        # Update the counts from the query results
        for lang, count in stats:
            all_stats[lang.lower()] = count

        total = sum(all_stats.values())

        return {
            'english': all_stats['english'],
            'hausa': all_stats['hausa'],
            'yoruba': all_stats['yoruba'],
            'igbo': all_stats['igbo'],
            'total': total
        }
    
    @classmethod
    def create(cls, number, language, area_id):
        numbers = cls(number=number, language=language, area_id=area_id, is_set=True)
        numbers.save()
        return numbers
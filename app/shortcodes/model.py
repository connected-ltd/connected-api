from app import db
from app.files.model import *
from app.shortcode_files.model import *
from app.user.model import *

class Shortcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, shortcode=None, user_id=None):
        self.shortcode = shortcode or self.shortcode
        self.user_id = user_id or self.user_id
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
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).first()
    
    @classmethod
    def get_shortcode_only_by_id(cls, id):
        return cls.query.with_entities(cls.shortcode).filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_files_by_shortcode(cls, shortcode):
        return db.session.query(cls, Shortcode_Files, Files).\
            join(Shortcode_Files, cls.id == Shortcode_Files.shortcode_id).\
            join(Files, Shortcode_Files.file_id == Files.id).\
            filter(cls.shortcode == shortcode,
                   cls.is_deleted == False,
                   Shortcode_Files.is_deleted == False,
                   Files.is_deleted == False).\
            all()
    
    @classmethod
    def get_user_by_shortcode(cls, shortcode):
        return db.session.query(User).join(cls, cls.user_id == User.id).filter(
            cls.shortcode == shortcode,
            cls.is_deleted == False
        ).first()
        
    @classmethod
    def get_user_id_by_shortcode(cls, shortcode):
        result = cls.query.with_entities(cls.user_id).filter_by(
            shortcode=shortcode,
            is_deleted=False
        ).first()
        return result[0] if result else None
    
    @classmethod
    def get_username_by_shortcode(cls, shortcode):
        result = db.session.query(User.username).\
            join(cls, User.id == cls.user_id).\
            filter(cls.shortcode == shortcode, cls.is_deleted == False).\
            first()
        return result[0] if result else None
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, shortcode, user_id):
        shortcodes = cls(shortcode=shortcode, user_id=user_id)
        shortcodes.save()
        return shortcodes
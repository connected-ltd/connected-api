from app import db

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
    def get_shortcode_only_by_id(cls, id):
        return cls.query.with_entities(cls.shortcode).filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, shortcode, user_id):
        shortcodes = cls(shortcode=shortcode, user_id=user_id)
        shortcodes.save()
        return shortcodes
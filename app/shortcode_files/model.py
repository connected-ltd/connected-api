from app import db

class Shortcode_Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    shortcode_id = db.Column(db.Integer, db.ForeignKey('shortcodes.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, shortcode_id=None, file_id=None):
        self.shortcode_id = shortcode_id or self.shortcode_id
        self.file_id = file_id or self.file_id
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
    def create(cls, shortcode_id, file_id):
        shortcode_files = cls(shortcode_id=shortcode_id, file_id=file_id)
        shortcode_files.save()
        return shortcode_files
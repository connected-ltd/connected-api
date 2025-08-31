from app import db

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    shortcode_id = db.Column(db.Integer, db.ForeignKey('shortcodes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, message=None, shortcode_id=None, user_id=None, area_id=None):
        self.message = message or self.message
        self.shortcode_id = shortcode_id or self.shortcode_id
        self.user_id = user_id or self.user_id
        self.area_id = area_id or self.area_id
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
        from app.shortcodes.model import Shortcodes
        from app.areas.model import Areas
        from sqlalchemy.orm import aliased

        Shortcode = aliased(Shortcodes)
        Area = aliased(Areas)

        results = db.session.query(
            cls,
            Shortcode.shortcode,
            Area.name
        ).join(
            Shortcode, cls.shortcode_id == Shortcode.id
        ).join(
            Area, cls.area_id == Area.id
        ).filter(
            cls.is_deleted == False
        ).all()

        data = []
        for msg_obj, shortcode, area in results:
            msg_dict = {
                'id': msg_obj.id,
                'message': msg_obj.message,
                'created_at': msg_obj.created_at,
                'updated_at': msg_obj.updated_at,
                'shortcode': shortcode,
                'area': area
            }
            data.append(msg_dict)
        return data
    
    @classmethod
    def create(cls, message, shortcode_id, user_id, area_id):
        messages = cls(message=message, shortcode_id=shortcode_id, user_id=user_id, area_id=area_id)
        messages.save()
        return messages
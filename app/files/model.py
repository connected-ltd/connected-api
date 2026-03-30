from app import db

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    file_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shortcode_id = db.Column(db.Integer, db.ForeignKey('shortcodes.id'), nullable=True) # NOTE: Can either be whatsapp number id or shortcode id
    whatsapp_number_id = db.Column(db.Integer, db.ForeignKey('whatsapp__number.id'), nullable=True) # NOTE: Can either be whatsapp number id or shortcode id
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, user_id=None):
        self.name = name or self.name
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
    def get_id_by_name(cls, name):
        return cls.query.filter_by(name=name, is_deleted=False).with_entities(cls.id).first()
    

    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()

    @classmethod
    def get_all_with_shortcodes_and_whatsapp(cls):
        from app.shortcodes.model import Shortcodes
        from app.whatsapp_number.model import Whatsapp_Number
        from app.user.model import User
        from sqlalchemy.orm import aliased

        Shortcode = aliased(Shortcodes)
        Whatsapp = aliased(Whatsapp_Number)
        UserModel = aliased(User)

        results = db.session.query(
            cls,
            Shortcode.shortcode,
            Whatsapp.number
        ).join(
            UserModel, cls.user_id == UserModel.id
        ).outerjoin(
            Shortcode, Shortcode.user_id == UserModel.id
        ).outerjoin(
            Whatsapp, Whatsapp.user_id == UserModel.id
        ).filter(
            cls.is_deleted == False
        ).all()

        data = []
        for file_obj, shortcode, whatsapp_number in results:
            file_dict = {
                'id': file_obj.id,
                'name': file_obj.name,
                'user_id': file_obj.user_id,
                'created_at': file_obj.created_at,
                'updated_at': file_obj.updated_at,
                'shortcode': shortcode,
                'whatsapp_number': whatsapp_number,
                'file_url': file_obj.file_url
            }
            data.append(file_dict)
        return data
    
    # TODO: Redo the above implementation
    
    @classmethod
    def has_files(cls, shortcode_id):
        return cls.query.filter_by(
            shortcode_id=shortcode_id, 
            is_deleted=False
        ).first() is not None

    @classmethod
    def create(cls, name, user_id, file_url, shortcode_id=None, whatsapp_number_id=None):
        if (shortcode_id or whatsapp_number_id) and file_url:
            file_obj = cls(
                name=name, 
                user_id=user_id, 
                file_url=file_url,
                shortcode_id=shortcode_id, 
                whatsapp_number_id=whatsapp_number_id
            )
            file_obj.save()
            return file_obj
        return None


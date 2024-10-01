from app import db

class Ussd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String)
    stage = db.Column(db.String)
    previous = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, session_id=None, stage=None, previous=None):
        self.session_id = session_id or self.session_id
        self.stage = stage or self.stage
        self.previous = previous or self.previous
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
    def get_by_session_id(cls, session_id):
        return cls.query.filter_by(session_id=session_id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create_or_update(cls, session_id, stage, previous=None):
        dispatch = cls.get_by_session_id(session_id)
        if not dispatch:
            dispatch = cls(session_id=session_id, stage=stage, previous=previous)
            dispatch.save()
        else:
            dispatch.update(stage=stage, previous=previous)
        return dispatch
    
    @classmethod
    def create(cls, session_id, stage, previous):
        ussd = cls(session_id=session_id, stage=stage, previous=previous)
        ussd.save()
        return ussd
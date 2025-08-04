from app import db
from datetime import datetime

class QueryAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    source = db.Column(db.String, nullable=True)  # Source of the query (ussd, whatsapp, etc.)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Relationships
    keywords = db.relationship('QueryKeyword', backref='query', lazy=True, cascade="all, delete-orphan")
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all(cls, limit=100, offset=0):
        return cls.query.order_by(cls.created_at.desc()).limit(limit).offset(offset).all()
    
    @classmethod
    def get_by_user(cls, user_id, limit=100, offset=0):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).offset(offset).all()
    
    @classmethod
    def get_by_timerange(cls, start_date, end_date):
        return cls.query.filter(cls.created_at.between(start_date, end_date)).all()
    
    @classmethod
    def create(cls, query_text, user_id=None, source=None):
        query = cls(query_text=query_text, user_id=user_id, source=source)
        query.save()
        return query


class QueryKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)  # Subject or category
    relevance_score = db.Column(db.Float, nullable=True)  # Optional score from 0-1
    query_id = db.Column(db.Integer, db.ForeignKey('query_analytics.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_top_keywords(cls, limit=10, timeframe=None):
        """Get the most frequently occurring keywords"""
        query = db.session.query(
            cls.keyword, 
            db.func.count(cls.id).label('count')
        ).group_by(cls.keyword).order_by(db.desc('count'))
        
        if timeframe:
            # If timeframe is specified, add time filter
            start_date = datetime.now() - timeframe
            query = query.join(QueryAnalytics).filter(QueryAnalytics.created_at >= start_date)
            
        return query.limit(limit).all()
    
    @classmethod
    def get_top_categories(cls, limit=10):
        """Get the most frequently occurring categories"""
        return db.session.query(
            cls.category, 
            db.func.count(cls.id).label('count')
        ).filter(cls.category != None).group_by(cls.category).order_by(db.desc('count')).limit(limit).all()
    
    @classmethod
    def create(cls, keyword, query_id, category=None, relevance_score=None):
        keyword_obj = cls(keyword=keyword, query_id=query_id, category=category, relevance_score=relevance_score)
        keyword_obj.save()
        return keyword_obj 
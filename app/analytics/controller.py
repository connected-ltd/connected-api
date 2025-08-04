from flask import Blueprint, jsonify, request
from app.analytics.service import AnalyticsService
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.route_guard import admin_required

# Create a blueprint for analytics routes
bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/keywords', methods=['GET'])
@jwt_required()
@admin_required()
def get_top_keywords():
    """Get the most frequently used keywords"""
    days = request.args.get('days', 30, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    keywords = AnalyticsService.get_top_keywords(days=days, limit=limit)
    
    result = []
    for keyword, count in keywords:
        result.append({
            'keyword': keyword,
            'count': count
        })
    
    return jsonify(result)

@bp.route('/categories', methods=['GET'])
@jwt_required()
@admin_required()
def get_top_categories():
    """Get the most common query categories"""
    limit = request.args.get('limit', 10, type=int)
    
    categories = AnalyticsService.get_top_categories(limit=limit)
    
    result = []
    for category, count in categories:
        result.append({
            'category': category,
            'count': count
        })
    
    return jsonify(result)

@bp.route('/queries', methods=['GET'])
@jwt_required()
@admin_required()
def get_recent_queries():
    """Get recent queries with pagination"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Parse date parameters if provided
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Set end date to end of day
            end_date = end_date.replace(hour=23, minute=59, second=59)
            
            queries = AnalyticsService.get_queries_by_timerange(start_date, end_date, limit, offset)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        # Default to last 30 days if no dates provided
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        queries = AnalyticsService.get_queries_by_timerange(start_date, end_date, limit, offset)
    
    result = []
    for query in queries:
        # Get keywords for this query
        keywords = [{'keyword': kw.keyword, 'category': kw.category} for kw in query.keywords]
        
        result.append({
            'id': query.id,
            'text': query.query_text,
            'user_id': query.user_id,
            'source': query.source,
            'created_at': query.created_at.isoformat(),
            'keywords': keywords
        })
    
    return jsonify(result)

@bp.route('/trends', methods=['GET'])
@jwt_required()
@admin_required()
def get_query_trends():
    """Get query trends over time"""
    days = request.args.get('days', 30, type=int)
    interval = request.args.get('interval', 'day')
    
    # Validate interval
    if interval not in ['day', 'week', 'month']:
        return jsonify({'error': 'Invalid interval. Use day, week, or month'}), 400
    
    trends = AnalyticsService.get_query_trend(days=days, interval=interval)
    
    return jsonify(trends)

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required()
def get_dashboard():
    """Get a summary dashboard of analytics data"""
    # Get query count for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    queries = AnalyticsService.get_queries_by_timerange(start_date, end_date)
    
    # Get top keywords
    top_keywords = AnalyticsService.get_top_keywords(days=30, limit=5)
    keywords_data = [{'keyword': kw, 'count': count} for kw, count in top_keywords]
    
    # Get top categories
    top_categories = AnalyticsService.get_top_categories(limit=5)
    categories_data = [{'category': cat, 'count': count} for cat, count in top_categories]
    
    # Get daily query trend for the past week
    daily_trends = AnalyticsService.get_query_trend(days=7, interval='day')
    
    dashboard = {
        'total_queries_30d': len(queries),
        'top_keywords': keywords_data,
        'top_categories': categories_data,
        'daily_trends': daily_trends
    }
    
    return jsonify(dashboard) 
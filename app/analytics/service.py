import os
from app.analytics.model import QueryAnalytics, QueryKeyword
from langchain_openai import ChatOpenAI
import json
from datetime import datetime, timedelta

class AnalyticsService:
    @staticmethod
    def process_query(query_text, user_id=None, source=None):
        """
        Process a user query and extract keywords/subjects
        """
        # Store the query
        query = QueryAnalytics.create(query_text, user_id, source)
        
        # Extract keywords and categories using OpenAI
        keywords = AnalyticsService._extract_keywords(query_text)
        
        # Store each keyword
        for kw in keywords:
            QueryKeyword.create(
                keyword=kw['keyword'],
                query_id=query.id,
                category=kw.get('category'),
                relevance_score=kw.get('relevance_score')
            )
            
        return query
    
    @staticmethod
    def _extract_keywords(query_text):
        """
        Use OpenAI to extract keywords and categories from the query
        """
        try:
            # Initialize the ChatOpenAI client
            llm = ChatOpenAI(
                openai_api_key=os.environ.get('OPENAI_API_KEY'),
                model_name='gpt-4o-mini',
                temperature=0.0
            )
            
            # Prompt for extracting keywords
            system_prompt = """
            You are an AI specialized in analyzing user queries and extracting keywords and topics.
            For the given user query, extract:
            1. 2-5 most relevant keywords
            2. The general category or subject the query belongs to
            3. A relevance score (0-1) for each keyword
            
            Return the data as a JSON array with this format:
            [
                {"keyword": "word1", "category": "subject", "relevance_score": 0.9},
                {"keyword": "word2", "category": "subject", "relevance_score": 0.8}
            ]
            
            Only respond with the JSON. No additional text.
            """
            
            # Send the query to OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query_text}
            ]
            
            response = llm.invoke(messages)
            
            # Parse the JSON response
            content = response.content
            
            # Extract the JSON part if there's additional text
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
                
            return json.loads(content)
            
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            # Return a basic fallback if OpenAI fails
            return [{"keyword": query_text.split()[0] if query_text.split() else "unknown", "category": "general"}]
    
    @staticmethod
    def get_top_keywords(days=30, limit=10):
        """
        Get the most common keywords from the past X days
        """
        timeframe = timedelta(days=days)
        return QueryKeyword.get_top_keywords(limit=limit, timeframe=timeframe)
    
    @staticmethod
    def get_top_categories(limit=10):
        """
        Get the most common categories
        """
        return QueryKeyword.get_top_categories(limit=limit)
    
    @staticmethod
    def get_queries_by_timerange(start_date, end_date, limit=100, offset=0):
        """
        Get queries within a specific time range
        """
        queries = QueryAnalytics.get_by_timerange(start_date, end_date)
        return queries[:limit] if len(queries) > limit else queries
    
    @staticmethod
    def get_query_trend(days=30, interval="day"):
        """
        Get query counts grouped by time interval (day, week, month)
        """
        start_date = datetime.now() - timedelta(days=days)
        
        if interval == "day":
            format_str = "%Y-%m-%d"
            group_func = lambda d: d.strftime(format_str)
        elif interval == "week":
            format_str = "%Y-%U"  # Year and week number
            group_func = lambda d: d.strftime(format_str)
        elif interval == "month":
            format_str = "%Y-%m"
            group_func = lambda d: d.strftime(format_str)
        else:
            format_str = "%Y-%m-%d"
            group_func = lambda d: d.strftime(format_str)
            
        # Get all queries in the time range
        queries = QueryAnalytics.query.filter(QueryAnalytics.created_at >= start_date).all()
        
        # Group by the chosen interval
        trends = {}
        for query in queries:
            key = group_func(query.created_at)
            if key not in trends:
                trends[key] = 0
            trends[key] += 1
            
        # Convert to list of dicts for easier frontend consumption
        result = [{"date": k, "count": v} for k, v in trends.items()]
        result.sort(key=lambda x: x["date"])
        
        return result 
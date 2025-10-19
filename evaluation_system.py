import time
from typing import Dict, List
from datetime import datetime
from collections import deque

class EvaluationSystem:
    def __init__(self):
        self.metrics = {
            'response_times': deque(maxlen=100),
            'query_count': 0,
            'accuracy_scores': deque(maxlen=100),
            'user_feedback': deque(maxlen=100)
        }
        self.session_start = datetime.now()
        
    def start_query(self) -> float:
        return time.time()
    
    def end_query(self, start_time: float) -> float:
        response_time = time.time() - start_time
        self.metrics['response_times'].append(response_time)
        self.metrics['query_count'] += 1
        return response_time
    
    def calculate_ciq(self, response_time: float, accuracy: float, actionability: float) -> float:
        speed_score = max(0, 100 - (response_time * 10))
        
        ciq = (
            speed_score * 0.3 +
            accuracy * 0.4 +
            actionability * 0.3
        )
        
        return round(ciq, 2)
    
    def add_feedback(self, rating: int, comment: str = ""):
        self.metrics['user_feedback'].append({
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        })
    
    def calculate_speedup(self, ai_time: float, manual_time: float = 300) -> float:
        return round(manual_time / ai_time, 2)
    
    def get_performance_summary(self) -> Dict:
        if not self.metrics['response_times']:
            return {'status': 'No data yet'}
        
        response_times = list(self.metrics['response_times'])
        avg_response = sum(response_times) / len(response_times)
        
        manual_baseline = 300
        speedup = self.calculate_speedup(avg_response, manual_baseline)
        
        feedback_ratings = [f['rating'] for f in self.metrics['user_feedback']]
        avg_rating = sum(feedback_ratings) / len(feedback_ratings) if feedback_ratings else 0
        
        return {
            'total_queries': self.metrics['query_count'],
            'avg_response_time': round(avg_response, 2),
            'min_response_time': round(min(response_times), 2),
            'max_response_time': round(max(response_times), 2),
            'speedup_vs_manual': speedup,
            'avg_user_rating': round(avg_rating, 2),
            'session_duration': str(datetime.now() - self.session_start).split('.')[0]
        }
    
    def get_real_time_metrics(self) -> Dict:
        recent_times = list(self.metrics['response_times'])[-10:] if self.metrics['response_times'] else []
        
        if recent_times:
            recent_avg = sum(recent_times) / len(recent_times)
        else:
            recent_avg = 0
        
        time_saved = 0
        if self.metrics['query_count'] > 0 and recent_avg > 0:
            time_saved = round((300 - recent_avg) * self.metrics['query_count'] / 60, 1)
        
        return {
            'last_10_avg_response': round(recent_avg, 2),
            'queries_this_session': self.metrics['query_count'],
            'estimated_time_saved': max(0, time_saved)
        }
    
    def evaluate_answer_quality(self, answer: str, has_metrics: bool, has_recommendations: bool) -> Dict:
        quality_score = 0
        
        if len(answer) > 50:
            quality_score += 25
        
        if has_metrics:
            quality_score += 35
        
        if has_recommendations:
            quality_score += 30
        
        if any(word in answer.lower() for word in ['however', 'although', 'consider', 'recommend']):
            quality_score += 10
        
        return {
            'quality_score': min(100, quality_score),
            'has_metrics': has_metrics,
            'has_recommendations': has_recommendations,
            'word_count': len(answer.split())
        }
    
    def reset_session(self):
        self.metrics = {
            'response_times': deque(maxlen=100),
            'query_count': 0,
            'accuracy_scores': deque(maxlen=100),
            'user_feedback': deque(maxlen=100)
        }
        self.session_start = datetime.now()
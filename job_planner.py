"""
PRAXIS - Job Planner
Where Thought Becomes Action
"""

from powerbi_connector import PowerBIConnector
from decision_engine import DecisionEngine
from llm_client import LLMClient
from evaluation_system import EvaluationSystem
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

Path('data').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

log_filename = f"logs/job_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class JobPlanner:
    def __init__(self):
        logger.info("="*60)
        logger.info("PRAXIS - Where Thought Becomes Action")
        logger.info("Team: 404 Port Not Found")
        logger.info("="*60)
        
        self.pbi = PowerBIConnector()
        self.engine = DecisionEngine()
        self.llm = LLMClient()
        self.eval_sys = EvaluationSystem()
    
    def plan_operations(self):
        logger.info("Starting job planning process")
        
        start_time = self.eval_sys.start_query()
        logger.info("Fetching vessel data from Power BI")
        df = self.pbi.get_operator_data()
        fetch_time = self.eval_sys.end_query(start_time)
        
        logger.info(f"Retrieved {len(df)} vessel records in {fetch_time:.2f}s")
        
        logger.info("Running decision engine analysis")
        start_time = self.eval_sys.start_query()
        analyzed_df = self.engine.analyze_dataframe(df)
        analysis_time = self.eval_sys.end_query(start_time)
        
        logger.info(f"Analysis completed in {analysis_time:.2f}s")
        logger.info(f"Average DIS Score: {analyzed_df['DIS_Score'].mean():.2f}")
        logger.info(f"Average Time Efficiency: {analyzed_df['Time_Efficiency'].mean():.2f}")
        logger.info(f"Average Cost Efficiency: {analyzed_df['Cost_Efficiency'].mean():.2f}")
        
        logger.info("Identifying top priorities")
        priorities = analyzed_df.nlargest(20, 'DIS_Score')
        logger.info(f"Top priority vessels identified: {len(priorities)}")
        
        logger.info("Generating AI recommendations")
        start_time = self.eval_sys.start_query()
        recommendations = self.engine.generate_recommendations(df)
        rec_time = self.eval_sys.end_query(start_time)
        
        logger.info(f"Recommendations generated in {rec_time:.2f}s")
        for i, rec in enumerate(recommendations, 1):
            logger.info(f"  Recommendation {i}: {rec}")
        
        return {
            'analyzed_data': analyzed_df,
            'priorities': priorities,
            'recommendations': recommendations,
            'metrics': {
                'fetch_time': fetch_time,
                'analysis_time': analysis_time,
                'rec_time': rec_time,
                'total_time': fetch_time + analysis_time + rec_time
            }
        }
    
    def export_results(self, results):
        logger.info("Exporting results to data/output.csv")
        
        analyzed_df = results['analyzed_data']
        
        logger.info(f"Available columns: {list(analyzed_df.columns)}")
        
        must_have_cols = [
            'DIS_Score', 'Time_Efficiency', 'Cost_Efficiency',
            'Environmental_Score', 'Risk_Score'
        ]
        
        optional_cols = [
            'Operator', 'Vessel', 'Service', 'BU',
            'Wait Time (Hours): ATB-BTR',
            'Arrival Accuracy (Final BTR)',
            'Bunker Saved (USD)',
            'Carbon Abatement (Tonnes)'
        ]
        
        export_cols = []
        
        for col in optional_cols:
            if col in analyzed_df.columns:
                export_cols.append(col)
        
        export_cols.extend(must_have_cols)
        
        output_df = analyzed_df[export_cols].copy()
        output_df = output_df.sort_values('DIS_Score', ascending=False)
        output_df.to_csv('data/output.csv', index=False)
        
        logger.info(f"Exported {len(output_df)} records to data/output.csv")
        logger.info(f"Columns included: {len(export_cols)} columns")
    
    def show_performance_comparison(self, metrics):
        logger.info("="*60)
        logger.info("PERFORMANCE COMPARISON: AI vs MANUAL")
        logger.info("="*60)
        
        total_ai_time = metrics['total_time']
        manual_time = 300
        
        logger.info(f"AI Processing Time: {total_ai_time:.2f} seconds")
        logger.info(f"  - Data Fetch: {metrics['fetch_time']:.2f}s")
        logger.info(f"  - Analysis: {metrics['analysis_time']:.2f}s")
        logger.info(f"  - Recommendations: {metrics['rec_time']:.2f}s")
        logger.info("")
        logger.info(f"Manual Processing Time (estimated): {manual_time:.0f} seconds")
        logger.info(f"  - Manual dashboard navigation: ~60s")
        logger.info(f"  - Data interpretation: ~120s")
        logger.info(f"  - Decision making: ~120s")
        logger.info("")
        
        speedup = manual_time / total_ai_time
        time_saved = manual_time - total_ai_time
        
        logger.info(f"SPEEDUP: {speedup:.1f}x faster")
        logger.info(f"TIME SAVED: {time_saved:.1f} seconds ({time_saved/60:.1f} minutes)")
        logger.info("")
        
        performance_summary = self.eval_sys.get_performance_summary()
        logger.info("Session Performance Metrics:")
        logger.info(f"  - Total queries processed: {performance_summary['total_queries']}")
        logger.info(f"  - Average response time: {performance_summary['avg_response_time']:.2f}s")
        if performance_summary['total_queries'] > 0:
            logger.info(f"  - Min response time: {performance_summary['min_response_time']:.2f}s")
            logger.info(f"  - Max response time: {performance_summary['max_response_time']:.2f}s")
        logger.info("="*60)

if __name__ == "__main__":
    try:
        planner = JobPlanner()
        
        results = planner.plan_operations()
        
        planner.export_results(results)
        
        planner.show_performance_comparison(results['metrics'])
        
        logger.info("="*60)
        logger.info("PRAXIS job planning completed successfully")
        logger.info(f"Output saved to: data/output.csv")
        logger.info(f"Log saved to: {log_filename}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Job planning failed: {str(e)}")
        logger.exception("Full error traceback:")
        raise
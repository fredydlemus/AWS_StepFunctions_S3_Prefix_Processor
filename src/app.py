import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f'Received event: {json.dumps(event, default=str)}')

    analysis_result = event.get('analysis_result', [])

    total_errors = 0
    total_warnings = 0
    total_records = 0
    hourly_breakdown = {}

    if isinstance(analysis_result, list):
        for result in analysis_result:
            if result and isinstance(result, dict):
                total_errors += result.get('errorCount', 0)
                total_warnings += result.get('warningCount', 0)
                total_records += result.get('processedRecords', 0)

                hour = result.get('hourOfDay', 'unknown')
                if hour not in hourly_breakdown:
                    hourly_breakdown[hour] = {'errors': 0, 'warnings': 0, 'records': 0}

                hourly_breakdown[hour]['errors'] += result.get('errorCount', 0)
                hourly_breakdown[hour]['warnings'] += result.get('warningCount', 0)
                hourly_breakdown[hour]['records'] += result.get('processedRecords', 0)

    summary = {
        'date': datetime.now().date().isoformat(),
        'totalErrors': total_errors,
        'totalWarnings': total_warnings,
        'totalRecords': total_records,
        'hourlyBreakdown': hourly_breakdown,
        'generatedAt': datetime.now().isoformat()
    }

    logger.info(f'Daily summary: {json.dumps(summary, default=str)}')
    return summary
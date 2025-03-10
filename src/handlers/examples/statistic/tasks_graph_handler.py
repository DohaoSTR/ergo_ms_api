from src.external.examples.bpm.scripts import get_tasks
from src.external.examples.bi.scripts import transform_data_for_bi_graph

from src.core.utils.auto_api.base_handler import BaseHandler

class HandlerClass(BaseHandler):
    def process(self):
        tasks = get_tasks(
            self.params.get('limit', 10),
            self.params.get('offset', 10),
            self.params.get('page_size', 10)
        )

        aggregation_params = [
            {
                "key": "status", 
                "aggregation_type": "count", 
                "data_source": "tasks"
            },
            {
                "key": "process_id", 
                "aggregation_type": "unique_count", 
                "data_source": "tasks"
            }
        ]

        graph_data = transform_data_for_bi_graph(tasks, aggregation_params)

        return {"data": graph_data}
aggregation_params_def = [
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

def transform_data_for_bi_graph(bpm_data, aggregation_params = aggregation_params_def):
    aggregated_data = {}

    for param in aggregation_params:
        key = param.get('key')
        aggregation_type = param.get('aggregation_type')
        data_source = param.get('data_source')

        if aggregation_type == 'count':
            counts = {}
            for item in bpm_data[data_source]:
                value = item.get(key)
                if value in counts:
                    counts[value] += 1
                else:
                    counts[value] = 1
            aggregated_data[f"{key}_counts"] = counts

        elif aggregation_type == 'unique_count':
            unique_counts = {}
            for item in bpm_data[data_source]:
                value = item.get(key)
                if value in unique_counts:
                    unique_counts[value].add(item["id"])
                else:
                    unique_counts[value] = {item["id"]}
            unique_counts = {k: len(v) for k, v in unique_counts.items()}
            aggregated_data[f"{key}_unique_counts"] = unique_counts

    return aggregated_data
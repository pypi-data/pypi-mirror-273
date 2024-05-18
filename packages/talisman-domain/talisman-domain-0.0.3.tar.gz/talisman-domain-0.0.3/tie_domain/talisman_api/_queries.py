def get_pagination_query(pagination: str, query: str, limit: int):
    return f'''
        {{
            {pagination}(filterSettings: {{}}, limit: {limit}) {{
                total
                {query}
            }}
        }}'''

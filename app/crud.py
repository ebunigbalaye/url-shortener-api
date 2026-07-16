"""The actual database operations: create_url(), get_url_by_slug(), increment_click_count(),delete_url(), list_urls(). 
This is the layer between routes and the database — routes call these functions, 
they don't write raw queries inline."""
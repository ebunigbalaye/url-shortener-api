"""Reads environment variables (database URL, base URL for shortened links, default TTL, etc.)
 into a single settings object, usually via pydantic-settings. 
 Every other file imports settings from here instead of reading os.environ directly.
"""
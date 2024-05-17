from functools import wraps

def validate_document_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_cv = kwargs.get('is_cv', None)
        is_job = kwargs.get('is_job', None)

        if len(args) > 0:
            is_cv = args[0]
        if len(args) > 1:
            is_job = args[1]

        if is_cv is None or is_job is None:
            raise ValueError('You must specify either the document is a CV (is_cv) or a Job (is_job).')
        if is_cv == is_job:
            raise ValueError('The document can be either a CV (is_cv) or a Job (is_job), not both.')

        return func(*args, **kwargs)
    return wrapper
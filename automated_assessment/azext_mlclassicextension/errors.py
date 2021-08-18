class AzureMLClassicError(Exception):
    '''AzureML Exception base class.'''
    def __init__(self, message):
        super(AzureMLClassicError, self).__init__(message)

class AzureMLClassicHttpError(AzureMLClassicError):
    '''Error from Azure ML REST API.'''
    def __init__(self, message, status_code):
        super(AzureMLClassicHttpError, self).__init__(message)
        self.status_code = status_code

    def __new__(cls, message, status_code, *args, **kwargs):
        if status_code == 409:
            cls = AzureMLClassicConflictHttpError
        elif status_code == 401:
            cls = AzureMLClassicUnauthorizedError
        return AzureMLClassicError.__new__(cls, message, status_code, *args, **kwargs)

class AzureMLClassicUnauthorizedError(AzureMLClassicHttpError):
    '''Unauthorized error from Azure ML REST API.'''
    def __init__(self, message, status_code):
        message = 'Unauthorized, please check your workspace ID and authorization token ({})'.format(message)
        super(AzureMLClassicUnauthorizedError, self).__init__(message, status_code)


class AzureMLClassicConflictHttpError(AzureMLClassicHttpError):
    '''Conflict error from Azure ML REST API.'''
    def __init__(self, message, status_code):
        super(AzureMLClassicConflictHttpError, self).__init__(message, status_code)

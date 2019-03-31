class InteractionError(Exception):
    """Error occured during the handling of an interaction"""
    pass


class InteractionParsingError(Exception):
    """Error determining the interaction type"""
    pass

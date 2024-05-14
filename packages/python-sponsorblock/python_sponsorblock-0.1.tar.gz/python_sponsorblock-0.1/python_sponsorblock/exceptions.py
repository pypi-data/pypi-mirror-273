class SponsorBlockError(Exception):
    pass

class SponsorBlockIdNotFoundError(SponsorBlockError):
    pass

class SponsorBlockConnectionError(SponsorBlockError):
    pass

class ReturnDefault(SponsorBlockError):
    pass

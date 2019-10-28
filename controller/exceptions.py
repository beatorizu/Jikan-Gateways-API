class CharacterNotFoundException(Exception):

    def __init__(self, name):
        self.message = f'Character {name} not found.'
        super(CharacterNotFoundException, self).__init__(self.message)

class MangaNotFoundException(Exception):

    def __init__(self, name):
        self.message = f'Manga {name} not found.'
        super(MangaNotFoundException, self).__init__(self.message)

class AnimeNotFoundException(Exception):

    def __init__(self, name):
        self.message = f'Anime {name} not found.'
        super(AnimeNotFoundException, self).__init__(self.message)

class ServiceUnavailable(Exception):

    def __init__(self):
        self.message = 'Service Unavailable.'
        super(ServiceUnavailable, self).__init__(self.message)

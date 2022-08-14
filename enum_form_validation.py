import enum

class GenreEnum(enum.Enum):
    
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RnB = 'RnB'
    Reggae = 'Reggae'
    RocknRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    def __str__(self):
        return self.name  # value string

    def __html__(self):
        return self.value  # label string

def coerce_for_enum(enum):
    def coerce(name):
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            raise ValueError(name)
    return coerce
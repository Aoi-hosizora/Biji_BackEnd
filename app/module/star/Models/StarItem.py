class StarItem(object):
    
    def __init__(self, title, url, content):
        self.title = title
        self.url = url
        self.content = content
    
    def toJson(self):
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content
        }

    @staticmethod
    def toJsonSet(stars):
        sets = []
        for star in stars:
            sets.append(star.toJson())
        return sets
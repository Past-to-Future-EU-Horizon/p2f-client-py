import furl

class doi:
    def __init__(self, doi_input: str):
        if doi_input.startswith("10"):
            doi_split = doi_input.split("/")
            print(doi_split)
            if len(doi_split) == 2:
                self.prefix, self.suffix = doi_split
            else:
                raise ValueError("The provided doi object does not conform to the prefix and suffix format.")
        elif doi_input.startswith("http"):
            url = furl.furl(doi_input)
            match url.host:
                case "doi.org": 
                    print(url.path.segments)
                    self.prefix = [x for x in url.path.segments if x.startswith("10")][0]
                    self.suffix = url.path.segments[url.path.segments.index(self.prefix) + 1]
                case "doi.pangaea.de":
                    print(url.path.segments)
                    self.prefix = [x for x in url.path.segments if x.startswith("10")][0]
                    self.suffix = url.path.segments[url.path.segments.index(self.prefix) + 1]
        elif doi_input.startswith("doi:"):
            doi_input = doi_input[4:]
            doi_split = doi_input.split("/")
            print(doi_split)
            if len(doi_split) == 2:
                self.prefix, self.suffix = doi_split
            else:
                raise ValueError("The provided doi object does not conform to the prefix and suffix format.")
        else:
            raise ValueError("Unable to recognize the format of this doi")
        self.url = furl.furl(f"https://doi.org/{self.prefix}/{self.suffix}")
        self.string = f"{self.prefix}/{self.suffix}"
    def __str__(self):
        return self.string
    def __repr__(self):
        return f"<doi object prefix={self.prefix} suffix={self.suffix}>"
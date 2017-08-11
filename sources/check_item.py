# Class for one check item in check list with
# id - number of check item
# status - pass/failed/block
# issue - link Jira issue


class CheckItem:
    def __init__(self, id, status, issue):
        self.id = id
        self.status = status
        self.issue = issue

    def __repr__(self):
        return 'id: {}, issue: {}, status: {}'.format(self.id, self.issue, self.status)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

import funkytree

class Initial(funkytree.State):
    
    @funkytree.state_change_to('HaveString')
    def can_make_string(self):
        return HaveString(x='hello')

    @funkytree.state_change_to('HaveString')
    def can_make_none_string(self):
        return HaveString(x=None)

class HaveString(funkytree.State):

    def test_is_instance(self):
        assert isinstance(self.x, basestring)

    def testHasLength(self):
        len(self.x)

    @funkytree.state_change_to('UpperCaseString')
    def can_upper(self):
        new = self.x.upper()
        return UpperCaseString(x=new)

    @funkytree.state_change_to('LowerCaseString')
    def can_lower(self):
        new = self.x.lower()
        return LowerCaseString(x=new)

class UpperCaseString(funkytree.State):
    def test_all_upper(self):
        assert self.x == self.x.upper()
        assert self.x != self.x.lower()

    @funkytree.state_change_to('LowerCaseString')
    def can_lower(self):
        return LowerCaseString(x=self.x.lower())


class LowerCaseString(funkytree.State):
    def test_all_lower(self):
        assert self.x != self.x.upper()
        assert self.x == self.x.lower()

if __name__ == '__main__':
    funkytree.main(Initial)

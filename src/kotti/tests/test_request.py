class TestExtendingRequest:
    def test_it(self):
        from zope.interface import implementedBy, providedBy

        from kotti.request import Request

        req = Request({})
        req.set_property(lambda x: "exists", "marker", reify=True)

        assert providedBy(req) == implementedBy(Request)
        assert req.marker == "exists"

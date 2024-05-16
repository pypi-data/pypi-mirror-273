from typing import List, Any, Dict, Optional

from flask_projects.core.vars.abs import HttpAbs


class _Detail:

    def __init__(
            self,
            router: str,
            methods: List[str],
            resource: Any
    ):

        self.router = router
        self.methods = methods
        self.resource = resource


class Http(HttpAbs):

    def __init__(self):

        self.map_detail: Dict[str, _Detail] = dict()

    def insert(self, router: str, methods: List[str], resource: Any, **kwargs) -> bool:

        assert not self.map_detail.get(router, None), "the info of http has existed in project"

        detail = _Detail(router, methods, resource)

        if kwargs:
            for key, value in kwargs.items():
                setattr(detail, key, value)

        self.map_detail[router] = detail

        return True

    def query(self, router: str) -> Optional[_Detail]:

        return self.map_detail.get(router, None)

    def query_router(self):

        return self.map_detail.keys()

    def destroy(self, router: str) -> bool:
        del self.map_detail[router]

        return True


http = Http()

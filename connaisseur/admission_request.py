from functools import cached_property

from connaisseur.exceptions import InvalidFormatException
from connaisseur.util import validate_schema
from connaisseur.workload_object import WorkloadObject


class AdmissionRequest:
    __SCHEMA_PATH = "/app/connaisseur/res/ad_request_schema.json"

    def __init__(self, ad_request: dict):
        validate_schema(
            ad_request, self.__SCHEMA_PATH, "AdmissionRequest", InvalidFormatException
        )

        request = ad_request["request"]
        self.__request = request
        self.uid = request["uid"]
        self.kind = request["kind"]["kind"]
        self.namespace = request["namespace"]
        self.operation = request["operation"]
        self.user = request["userInfo"]["username"]
        self.wl_object = WorkloadObject(request["object"], self.namespace)

    @property
    def context(self):
        # for logging, the logged json object cannot have a
        # name field on top-level. thus the context is encapsuled
        # in "admission_review"
        return {
            "admission_review": {
                "user": self.user,
                "operation": self.operation,
                "kind": self.kind,
                "name": self.wl_object.name,
                "namespace": self.namespace,
            }
        }

    @cached_property
    def old_wl_object(self):
        return WorkloadObject(self.__request.get("oldObject"), self.namespace)

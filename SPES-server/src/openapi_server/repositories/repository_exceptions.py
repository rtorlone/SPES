"""
NotFoundError
"""


class NotFoundError(Exception):
    entity_name: str
    entity_id: str

    def __init__(self, entity_id):
        self.entity_id = entity_id
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):
    entity_name: str = "User"


class PersonNotFoundError(NotFoundError):
    entity_name: str = "Person"


class AddressNotFoundError(NotFoundError):
    entity_name: str = "Address"


class CitizenshipNotFoundError(NotFoundError):
    entity_name: str = "Citizenship"


class MaritalStatusNotFoundError(NotFoundError):
    entity_name: str = "MaritalStatus"


class ReportNotFoundError(NotFoundError):
    entity_name: str = "Report"


class DocumentNotFoundError(NotFoundError):
    entity_name: str = "Document"


class PermissionNotFoundError(NotFoundError):
    entity_name: str = "Permission"


"""
UploadError
"""


class UploadError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} upload error, id: {entity_id}")


class UploadReportError(UploadError):
    entity_name: str = "Report"


class UploadDocumentError(UploadError):
    entity_name: str = "Document"


class FormatReportError(Exception):
    entity_name: str
    media_type: str
    entity_id: str

    def __init__(self, entity_id, media_type):
        self.entity_name = "Report"
        self.media_type = media_type
        self.entity_id = entity_id
        super().__init__(f"{self.entity_name} format error, id: {entity_id}. Wrong media type: {media_type}")

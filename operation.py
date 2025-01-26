# operation.py
from uds_enums import OperationType, OperationStatus

class Operation:
    def __init__(self, operation_type: OperationType):
        self._operation_type = operation_type
        self._status = OperationStatus.PENDING

    @property
    def operation_type(self) -> OperationType:
        return self._operation_type

    @property
    def status(self) -> OperationStatus:
        return self._status

    @status.setter
    def status(self, value: OperationStatus):
        self._status = value
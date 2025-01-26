# server.py
from typing import List
from uds_enums import SessionType
from operation import Operation

class Server:
    def __init__(self, can_id: int):
        self._can_id = can_id
        self._session = SessionType.NONE
        self._pending_operations: List[Operation] = []
        self._completed_operations: List[Operation] = []
        self._logs: List[str] = []
        self._p2_timing = 0
        self._p2_star_timing = 0

    # Getters and setters
    @property
    def can_id(self) -> int:
        return self._can_id

    @property
    def session(self) -> SessionType:
        return self._session

    @session.setter
    def session(self, value: SessionType):
        self._session = value

    @property
    def p2_timing(self) -> int:
        return self._p2_timing

    @p2_timing.setter
    def p2_timing(self, value: int):
        self._p2_timing = value

    @property
    def p2_star_timing(self) -> int:
        return self._p2_star_timing

    @p2_star_timing.setter
    def p2_star_timing(self, value: int):
        self._p2_star_timing = value

    # List operations
    def add_pending_operation(self, operation: Operation):
        self._pending_operations.append(operation)

    def remove_pending_operation(self, operation: Operation):
        self._pending_operations.remove(operation)

    def add_completed_operation(self, operation: Operation):
        self._completed_operations.append(operation)

    def add_log(self, log: str):
        self._logs.append(log)

    def get_pending_operation_by_type(self, operation_type: OperationType) -> Operation:
        for operation in self._pending_operations:
            if operation.operation_type == operation_type:
                return operation
        return None

    # UDS Service functions (to be implemented later)
    def read_data_by_identifier(self):
        pass

    def write_data_by_identifier(self):
        pass

    def ecu_reset(self):
        pass

    def transfer_data(self):
        pass

    def request_download(self):
        pass

    def request_transfer_exit(self):
        pass
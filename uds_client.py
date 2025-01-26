# uds_client.py
from typing import List, Optional
from server import Server
from operation import Operation
from uds_enums import SessionType, OperationStatus

class Address:
    def __init__(self, addressing_mode: int = 0, txid: Optional[int] = None, rxid: Optional[int] = None):
        self.addressing_mode = addressing_mode
        self._txid = txid
        self._rxid = rxid

class UdsClient:
    def __init__(self, client_id: int, isotp_layer):
        self._client_id = client_id
        self._servers: List[Server] = []
        self._pending_servers: List[Server] = []
        self._isotp_layer = isotp_layer

    def add_server(self, address: Address, session_type: SessionType):
        # Prepare Diagnostic Session Control message (0x10)
        message = bytearray([0x10, session_type.value])
        
        # Send via ISO-TP
        self._isotp_layer.send(message, address)
        
        # Create new server and add to pending
        server = Server(address._rxid)
        self._pending_servers.append(server)

    def process_message(self, address: Address, data: bytearray):
        service_id = data[0]
        
        if service_id == 0x50:  # Positive response to Session Control
            server = self._find_server_by_can_id(address._txid, self._pending_servers)
            if server:
                server.session = SessionType(data[1])
                self._servers.append(server)
                self._pending_servers.remove(server)
                
        elif service_id == 0x7F:  # Negative response
            server = self._find_server_by_can_id(address._txid, self._pending_servers)
            if server:
                server.add_log(f"Negative response on Session Control: {hex(data[2])}")
                server.session = SessionType.NONE
                self._servers.append(server)
                self._pending_servers.remove(server)
        
        else:  # Response to other services
            server = self._find_server_by_can_id(address._txid, self._servers)
            if server:
                operation = self._find_pending_operation(server, service_id)
                if operation:
                    if service_id & 0x40:  # Positive response
                        operation.status = OperationStatus.COMPLETED
                    else:  # Negative response
                        operation.status = OperationStatus.REJECTED
                    
                    server.remove_pending_operation(operation)
                    server.add_completed_operation(operation)

    def _find_server_by_can_id(self, can_id: int, server_list: List[Server]) -> Optional[Server]:
        for server in server_list:
            if server.can_id == can_id:
                return server
        return None

    def _find_pending_operation(self, server: Server, service_id: int) -> Optional[Operation]:
        # Implementation depends on how you want to match service IDs to operations
        pass

    def receive_message(self, data: bytearray, address: Address):
        self.process_message(address, data)
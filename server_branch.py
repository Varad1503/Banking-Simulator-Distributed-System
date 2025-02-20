import grpc
from concurrent import futures
import time
import sys
import json

# import the generated classes
import comm_pb2
import comm_pb2_grpc

# import the original calculator.py
import branch
from branch import Branch

input_json_file = sys.argv[1]
b = Branch()
branch_stubs = b.createstub_branch(input_json_file)
number_of_branchs = len(branch_stubs)

class CommunicatorServicer(comm_pb2_grpc.CommunicatorServicer):
    def __init__(self, branch_instance):
        self.branch_instance = branch_instance

    def BranchInfo(self,request,context):
        money = request.branch_balance
        branch_id = float(request.branch_id)
        interface = request.interface
        update = self.branch_instance.Update_Balance(money,branch_id,interface)
        response = comm_pb2.BroadCast_Response(value=update)
        return response

    def Customer_Process(self, request, context):
        # Extract customer_id, interface, and money from the request
        customer_id = request.customer_id
        interface = request.interface
        money = request.money
        new_amount = self.branch_instance.msgDelivery(customer_id, interface, money)
        if new_amount != None:
            process_result = "SUCCESS"
        response = comm_pb2.Info_Response(new_balance=new_amount,process_result = process_result)
        #new_balance = response.new_balance
        for i in range(number_of_branchs+1):
            port = 50000 + i;
            channel_branch = grpc.insecure_channel('localhost:'+str(port))
            stub_branch = comm_pb2_grpc.CommunicatorStub(channel_branch)
            output = stub_branch.BranchInfo(comm_pb2.BroadCast(branch_balance = money, branch_id = float(i), interface = interface ))
        return response

server_names = [f"server{i}" for i in range(number_of_branchs + 1)]
for i in range(number_of_branchs + 1):
    server_names[i] = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comm_pb2_grpc.add_CommunicatorServicer_to_server(CommunicatorServicer(b), server_names[i])
    port = 50000 + i;
    server_names[i].add_insecure_port('[::]:'+str(port))
    server_names[i].start()
    print('Server started. Listening on port '+str(port)+".")



try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

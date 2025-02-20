import grpc
import sys
import comm_pb2
import comm_pb2_grpc
import json
from customer import Customer  # Make sure the 'customer' module is correctly imported

def customer_service_client():
    # Create a gRPC channel to connect to the server
    output_data = []
    input_json_file = sys.argv[1]  # Assuming you're passing the JSON file as a command-line argument
    c = Customer()
    cust_stubs = c.createstubs(input_json_file)
    count_customer = c.count_customers();
    total_events = len(cust_stubs)
    customer_ports= [f"{50000 + i}" for i in range(1, count_customer+ 1)]
    #channel = grpc.insecure_channel('localhost:50000')  # Replace with the appropriate server address

    # Create a gRPC stub for the CustomerService
    #stub = comm_pb2_grpc.CommunicatorStub(channel)

    for customer in cust_stubs:
        port = 50000 + int(customer["customer_id"])
        channel = grpc.insecure_channel('localhost:'+str(port))  # Replace with the appropriate server address
            #channel = grpc.insecure_channel('localhost:50000')  # Replace with the appropriate server address

    # Create a gRPC stub for the CustomerService
    #stub = comm_pb2_grpc.CommunicatorStub(channel)

        stub = comm_pb2_grpc.CommunicatorStub(channel)
        customer_id = float(customer['customer_id'])
        event_id = float(customer["event_id"])

        money = float(customer.get('money', 0))  # 'money' may not be present for 'query' events
        interface = customer['interface']
         #channel = grpc.insecure_channel('localhost:50000')  # Replace with the appropriate server address

        response = stub.Customer_Process(comm_pb2.Info_Request(customer_id=customer_id, money=money, interface=interface))
        # Handle the response
        new_balance = response.new_balance
        process_result = response.process_result
        if( interface == "deposit" or interface == "withdraw"):
            next_event = "query"
        if( interface == "deposit" or interface == "withdraw"):
            #print(f"customer ({customer_id}) event ({event_id}) interface ({interface}) money({money}) new balance: {new_balance}")
            output_entry = {"id": customer_id, "recv": [{"interface": interface, "result": process_result }, {"interface": next_event, "result": "SUCCESS", "money": new_balance}]}
            print(output_entry)
        output_data.append(output_entry)

    with open('output.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=2)
            

    

if __name__ == '__main__':
    customer_service_client()

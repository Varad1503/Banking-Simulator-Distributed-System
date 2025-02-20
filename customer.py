import sys
import json
#import stub_service_pb2_grpc
#import stub_service_pb2
import grpc

class Customer:
    def __init__(self):
        self.stubs = []
        self.count = 0;

    def count_customers(self):
        return self.count

    def createstubs(self, input_json_file):
        try:
            with open(input_json_file, 'r') as json_file:
                data = json.load(json_file)
                for customer_person in data:
                    if customer_person["type"] == "customer":
                        self.count = int(customer_person["id"])
                        customer_id = float(customer_person['id'])
                        for e in customer_person['events']:
                            event_id = float(e['id'])
                            interface = e['interface']
                            if interface == "query":
                                # 'money' may not be present for 'query' events, use a default of 0
                                money = float(0)
                                stub = self._create_stub(customer_id, event_id, interface,money)
                                self.stubs.append(stub)
                            else:
                                money = float(e['money'])
                                stub = self._create_stub_withdraw_deposit(customer_id, event_id, interface, money)
                                self.stubs.append(stub)
        except FileNotFoundError:
            print(f"Error: File '{input_json_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return self.stubs


    def _create_stub(self, customer_id, event_id, interface,money):
        # Create a dictionary based on the event data
        return {'customer_id': customer_id, 'event_id': event_id, 'interface': interface, 'money': money}

    def _create_stub_withdraw_deposit(self, customer_id, event_id, interface, money):
        # Create a dictionary based on the event data
        return {'customer_id': customer_id, 'event_id': event_id, 'interface': interface, 'money': money}


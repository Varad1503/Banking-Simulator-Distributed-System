import json
import grpc
import comm_pb2
import comm_pb2_grpc

class Branch(comm_pb2_grpc.CommunicatorServicer):
  def __init__(self):
    self.branch_stubs = []

  def createstub_branch(self, input_json_file):
    with open(input_json_file, 'r') as json_file:
      data = json.load(json_file)
      for customer_person in data:
        if customer_person["type"] == "branch":
          branch_id = float(customer_person["id"])
          balance = float(customer_person["balance"])
          stub = self._create_stub(branch_id,balance)
          self.branch_stubs.append(stub)
    return(self.branch_stubs)
  
  def msgDelivery(self,customer_id,interface,money):
    branch_id = customer_id
    new_amount = 0;
    if interface == "withdraw":
     new_amount = self.withdraw(branch_id,money)
     return(new_amount)
    elif interface == "deposit":
     new_amount = self.deposit(branch_id,money)
     return(new_amount)
    elif interface == "query":
     new_amount = self.query(branch_id,money)
     return(new_amount)
    

  def _create_stub(self,branch_id, balance):
    return {'branch_id': branch_id, 'balance': balance}

  def withdraw(self, customer_id,money):
    for stub in self.branch_stubs:
        if stub["branch_id"] == customer_id:
          amount_withdraw = stub["balance"] - money
          return(amount_withdraw)  # Assuming `branch_id` is an attribute of the stub

  def deposit(self, customer_id,money):
    for stub in self.branch_stubs:
        if stub["branch_id"] == customer_id:  # Assuming `branch_id` is an attribute of the stub
         amount_deposit = stub["balance"] + money
         #self.Update_Balance(amount_deposit)
         return(amount_deposit)


  def query(self,customer_id,money):
    for stub in self.branch_stubs:
      if stub["branch_id"] == customer_id:
        amount_query = stub["balance"]
        #self.Update_Balance(amount_query)
        return(amount_query)

  def Update_Balance(self,money,branch_id,interface):
     for stub in self.branch_stubs:
        if stub["branch_id"] == branch_id:
          if interface == "deposit":
            amount = self.Propogate_Deposit(money,branch_id)
            return(amount)
          elif interface == "withdraw":
            amount = self.Propogate_Withdraw(money,branch_id)
            return(amount)
          elif interface == "query":
            return(stub["balance"])

   #def Propogate_Deposit(self,branch_balance,branch_id):
  #  new_balance = branch_balance
  #  port = int(50000 + branch_id)
  #  channel = grpc.insecure_channel('localhost:'+str(port))
  #  stub = comm_pb2_grpc.CommunicatorStub(channel)
  #  response = stub.BranchInfo(comm_pb2.BroadCast(branch_balance = new_balance))
  #  return 0   
  def Propogate_Withdraw(self,money,branch_id):
    for stub in self.branch_stubs:
      if stub["branch_id"] == branch_id:
        stub["balance"] = self.withdraw(branch_id,money);
        return(stub["balance"])

# def Propogate_Withdraw(self,branch_balance,branch_id):
 #   new_balance = branch_balance
 #   port = int(50000 + branch_id)
 #   channel = grpc.insecure_channel('localhost:'+str(port))
 #   stub = comm_pb2_grpc.CommunicatorStub(channel)
 #   response = stub.BranchInfo(comm_pb2.BroadCast(branch_balance = new_balance))
 #   return 0
  def Propogate_Deposit(self,money,branch_id):
    for stub in self.branch_stubs:
      if stub["branch_id"] == branch_id:
        stub["balance"] = self.deposit(branch_id,money);
        return(stub["balance"])


         


 


  
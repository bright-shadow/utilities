import json
import os

########################     DEFINITION


class generic_transaction:

    attributes = None

    def __init__(self, ext_attributes, transaction_attributes):

        self.attributes = transaction_attributes

        if not (ext_attributes.__class__ == dict):
            raise ValueError("Attributes are not in a dictionary form")
        for k in ext_attributes.keys():
            if not k in self.attributes.keys():
                raise Exception("Attributes are in an invalid format")

        self.attributes = ext_attributes

    def __str__(self):
        return str(self.attributes)


class generic_transaction_manager:

    transaction_list = list()

    def load_transactions(self, transactions_list):
        # CHECK IF THE TRANSACTION FORMAT IS CORRECT
        # AND IF THEY'RE DUPLICATED
        if not (transactions_list.__class__ == list):
            raise ValueError(
                "Attributes are not in a list[generic_transaction instance] form"
            )
        for t in transactions_list:
            if not isinstance(t, generic_transaction):
                raise ValueError(
                    "Functions are not in a list[instanceof(generic_transaction)] form"
                )

        for ext_t in transactions_list:

            found = False

            for int_t in self.transaction_list:
                if ext_t.attributes == int_t.attributes:
                    found = True
                    break

            if not found:
                self.transaction_list.append(ext_t)

        return True

    # LOOKUP FOR TRANSACTION
    # , BASED UPON AN EXACT TRANSACTION PARAMETERS CORRESPONDENCE
    def lookup_for_transactions(self, key_value_dict):

        query_parameters_length = len(key_value_dict)

        correspondent_transactions = list()

        for transaction in self.transaction_list:
            correspondences = 0

            # LOOKING UP FOR CORRESPONDENCES
            for k_v_d in key_value_dict.keys():
                if key_value_dict[k_v_d] == transaction.attributes[k_v_d]:
                    correspondences += 1

            # DECIDE IF TO APPEND THE TRANSACTION
            if correspondences == query_parameters_length:
                correspondent_transactions.append(transaction)

        return correspondent_transactions
    
    


########################     EXECUTION


# DEFINE THE TRANSACTION ATTRIBUTES
transaction_attributes = {
    "value": {"amount": None, "currency": None},
    "time": None,
    "reason": None,
    "receiver": None,
    "description": None,
}

# DEFINE A TRANSACTION MANAGER
transaction_manager_instance = generic_transaction_manager()

# OPEN A FILE CONTAINING A BULK OF TRANSACTIONS
def bulk_load(path):

    if not os.path.exists(path):
        return False

    with open(path) as file:
        content = file.read()

    return json.loads(content)


# CREATE A LIST OF TRANSACTIONS
# FROM A LIST OF DICTS OF TRANSACTIONS
def create_transactions(raw_transactions):
    transactions_list = list()

    for t in raw_transactions:
        transactions_list.append(generic_transaction(t, transaction_attributes))

    return transactions_list


# DEFINE THE MAIN EXECUTION FLOW OF THE PROGRAM
# WITH VARIOUS EXECUTION OPTIONS
def main():
    while True:

        try:
            choose = input(
                """
                       Choose the operation: 
                       1 - Load transactions from a given path
                       2 - Display all transactions
                       3 - Display a transaction subset
                       exit - To exit
                    """
            )
        except:
            print("Invalid input")
            continue

        if choose == "1":
            jsonned_transactions = None
            try:
                jsonned_transactions = bulk_load(input("Need a path to load: "))
                if jsonned_transactions == False:
                    print("Given path is non existent \n")
                    continue
                transaction_manager_instance.load_transactions(
                    create_transactions(jsonned_transactions)
                )
            except:
                print("Invalid data processed")
        elif choose == "2":
            for t in transaction_manager_instance.transaction_list:
                print("\n" + str(t))
        elif choose == "3":
            query = None
            try:
                query = json.loads(input("Input the research json hash: "))
                for transaction in transaction_manager_instance.lookup_for_transactions(
                    query
                ):
                    print(transaction)
            except:
                print("Invalid input or Invalid stored data encountered")
                continue
        elif choose == "exit":
            exit()
        else:
            print("Invalid option")


main()
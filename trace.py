#Traceability in fishery supply chain using blockchain
import base64
from solcx import compile_standard, install_solc
from web3 import Web3
import json


#Read Solidity file and convert into json file
install_solc('0.8.5')
with open("traceability.sol", "r") as file:
    fish_file_details = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"sample fish.sol": {"content": fish_file_details}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract
                }
            }
        },
    },
    solc_version="0.8.5",
)

with open("compiled_code3.json", "w") as file:
    json.dump(compiled_sol, file)
# get bytecode
bytecode = compiled_sol["contracts"]["sample fish.sol"]["SupplyChain"]["evm"]["bytecode"]["object"]
#print(bytecode)

# get abi
abi = json.loads(compiled_sol["contracts"]["sample fish.sol"]["SupplyChain"]["metadata"])["output"]["abi"]
#print(abi)


# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
address = "0x72a95f128ba392461b394Dd7D45CB8cD400DAC74"
private_key = "0xa4a1cdc9a35fe5f93405ccfb409b5c860e306544fd926cb97ea717dcea3b7726" # leaving the private key like this is very insecure if you are working on real world project

# Create the contract in Python
FishMania = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the number of latest transaction
nonce = w3.eth.get_transaction_count(address)

# build transaction
transaction = FishMania.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

# Sign the transaction
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#print("Deploying Contract!")

# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
#print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
#print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

#initialize our contract with the contract address and ABI.
fish_details = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
#print(fish_details)

while True:

    print("\n\t\t\t\t******* Traceability of Fish using Blockchain ********")
    print("\t\t\t\t 1. Add the Details")
    print("\t\t\t\t 2. Supply fish lots")
    print("\t\t\t\t 3. Trace Stage")
    print("\t\t\t\t 4. Showing the details")
    print("\t\t\t\t ********************************************************\n")

    choice = input("\t\t\t\t Please enter the above choice only: ")
    #Fisherman details
    if choice == '1':
        while True:
            print("\n\t\t\t\t\t\t********** Adding the Details ***************")
            print("\t\t\t\t\t\t a. Add Fisherman Deatils")
            print("\t\t\t\t\t\t b. Add Processor Deatils")
            print("\t\t\t\t\t\t c. Add Distrbutor Deatils")
            print("\t\t\t\t\t\t d. Add Retailer Deatils")
            print("\t\t\t\t\t\t e. Add Fish Image")
            print("\t\t\t\t\t\t f. Add Fish Details")
            print("\t\t\t\t\t\t *********************************************\n")
            choice1 = input("\t\t\t\t\t\t Please enter the above choice only: ")

            # Add Fisherman details
            if choice1 == 'a':
                name = input("\t\t\t\t\t\t Enter the Name:")
                place = input("\t\t\t\t\t\t Enter the place:")
                contactno = input("\t\t\t\t\t\t Enter the Contact no:")
                # Fisherman data store on contract
                store_fisherman = fish_details.functions.addFisherman(address, name, place, contactno).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})
                # Sign the transaction for fisherman
                sign_store_fisherman = w3.eth.account.sign_transaction(
                    store_fisherman, private_key=private_key
                )
                # Send the transaction of fisherman and get transaction receipt
                send_store_fisherman = w3.eth.send_raw_transaction(sign_store_fisherman.rawTransaction)
                transaction_receipt_fisherman = w3.eth.wait_for_transaction_receipt(send_store_fisherman)

                print("\n\t\t\t\t\t\t Fisherman Details:")
                print(send_store_fisherman)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_fisherman)

            #Processor Details
            elif choice1 == 'b':
                name = input("\t\t\t\t\t\t Enter the Name:")
                place = input("\t\t\t\t\t\t Enter the place:")
                contactno = input("\t\t\t\t\t\t Enter the Contact no:")

                # Processor data store on contract
                store_processor = fish_details.functions.addProcessor(address, name, place, contactno).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 2})

                # Sign the transaction for processor
                sign_store_processor = w3.eth.account.sign_transaction(
                    store_processor, private_key=private_key
                )

                # Send the transaction of processor and get transaction receipt
                send_store_processor = w3.eth.send_raw_transaction(sign_store_processor.rawTransaction)
                transaction_receipt_processor = w3.eth.wait_for_transaction_receipt(send_store_processor)

                print("\n\t\t\t\t\t\t Processor Details:")
                print(send_store_processor)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_processor)

            #Distributer Details
            elif choice1 == 'c':
                name = input("\t\t\t\t\t\t Enter the Name:")
                place = input("\t\t\t\t\t\t Enter the place:")
                contactno = input("\t\t\t\t\t\t Enter the Contact no:")

                # Distributor data store on contract
                store_distributor = fish_details.functions.addDistributor(address, name, place, contactno).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 3})

                # Sign the transaction for distributor
                sign_store_distributor = w3.eth.account.sign_transaction(
                    store_distributor, private_key=private_key
                )

                # Send the transaction of distributor and get transaction receipt
                send_store_distributor = w3.eth.send_raw_transaction(sign_store_distributor.rawTransaction)
                transaction_receipt_distributor = w3.eth.wait_for_transaction_receipt(send_store_distributor)

                print("\n\t\t\t\t\t\t Distributor Details:")
                print(send_store_distributor)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_distributor)

            #Retailer Details
            elif choice1 == 'd':
                name = input("\t\t\t\t\t\t Enter the Name:")
                place = input("\t\t\t\t\t\t Enter the place:")
                contactno = input("\t\t\t\t\t\t Enter the Contact no:")

                # Retailer data store on contract
                store_retailer = fish_details.functions.addRetailer(address, name, place, contactno).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 4})

                # Sign the transaction for retailer
                sign_store_retailer = w3.eth.account.sign_transaction(
                    store_retailer, private_key=private_key
                )

                # Send the transaction of retailer and get transaction receipt
                send_store_retailer = w3.eth.send_raw_transaction(sign_store_retailer.rawTransaction)
                transaction_receipt_retailer = w3.eth.wait_for_transaction_receipt(send_store_retailer)

                print("\n\t\t\t\t\t\t Retailer Details:")
                print(send_store_retailer)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_retailer)

            # Add Image
            elif choice1 == 'e':
                # read fish image and convert it into base64
                with open("C://Desktop Data 4-11-2023//fish//test1.jpg", "rb") as fishimage:
                    fish_base64 = base64.b64encode(fishimage.read())
                fish_image = str(fish_base64)

                # Image store on contract
                store_image = fish_details.functions.pushImage(fish_image, address).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 5})

                # Sign the transaction for image
                sign_store_image = w3.eth.account.sign_transaction(
                    store_image, private_key=private_key
                )

                # Send the transaction of image and get transaction receipt
                send_store_image = w3.eth.send_raw_transaction(sign_store_image.rawTransaction)
                transaction_receipt_image = w3.eth.wait_for_transaction_receipt(send_store_image)

                print("\n\t\t\t\t\t\t Image Details:")
                print(send_store_image)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_image)

            # Fish details
            elif choice1 == 'f':
                fishname = input("\t\t\t\t\t\t Enter the Fish Name:")
                capturearea = input("\t\t\t\t\t\t Enter the Region name:")
                fishweight = input("\t\t\t\t\t\t Enter the Fish weight:")

                # Fish information data store on contract
                store_fish = fish_details.functions.addfishlot(fishname, capturearea, fishweight).build_transaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 6})

                # Sign the transaction for fish
                sign_store_fish = w3.eth.account.sign_transaction(
                store_fish, private_key=private_key
                )

                # Send the transaction of fish details and get transaction receipt
                send_store_fish = w3.eth.send_raw_transaction(sign_store_fish.rawTransaction)
                transaction_receipt_fish = w3.eth.wait_for_transaction_receipt(send_store_fish)

                print("\n\t\t\t\t\t\t Fish Details:")
                print(send_store_fish)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_fish)

            else:
                print("\n\t\t\t\t\t\t Sorry you are not entered the correct choice..!!")

            ch1 = input("\n\t\t\t\t\t\t Want to continue in the add panel?(y/n):")
            if ch1 == 'n':
                break

    elif choice == '2':
        while True:
            print("\n\t\t\t\t\t\t********** Supply Fishlot ***************")
            print("\t\t\t\t\t\t a. Supply fishlots from Fisherman to the processor")
            print("\t\t\t\t\t\t b. Process Fishlot ")
            print("\t\t\t\t\t\t c. Distribute Fishlot ")
            print("\t\t\t\t\t\t d. Retailer fishlot ")
            print("\t\t\t\t\t\t e. Sold Fishlot ")
            print("\t\t\t\t\t\t *********************************************\n")

            choice2 = input("\t\t\t\t\t\t Please select the above choice only: ")

            # supply fishlots from Fisherman to the processor
            if choice2 == 'a':
                fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))

                # FSsupply data store on contract
                store_FSsupply = fish_details.functions.FSsupply(fishlotID).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 7})

                # Sign the transaction for FSsupply
                sign_store_FSsupply = w3.eth.account.sign_transaction(
                    store_FSsupply, private_key=private_key
                )
                # Send the transaction of FSsupply and get transaction receipt
                send_store_FSsupply = w3.eth.send_raw_transaction(sign_store_FSsupply.rawTransaction)
                transaction_receipt_FSsupply = w3.eth.wait_for_transaction_receipt(send_store_FSsupply)

                print("\n\t\t\t\t\t\t FSsupply Details:")
                print(send_store_FSsupply)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_FSsupply)

            #Process fishlot
            elif choice2 == 'b':
                fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))

                # Processing data store on contract
                store_Processing = fish_details.functions.Processing(fishlotID).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 8})

                # Sign the transaction for Processing
                sign_store_Processing = w3.eth.account.sign_transaction(
                    store_Processing, private_key=private_key
                )
                # Send the transaction of Processing and get transaction receipt
                send_store_Processing = w3.eth.send_raw_transaction(sign_store_Processing.rawTransaction)
                transaction_receipt_Processing = w3.eth.wait_for_transaction_receipt(send_store_Processing)

                print("\n\t\t\t\t\t\t Processing Details:")
                print(send_store_Processing)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_Processing)

            # supply fishlots from Processor to distributor
            elif choice2 == 'c':
                fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))

                # Distribute data store on contract
                store_Distribute = fish_details.functions.Distribute(fishlotID).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 9})

                # Sign the transaction for Distribute
                sign_store_Distribute = w3.eth.account.sign_transaction(
                    store_Distribute, private_key=private_key
                )
                # Send the transaction of Distribute and get transaction receipt
                send_store_Distribute = w3.eth.send_raw_transaction(sign_store_Distribute.rawTransaction)
                transaction_receipt_Distribute = w3.eth.wait_for_transaction_receipt(send_store_Distribute)

                print("\n\t\t\t\t\t\t Distribute Details:")
                print(send_store_Distribute)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_Distribute)

            # supply supply fishlots from distributor to retailer
            elif choice2 == 'd':
                fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))

                # Retail data store on contract
                store_Retail = fish_details.functions.Retail(fishlotID).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 10})

                # Sign the transaction for Retail
                sign_store_Retail = w3.eth.account.sign_transaction(
                    store_Retail, private_key=private_key
                )
                # Send the transaction of Retail and get transaction receipt
                send_store_Retail = w3.eth.send_raw_transaction(sign_store_Retail.rawTransaction)
                transaction_receipt_Retail = w3.eth.wait_for_transaction_receipt(send_store_Retail)

                print("\n\t\t\t\t\t\t Retail Details:")
                print(send_store_Retail)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_Retail)

            # sell fishlots from retailer to consumer
            elif choice2 == 'e':
                fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))

                # sold data store on contract
                store_sold = fish_details.functions.sold(fishlotID).build_transaction(
                    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 11})

                # Sign the transaction for sold
                sign_store_sold = w3.eth.account.sign_transaction(
                    store_sold, private_key=private_key
                )
                # Send the transaction of sold and get transaction receipt
                send_store_sold = w3.eth.send_raw_transaction(sign_store_sold.rawTransaction)
                transaction_receipt_sold = w3.eth.wait_for_transaction_receipt(send_store_sold)

                print("\n\t\t\t\t\t\t Sold Details:")
                print(send_store_sold)
                print("\n\t\t\t\t\t\t Transaction Receipt:")
                print(transaction_receipt_sold)
            else:
                print("\n\t\t\t\t\t\t Sorry you are not entered the correct choice..!!")

            ch2 = input("\n\t\t\t\t\t\t Want to continue in the supply panel?(y/n):")
            if ch2 == 'n':
                break

    elif choice == '3':
    # Stage details
        #elif choice == '13':
            fishlotID = int(input("\t\t\t\t\t\t Enter the fish lot id:"))
            stage_details = fish_details.functions.showStage(fishlotID).call()
            print("\t\t\t\t\t\t ******* Stage Details ***********")
            print("\t\t\t\t\t\t",stage_details)
            print("\t\t\t\t\t\t *********************************\n")

    elif choice == '4':
        while True:
            print("\n\t\t\t\t\t\t ***** Show Fish Details *********")
            print("\t\t\t\t\t\t a. Show Fish lot Details ")
            print("\t\t\t\t\t\t b. Show Fisherman Details ")
            print("\t\t\t\t\t\t c. Show Processor Details ")
            print("\t\t\t\t\t\t d. Show Distributor Details ")
            print("\t\t\t\t\t\t e. Show Retailer Details ")
            print("\t\t\t\t\t\t f. Show Fisherman Count ")
            print("\t\t\t\t\t\t g. Show Processor Count")
            print("\t\t\t\t\t\t h. Show Distributor Count ")
            print("\t\t\t\t\t\t i. Show Retailer Count ")
            print("\t\t\t\t\t\t j. Show Fish lot Count ")
            print("\t\t\t\t\t\t k. Show the Image of fish")
            print("\t\t\t\t\t\t *********************************\n")
            choice3 = input("\t\t\t\t\t\t Please select the above choice only: ")

            # fishlotstock details
            if choice3 == 'a':
                id = int(input("\t\t\t\t Enter the fish lot id:"))
                details = fish_details.functions.FishlotStock(id).call()
                # print(details)
                print("\n\t\t\t\t ******** Fish Details *********")
                print("\t\t\t\t Fish Lot Id:", details[0])
                print("\t\t\t\t Fish Name:", details[1])
                print("\t\t\t\t Cpature Area:", details[2])
                print("\t\t\t\t Fish Weight at the time of packing:", details[3])
                print("\t\t\t\t Fisherman id:", details[4])
                print("\t\t\t\t Processor id", details[5])
                print("\t\t\t\t Distributor id:", details[6])
                print("\t\t\t\t Retailer id:", details[7])
                print("\t\t\t\t Image Id:", details[8])
                print("\t\t\t\t Stage no :", details[9])
                print("\t\t\t\t *****Thank you !!...Visit Again!!*********\n")

            # Fisherman Details
            elif choice3 == 'b':
                fsid = int(input("\t\t\t\t\t\t Enter the fisherman id:"))
                Fisherman_details = fish_details.functions.FS(fsid).call()
                print("\n\t\t\t\t\t\t ******* Fisherman Details *********")
                print("\t\t\t\t\t\t Owner Address:", Fisherman_details[0])
                print("\t\t\t\t\t\t Id:", Fisherman_details[1])
                print("\t\t\t\t\t\t Name:", Fisherman_details[2])
                print("\t\t\t\t\t\t Place:", Fisherman_details[3])
                print("\t\t\t\t\t\t Contact number:", Fisherman_details[4])
                print("\t\t\t\t\t\t *********************************\n")

            # show processor details
            elif choice3 == 'c':
                proid = int(input("\t\t\t\t\t\t Enter the processor id:"))
                Processor_details = fish_details.functions.PRO(proid).call()
                print("\n\t\t\t\t\t\t ***** Processor Details *********")
                print("\t\t\t\t\t\t Owner Address:", Processor_details[0])
                print("\t\t\t\t\t\t Id:", Processor_details[1])
                print("\t\t\t\t\t\t Name:", Processor_details[2])
                print("\t\t\t\t\t\t Place:", Processor_details[3])
                print("\t\t\t\t\t\t Contact number:", Processor_details[4])
                print("\t\t\t\t\t\t *********************************\n")

            # show distributor details
            elif choice3 == 'd':
                dsid = int(input("\t\t\t\t\t\t Enter the distributor id:"))
                Distributor_details = fish_details.functions.DIS(dsid).call()
                print("\n\t\t\t\t\t\t ***** Distributor Details *********")
                print("\t\t\t\t\t\t Owner Address:", Distributor_details[0])
                print("\t\t\t\t\t\t Id:", Distributor_details[1])
                print("\t\t\t\t\t\t Name:", Distributor_details[2])
                print("\t\t\t\t\t\t Place:", Distributor_details[3])
                print("\t\t\t\t\t\t Contact number:", Distributor_details[4])
                print("\t\t\t\t\t\t *********************************\n")

            # show retailer details
            elif choice3 == 'e':
                reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Retailer_details = fish_details.functions.RET(reid).call()
                print("\n\t\t\t\t\t\t ***** Retailer Details *********")
                print("\t\t\t\t\t\t Owner Address:", Retailer_details[0])
                print("\t\t\t\t\t\t Id:", Retailer_details[1])
                print("\t\t\t\t\t\t Name:", Retailer_details[2])
                print("\t\t\t\t\t\t Place:", Retailer_details[3])
                print("\t\t\t\t\t\t Contact number:", Retailer_details[4])
                print("\t\t\t\t\t\t *********************************\n")

            # show Fisherman count
            elif choice3 == 'f':
                #reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Fisherman_count = fish_details.functions.fmCtr().call()
                print("\n\t\t\t\t\t\t ***** Fisherman count *********")
                print("\t\t\t\t\t\t Count:", Fisherman_count)
                print("\t\t\t\t\t\t *********************************\n")

            # Show Processor count
            elif choice3 == 'g':
                #reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Processor_count = fish_details.functions.proCtr().call()
                print("\n\t\t\t\t\t\t ***** Processor count *********")
                print("\t\t\t\t\t\t Count:", Processor_count)
                print("\t\t\t\t\t\t *********************************\n")

            # Show Distributor count
            elif choice3 == 'h':
                #reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Distributor_count = fish_details.functions.disCtr().call()
                print("\n\t\t\t\t\t\t ***** Distributor count *********")
                print("\t\t\t\t\t\t Count:", Distributor_count)
                print("\t\t\t\t\t\t *********************************\n")

            #Show Retailer count
            elif choice3 == 'i':
                #reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Retailer_count = fish_details.functions.retCtr().call()
                print("\n\t\t\t\t\t\t ***** Retailer count *********")
                print("\t\t\t\t\t\t Count:", Retailer_count)
                print("\t\t\t\t\t\t *********************************\n")

            # Show fishlot count
            elif choice3 == 'j':
                #reid = int(input("\t\t\t\t\t\t Enter the retailer id:"))
                Fishlot_count = fish_details.functions.fishlotCtr().call()
                print("\n\t\t\t\t\t\t ***** Fishlot count *********")
                print("\t\t\t\t\t\t Count:", Fishlot_count)
                print("\t\t\t\t\t\t *********************************\n")

            # show fish image
            elif choice3 == 'k':
                imid = int(input("\t\t\t\t\t\t Enter the image id:"))
                image_details = fish_details.functions.returnImage(imid).call()
                str1 = image_details[0]
                str2 = str1[2:-1]
                decoded_data = base64.b64decode((str2))
                with open("C://Desktop Data 4-11-2023//fish//original_sample_image.jpeg","wb") as img_file:
                    img_file.write(decoded_data)
                print("\n\t\t\t\t\t\t ***************** Fish Image ************************* ")
                print("\n\t\t\t\t\t\t Please check image in C://Desktop Data 4-11-2023//fish ")
                print("\t\t\t\t\t\t ****************************************************\n")

            else:
                print("\n\t\t\t\t\t\t Sorry you are not entered the correct choice..!!")

            ch3 = input("\n\t\t\t\t\t\t Want to continue in the showing panel?(y/n):")
            if ch3 == 'n':
                break

    else :
        print("\n\t\t\t\t Sorry you are not entered the correct choice..!!")

    ch = input("\n\t\t\t\t Do you want to continue?(y/n):")
    if ch == 'n':
        break




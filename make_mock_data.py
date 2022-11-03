from dataclass import MasterAccount, MessagingAppProfile
import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def main():
    master_account_df = {
        "Org_name": ["MockOrg", "MockOrg", "MockOrg"],
        "Messaging_id": ["id1", "id2", "id3"],
        "Public_key": [b'publickey1', b'publickey2', b'publickey3']
    }
    master_account_df = pd.DataFrame(master_account_df)
    master_account_df.to_pickle("./data/mock_master_account_df.pkl")

    messagingAppProfile_df = {
        "id": ["12345", "12345", "12345"],
        "Org_name": ["MockOrg1", "MockOrg2", "MockOrg3"],
        "Private_key": [b'privatekey1', b'privatekey2', b'privatekey3']
    }
    messagingAppProfile_df = pd.DataFrame(messagingAppProfile_df)
    messagingAppProfile_df.to_pickle("./data/mock_messagingProfile_account_df.pkl")

if __name__ == '__main__':
    main()
    
    test_master_account = MasterAccount()
    test_master_account.load_account_from_org_name("MockOrg")
    test_master_account.save_account()
    test_master_account.load_account_from_org_name("MockOrg")

    print(test_master_account.org_name)
    print(test_master_account.id_key_dict)

    test_messaging_profile = MessagingAppProfile()
    test_messaging_profile.load_profile_from_id("12345")
    test_messaging_profile.save_profile()
    test_messaging_profile.load_profile_from_id("12345")
    print(test_messaging_profile.id)
    print(test_messaging_profile.private_signatures)

    key = RSA.generate(2048)
    
    private_key = key.export_key()
    private_key = RSA.import_key(private_key)
    print(f"private key: {private_key}")
    print(type(private_key))

    public_key =  key.publickey().export_key()
    public_key = RSA.import_key(public_key)
    # print(f"public key: {public_key}")

    data = "testing testing 1 2 3".encode()
    hashed_data = SHA256.new(data)
    signed_data = pkcs1_15.new(private_key).sign(hashed_data)

    try:
        pkcs1_15.new(public_key).verify(hashed_data, signed_data)
        print("Verification successful")

    except (ValueError, TypeError):
        print("Verification failed")

    # cipher_rsa = PKCS1_OAEP.new(public_key)
    # encrypted_data = cipher_rsa.encrypt(data)

    # cipher_rsa = PKCS1_OAEP.new(private_key)
    # decrypted_data = cipher_rsa.decrypt(encrypted_data)

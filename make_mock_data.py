from dataclass import MasterAccount, MessagingAppProfile
import pandas as pd

def main():
    master_account_df = {
        "Org_name": ["MockOrg", "MockOrg", "MockOrg"],
        "Messaging_id": ["id1", "id2", "id3"],
        "Public_key": [b'publickey1', b'publickey2', b'publickey3']
    }
    master_account_df = pd.DataFrame(master_account_df)
    master_account_df.to_pickle("./data/mock_master_account_df.pkl")

if __name__ == '__main__':
    main()
    test_master_account = MasterAccount()
    test_master_account.load_account_from_org_name("MockOrg")
    test_master_account.save_account()
    test_master_account.load_account_from_org_name("MockOrg")

    print(test_master_account.org_name)
    print(test_master_account.id_key_dict)
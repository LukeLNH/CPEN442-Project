import pandas as pd
class MasterAccount:

    def __init__(self):
        self.org_name = ""
        self.id_key_dict = {}

    def load_account_from_org_name(self, org_name):
        df = pd.read_pickle("./data/master_account_df.pkl") # need to pickle to use bytes
        df = df[df['Org_name'] == org_name]
        
        self.org_name = org_name
        self.id_key_dict = dict(zip(df['Messaging_id'], df['Public_key']))

    def save_account(self):
        df = pd.read_pickle("./data/master_account_df.pkl")

        df = df[df['Org_name'] != self.org_name] # drop all current rows

        updated_account = pd.DataFrame({
            "Org_name": [self.org_name for _ in range(len(self.id_key_dict))],
            "Messaging_id": list(self.id_key_dict.keys()),
            "Public_key": list(self.id_key_dict.values())
        })

        df = pd.concat([df, updated_account], ignore_index=True)
        df.to_pickle("./data/master_account_df.pkl")


    def issue_private_key(self, new_account):
        # check that it's actually a new account
        # add new_account_id : public key to id_key_dict
        # add the private key to the new_accounts list of signatures
        pass

    def get_published_public_keys(self):
        return self.id_key_dict.value()

    def revoke_key(self): # Probably won't need for MVP, do it if we have time.
        pass

class MessagingAppProfile:

    def __init__(self):
        self.id = ""
        self.private_signatures = {}

    def load_profile_from_file(self, file_path):
        pass

    def save_profile_to_file(self, file_path):
        pass

    def add_signature_key(self, org_name, key):
        pass

    def sign_nonce(self, nonce):
        pass

    def revoke_key(self, org_name): # Probably won't need for MVP, do it if we have time.
        pass


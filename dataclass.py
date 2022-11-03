import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class MessagingAppProfile:

    def __init__(self):
        self.id = ""
        self.private_signatures = {}
        # Add passphrases to private key for extra security if have time. Not required for demo.
        # self.passphrases = {saved exported private key, passphrase}

    def load_profile_from_id(self, id: str):
        df = pd.read_pickle("./data/messagingProfile_account_df.pkl") # need to pickle to use bytes
        df = df[df['id'] == id]

        self.id = id
        self.private_signatures = dict(zip(df['Org_name'], df['Private_key']))

    def save_profile(self):
        df = pd.read_pickle("./data/messagingProfile_account_df.pkl")
        df = df[df['id'] != self.id]

        updated_profile = pd.DataFrame({
            "id": [self.id for _ in range(len(self.private_signatures))],
            "Org_name": list(self.private_signatures.keys()),
            "Private_key": list(self.private_signatures.values())
        })

        df = pd.concat([df, updated_profile], ignore_index=True)
        df.to_pickle("./data/messagingProfile_account_df.pkl")


    def add_signature_key(self, org_name: str, key: bytes):
        self.private_signatures[org_name] = key

    def sign_nonce(self, org_name: str, nonce: bytes):
        assert org_name in self.private_signatures, f"No key issued from org {org_name}"

        private_key = RSA.import_key(self.private_signatures[org_name])
        hashed_nonce = SHA256.new(nonce)
        signed_nonce = pkcs1_15.new(private_key).sign(hashed_nonce)

        return signed_nonce

    def revoke_key(self, org_name): # Probably won't need for MVP, do it if we have time.
        pass


class MasterAccount:

    def __init__(self):
        self.org_name = ""
        self.id_key_dict = {}

    def load_account_from_org_name(self, org_name: str):
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


    def issue_private_key(self, new_account: MessagingAppProfile):
        key = RSA.generate(2048)

        public_key = public_key = key.publickey().export_key()
        self.id_key_dict[new_account.id] = public_key
        
        private_key = key.export_key()
        new_account.add_signature_key(self.org_name, private_key)

    def get_published_public_keys(self):
        return self.id_key_dict.values()

    def revoke_key(self): # Probably won't need for MVP, do it if we have time.
        pass


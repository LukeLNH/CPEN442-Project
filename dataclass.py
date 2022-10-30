class MasterAccount:

    def __init__(self):
        self.org_name = ""
        self.id_key_dict = {}

    def load_account_from_file(self, file_path):
        pass

    def save_account_to_file(self, file_path):
        pass

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


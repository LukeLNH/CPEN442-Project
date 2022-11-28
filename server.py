from flask import Flask, request, jsonify
from dataclass import MasterAccount, MessagingAppProfile
from Crypto import Random
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import pandas as pd

app = Flask(__name__)

VERIFICATION_SUCCESS_MESSAGE = jsonify({
    'verification_success': True
})

VERIFICATION_FAILURE_MESSAGE = jsonify({
    'verification_success': False
})

@app.route("/")
def initialize_server():
    json_res = {
        "message": "YEET"
    }
    return json_res

@app.route("/list_all_organizations", methods=['POST'])
def list_all_organizations():
    df = pd.read_pickle("./data/master_account_df.pkl") # need to pickle to use bytes
    org_names = df['Org_name'].unique().tolist()
    return jsonify({
        'org_names': org_names
    })


@app.route("/verify_account", methods=['POST'])
def verify_account():
    # parse out the following:
    # - messaging id of sender
    # - company name the sender claims to be from

    sender_profile = MessagingAppProfile()
    sender_profile.load_profile_from_id("")

    master_account = MasterAccount()
    master_account.load_account_from_org_name("")

    # Generate new nonce
    nonce = Random.get_random_bytes(4)

    try:
        signed_nonce = sender_profile.sign_nonce(nonce)
        hashed_nonce = SHA256.new(nonce)
        published_public_keys = master_account.get_published_public_keys()

        for public_key in published_public_keys:
            try:
                pkcs1_15.new(public_key).verify(hashed_nonce, signed_nonce)
                return VERIFICATION_SUCCESS_MESSAGE
            except:
                # this wasn't the right public key, continue looking
                continue
    except:
        # did not find key associated with master account.
        pass

    # did not find public key associated with the sender_profile
    return VERIFICATION_FAILURE_MESSAGE

if __name__ == "__main__":
    app.run(host='0.0.0.0')
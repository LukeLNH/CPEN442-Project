from flask import Flask, request, jsonify
from dataclass import MasterAccount, MessagingAppProfile
from Crypto import Random
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pandas as pd
import json

app = Flask(__name__)

@app.route("/")
def initialize_server():
    json_res = {
        "message": "YEET"
    }
    return json_res

@app.route("/set_verification_org", methods=['POST'])
def set_verification_org():
    req = request.json
    with open('data/verification_org.json', 'w') as f:
        f.write(json.dumps(req))
    return "Success"
    

@app.route("/list_all_organizations", methods=['GET'])
def list_all_organizations():
    df = pd.read_pickle("./data/master_account_df.pkl") # need to pickle to use bytes
    org_names = df['Org_name'].unique().tolist()
    return jsonify({
        'org_names': org_names
    })


@app.route("/verify_account", methods=['POST'])
def verify_account():
    VERIFICATION_MESSAGE = {
        'id': "",
        'verification_success': True,
        'org_name': ""
    }

    req = request.json

    message_profile_id = req['id']

    sender_profile = MessagingAppProfile()
    master_account = MasterAccount()
    sender_profile.load_profile_from_id(message_profile_id)

    VERIFICATION_MESSAGE['id'] = message_profile_id

    data = {}
    with open('data/verification_org.json', 'r') as f:
        data = json.load(f)
        if not data['Logged_in']:
            VERIFICATION_MESSAGE['verification_success'] = False
            return jsonify(VERIFICATION_MESSAGE)
        master_account.load_account_from_org_name(data['Org_name'])
        VERIFICATION_MESSAGE['org_name'] = data['Org_name']

    # Generate new nonce
    nonce = Random.get_random_bytes(4)

    try:
        signed_nonce = sender_profile.sign_nonce(data['Org_name'], nonce)
        hashed_nonce = SHA256.new(nonce)
        published_public_keys = master_account.get_published_public_keys()

        for public_key in published_public_keys:
            try:
                print(public_key)
                pkcs1_15.new(RSA.import_key(public_key)).verify(hashed_nonce, signed_nonce)
                VERIFICATION_MESSAGE['verification_success'] = True
                return jsonify(VERIFICATION_MESSAGE)
            except:
                # this wasn't the right public key, continue looking
                continue
    except Exception as e:
        # did not find key associated with master account.
        pass

    # did not find public key associated with the sender_profile
    VERIFICATION_MESSAGE['verification_success'] = False
    return jsonify(VERIFICATION_MESSAGE)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
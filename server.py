from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def initialize_server():
    json_res = {
        "message": "YEET"
    }
    return json_res

@app.route("/list_all_organizations", methods=['POST'])
def list_all_organizations():
    pass

@app.route("/verify_account", methods=['POST'])
def verify_playlist():
    # parse out the following:
    # - messaging id of sender
    # - company name the sender claims to be from

    sender_profile = MessagingAppProfile()
    sender_profile.load_profile_from_file("")

    master_account = MasterAccount()
    master_account.load_account_from_file("")

    # Generate new nonce
    nonce = None

    signed_nonces = sender_profile.sign_nonce(nonce)

    published_public_keys = master_account.get_published_public_keys()

    for signed_nonce in signed_nonces:
        for public_key in published_public_keys:
            # verify signature
            verification_nonce = None
            
            if verification_nonce == nonce:
                return "Success message here"

    return "failure message here"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
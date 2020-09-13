import pyotp

key_mfa = pyotp.TOTP('5PSLMVIMMA65HIKQ')

def generate_url_mfa():
    topt = pyotp.TOTP(key_mfa).provisioning_uri(name='robertsilva.info@gmail.com', issuer_name='Desafio Python')
    print(topt)

def verify_mfa(mfa_code):
    topt = pyotp.TOTP('5PSLMVIMMA65HIKQ')
    verify = topt.verify(mfa_code)
    return verify

def generate_key():
    topt = pyotp.random_base32
    print(topt)
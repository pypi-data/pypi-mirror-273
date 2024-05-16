class JWTModel:
    def __init__(self, jwt_data):
        self.jwt_data = jwt_data

        self.fresh = jwt_data.get('fresh')
        self.iat = jwt_data.get('iat')
        self.jti = jwt_data.get('jti')
        self.type = jwt_data.get('type')
        self.sub = jwt_data.get('sub')
        self.nbf = jwt_data.get('nbf')
        self.csrf = jwt_data.get('csrf')
        self.exp = jwt_data.get('exp')
        self.full_name = jwt_data.get('full_name')
        self.email = jwt_data.get('email')
        self.mobile = jwt_data.get('mobile')
        self.country_iso_code = jwt_data.get('country_iso_code')

    def is_fresh(self):
        return self.fresh

    def is_access(self):
        return self.type == 'access'

    def is_refresh(self):
        return self.type == 'refresh'

    def is_admin(self):
        return self.jwt_data.get('is_admin')

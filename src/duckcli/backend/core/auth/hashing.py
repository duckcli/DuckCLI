from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(self):
        return pwd_cxt.hash(self)

    def verify(self, normal):
        return pwd_cxt.verify(normal, self)

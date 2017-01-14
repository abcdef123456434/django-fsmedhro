import ldap
from django.contrib.auth.models import User


class LdapUniHro(object):
    """
    """
    BASE_DN = "ou=people,o=uni-rostock,c=de"
    HOST = "ldaps://ldap.uni-rostock.de"

    def authenticate(self, username, password):

        user_dn = "uid=%s,%s" % (username, self.BASE_DN)
        conection = ldap.initialize(self.HOST)

        try:
            try:
                conection.bind_s(user_dn, password)
            except ldap.INVALID_CREDENTIALS:
                return None  # throw error?
            except ldap.LDAPError as e:
                return None
            else:
                ldapuser = conection.search_s("ou=people,o=uni-rostock,c=de", ldap.SCOPE_SUBTREE, "uid="+username)[0][1]
        finally:
            conection.unbind()

        if validate_ladp_user(ldapuser):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. password won't be used for authentification
                user = User(username=username, password='get from LDAP')
                user.is_staff = False
                user.is_superuser = False
                user.save()

            if user.is_active:
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def validate_ladp_user(ldapuseratts):
    filterlist = [
        ["employeeType", "s"],
        ["uniRFaculty", "03"],
        ["gidNumber", "97"]
    ]

    filterstatus = []
    for filter in filterlist:
        # if there is no matching in one filter-row, return False
        if not (any(item.decode() == filter[1] for item in ldapuseratts[filter[0]])):
            return False

    return True
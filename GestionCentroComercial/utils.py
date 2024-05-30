
def checkAdmin(request):
    return request.user.groups.filter(name="Administrador").exists()

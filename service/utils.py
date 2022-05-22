def setallattrs(instance, attrs):
    for key, value in attrs.items():
        setattr(instance, key, value)

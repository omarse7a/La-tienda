from .models.bag_models import Bag, ShippingInfo

def get_bag(request):
    session_key = request.session.session_key # getting the session key
    # Create a the session if it doesn't exist
    if not session_key: 
        request.session.create()
        session_key = request.session.session_key
    # Create or retrieve a bag
    bag, created = Bag.objects.get_or_create(session_key=session_key)
    return bag

def get_governorates():
    return [gov[0] for gov in ShippingInfo.GOVS]
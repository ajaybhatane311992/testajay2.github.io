from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys=cart.keys()
    # print(keys)
    for id in keys:
        # print(type(id), type(product.id))  #str int
        if int(id) == product.id:
            return True
    # print('car.py product=',product)
    # print('car.py cart=',cart)
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys=cart.keys()   #cart keys{'1':8,'2':}
    # print(keys)
    for id in keys:
        # print(type(id), type(product.id))
        if int(id) == product.id:
            return cart.get(id) #return value of id id=1 value=8

    # print('car.py product=',product)
    # print('car.py cart=',cart)
    return 0

@register.filter(name='price_total')
def price_total(product,cart):
    return product.Price * cart_quantity(product,cart)

@register.filter(name='total_cart_price')
def total_cart_price(products,cart):
    sum=0
    for p in products:
        sum +=  price_total(p,cart)
    return sum

@register.filter(name='check_gender')
def check_gender(name,gender):
    if gender == 2:
        return 'Mr.'+name
    else:
        return 'Miss'+name

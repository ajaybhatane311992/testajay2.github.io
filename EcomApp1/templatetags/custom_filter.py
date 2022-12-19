from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return '₹'+str(number)

@register.filter(name='multiply')
def multiply(number,number1):
    return number*number1

@register.filter(name='price_filter')
def price_filter(products):
    if products.Price<500:
        return products
    else:
        return products




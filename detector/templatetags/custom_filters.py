"""
Custom template filters for Coin Detector application
"""

from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiply the value by the argument
    Usage: {{ value|multiply:100 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='subtract')
def subtract(value, arg):
    """
    Subtract the argument from the value
    Usage: {{ value|subtract:10 }}
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='add_number')
def add_number(value, arg):
    """
    Add the argument to the value
    Usage: {{ value|add_number:10 }}
    """
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='percentage')
def percentage(value):
    """
    Convert decimal to percentage
    Usage: {{ 0.95|percentage }} -> 95
    """
    try:
        return float(value) * 100
    except (ValueError, TypeError):
        return 0


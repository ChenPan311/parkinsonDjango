from django import template
register = template.Library()


def translate_type(choice_type):
    if choice_type == 'MultipleChoice':
        return 'בחירה מרובה'
    elif choice_type == 'SingleChoice':
        return 'בחירה יחידה'
    else:
        return 'שאלה פתוחה'


register.filter(translate_type)

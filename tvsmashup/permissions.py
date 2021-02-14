from rest_framework import permissions
#from quiz.models import Question


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        print("Owner",obj.owner)
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

def is_authorised(user,obj):
    return user.is_superuser or user == obj.user


# def add_round_permission(func):
#     def wrapper(obj):
#         if obj.context['quiz'].user == obj.context['user']:
#             return func(obj)
#         else:
#             raise Exception("Permission to object denied")
#     return wrapper
#
#
# def add_question_permission(func):
#     def wrapper(obj):
#         if obj.context['round']:
#             #19-12-2020 Not sure why the validation was done as first if statement
#             #Changed to check against the quiz to avoid array bounds issues
#             #if obj.context['round'].roundquestion_set.all()[0].question.user == obj.context['user']:
#             if obj.context['round'].quiz.user == obj.context['user']:
#                 return func(obj)
#             else:
#                 raise Exception("Permission to object denied")
#         else:
#             #Question not part of round can just add
#             return func(obj)
#     return wrapper

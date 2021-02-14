from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models import Count
from accounts.models import Account
from tv.models import *

class GeneralResponse(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=100)

#Restrict publicly viewable user attributes
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','name')


class TVImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TVImage
        fields = ('id','picture',)

class TVShowSerializer(serializers.ModelSerializer):
    tv_image = TVImageSerializer()

    class Meta:
        model = TVShow
        fields = ('id','tv_image')



#
# class PictureAnswerSerializer(serializers.ModelSerializer):
#     #picture = serializers.SerializerMethodField()
#
#     class Meta:
#         model = PictureAnswer
#         fields = ('id','answer','is_correct','picture')
#
# class AnswerSerializer(serializers.ModelSerializer):
#     #picture = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Answer
#         fields = ('id','answer','is_correct')
#
#     def get_picture(self,obj):
#         if obj.picture:
#             return obj.picture
#         else:
#             return None
#
#     def to_representation(self, obj):
#         """
#         Because Answer is Polymorphic
#         """
#         if isinstance(obj, PictureAnswer):
#             return PictureAnswerSerializer(obj, context=self.context).to_representation(obj)
#         return super(AnswerSerializer, self).to_representation(obj)
#
#
# class QuestionSerializer(serializers.ModelSerializer):
#     answer_set = AnswerSerializer(many=True)
#
#     class Meta:
#         model = Question
#         fields = ('id','question','answer_set')
#
#     @add_question_permission
#     def save(self):
#         user = self.context['user']
#         round = self.context['round']
#         answers = self.validated_data.pop('answer_set',None)
#         question = Question.objects.create(
#             user = user,
#             question = self.validated_data['question']
#         )
#         if round:
#             RoundQuestion.objects.create(
#                 question= question,
#                 round = round
#             )
#         if answers:
#             for answer in answers:
#                 answer = Answer.objects.create(question=question, **answer)
#         return question
#
#
# class RoundSerializer(serializers.ModelSerializer):
#     question_set = QuestionSerializer(many=True)
#
#     class Meta:
#         model = Round
#         fields = ('id','name','timed','minutes','question_set')
#
#     @add_round_permission
#     def save(self):
#         user = self.context['user']
#         quiz = self.context['quiz']
#         questions = self.validated_data.pop('question_set', None)
#         print(self.validated_data)
#         round = Round.objects.create(
#             quiz = quiz,
#             name = self.validated_data['name'],
#             timed = self.validated_data['timed'],
#             minutes = self.validated_data['minutes']
#         )
#         if questions:
#             for question in questions:
#                 answers = question.pop('answer_set',None)
#                 question_obj = Question.objects.create(user=self.context['user'],**question)
#                 RoundQuestion.objects.create(round=round,question=question_obj)
#                 if answers:
#                     for answer in answers:
#                         answer = Answer.objects.create(question=question_obj, **answer)
#         return round
#
#
# class QuizSerializer(serializers.ModelSerializer):
#     round_set = RoundSerializer(many=True)
#
#     class Meta:
#         model = Quiz
#         fields = ('id','name','multiround','round_set')
#
#     def save(self):
#         user = self.context['user']
#         name = self.validated_data['name']
#         multiround = self.validated_data['multiround']
#         quiz = Quiz.objects.create(
#             user=user,
#             name=name,
#             multiround=multiround
#         )
#         rounds = self.validated_data.pop('round_set', None)
#         print('here are the rounds',rounds)
#         if rounds:
#             for round in rounds:
#                 questions = round.pop('question_set',None)
#                 print('here are the questions',questions)
#                 round = Round.objects.create(quiz=quiz, **round)
#                 if questions:
#                     for question in questions:
#                         answers = question.pop('answer_set',None)
#                         question_obj = Question.objects.create(user=self.context['user'],**question)
#                         RoundQuestion.objects.create(round=round,question=question_obj)
#                         if answers:
#                             for answer in answers:
#                                 answer = Answer.objects.create(question=question_obj, **answer)
#         return quiz
#
# #For serializing a quiz object
#
# class StoredRoundSerializer(serializers.ModelSerializer):
#     question_set = serializers.SerializerMethodField()
#     number_questions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Round
#         fields = ('id','name','timed','minutes','question_set','number_questions')
#
#
#     def get_question_set(self,obj):
#         questions = Question.objects.filter(roundquestion__round=obj)
#         return QuestionSerializer(questions,many=True).data
#
#     def get_number_questions(self,obj):
#         return obj.roundquestion_set.count()
#
#
# class StoredQuizSerializer(serializers.ModelSerializer):
#     round_set = StoredRoundSerializer(many=True)
#     user = serializers.SerializerMethodField()
#     number_rounds = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Quiz
#         fields = ('id','name','multiround','user','number_rounds','date_added','date_modified','round_set')
#
#     def get_rounds(self,obj):
#         Question.objects.filter(roundquestion__round)
#
#     def get_user(self,obj):
#         return PublicUserSerializer(obj.user).data
#
#     def get_number_rounds(self,obj):
#         return obj.round_set.count()
#
#
# #################################FOR SEARCHES##########################
#
# #Restrict publicly viewable user attributes
# class PublicUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('id','name')
#
# class RoundNameSerializer(serializers.ModelSerializer):
#     number_questions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Round
#         fields = ('id','name', 'number_questions')
#
#     def get_number_questions(self,obj):
#         return obj.roundquestion_set.count()
#
# class SearchQuizSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     round_set = RoundNameSerializer(many=True)
#     number_rounds = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Quiz
#         fields = ('id','name','multiround','user','round_set','number_rounds')
#
#     def get_user(self,obj):
#         return PublicUserSerializer(obj.user).data
#
#     def get_number_rounds(self,obj):
#         return obj.round_set.count()
#
# class SearchQuestionSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Question
#         fields = ('id','question','user')
#
#     def get_user(self,obj):
#         return PublicUserSerializer(obj.user).data
#
# ################################ MARKING #####################
#
# class MarkedAnswersSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     answer = serializers.CharField(allow_blank=True)
#     is_correct = serializers.BooleanField()
#
# class MarkedQuestionsSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     correct = serializers.BooleanField()
#     question = serializers.CharField()
#     answer_set = MarkedAnswersSerializer(many=True)
#     correct_answers = MarkedAnswersSerializer(many=True)
#
# class MarkedRoundSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     questions = MarkedQuestionsSerializer(many=True)
#
#
# ################################ HISTORY ######################
#
# class QuestionHistorySerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='question.id')
#     question = QuestionSerializer()
#
#     class Meta:
#         model = QuestionHistory
#         fields = ('id','question','answered_correctly','date_added')
#
#
# class RoundHistorySerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='round.id')
#     questions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = RoundHistory
#         fields = ('id','questions')
#
#     def get_questions(self,obj):
#         if self.context:
#             #Gets the latest distinct questions only
#             data = obj.questionhistory_set.all().order_by('question','-date_added').distinct('question')
#             for d in data:
#                 print(d.question.id)
#             return QuestionHistorySerializer(data,many=True,context=self.context).data
#         else:
#             return QuestionHistorySerializer(obj.questionhistory_set.all(),many=True,context=self.context).data
#
#
# class QuizHistorySerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='quiz.id')
#     rounds = serializers.SerializerMethodField()
#
#     class Meta:
#         model = QuizHistory
#         fields = ('id','rounds')
#
#     def get_rounds(self,obj):
#         return RoundHistorySerializer(obj.roundhistory_set.all(),many=True,context=self.context).data

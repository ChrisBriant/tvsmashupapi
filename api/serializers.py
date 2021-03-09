from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models import Count, Avg
from accounts.models import Account
from tv.models import *

class GeneralResponse(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=100)

class ShowsAndSmashups(object):
    def __init__(self, shows, smashups):
        self.shows = shows
        self.smashups = smashups


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
    user = serializers.SerializerMethodField()
    tv_image = serializers.SerializerMethodField()


    class Meta:
        model = TVShow
        fields = ('id','name','tv_image','user',)

    def get_tv_image(self,obj):
        try:
            image = TVImage.objects.get(show__id=obj.id)
            return TVImageSerializer(image).data
        except Exception as e:
            return None

    def get_user(self,obj):
        return PublicUserSerializer(obj.user).data

#May no longer be required
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','category')

class CategorySmashupSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.category')
    show_1_average_rating = serializers.SerializerMethodField()
    show_2_average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    already_rated = serializers.SerializerMethodField()
        ## TODO: factor in context if user is logged in find if category ratied

    class Meta:
        model = CategorySmashup
        fields = ('id','category','show_1_average_rating','show_2_average_rating','rating_count','already_rated')

    def get_show_1_average_rating(self, obj):
        return obj.categoryscore_set.aggregate(Avg('show_1_rating__rating'))

    def get_show_2_average_rating(self, obj):
        return obj.categoryscore_set.aggregate(Avg('show_2_rating__rating'))

    def get_rating_count(self,obj):
        return obj.categoryscore_set.count()

    def get_already_rated(self,obj):
        if not self.context['user_id']:
            print('No user')
            return False
        else:
            #Determine if the user ID is in the ratings
            print('Is user', self.context['user_id'])
            ratings = obj.categoryscore_set.all().values();
            ratings_filtered = [r['user_id'] for r in ratings if r['user_id']]
            if self.context['user_id'] in ratings_filtered:
                return True
            else:
                return False

class TVSmashupSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    show1 = serializers.SerializerMethodField()
    show2 = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = SmashUp
        fields = ('id','show1','show2','creator','categories')

    def get_show1(self,obj):
        return TVShowSerializer(obj.show_1).data

    def get_show2(self,obj):
        return TVShowSerializer(obj.show_2).data

    def get_creator(self,obj):
        return PublicUserSerializer(obj.creator).data

    def get_categories(self,obj):
        if not self.context:
            return CategorySmashupSerializer(obj.categorysmashup_set,many=True,context={'user_id':None}).data
        else:
            return CategorySmashupSerializer(obj.categorysmashup_set,many=True,context=self.context).data

class ShowRatingSerializer(serializers.ModelSerializer):
    show_id = serializers.ReadOnlyField(source='show.id')
    show_name = serializers.ReadOnlyField(source='show.name')

    class Meta:
        model = ShowRating
        fields = ('show_id', 'show_name', 'rating')

class RatingSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    show_1_rating = ShowRatingSerializer()
    show_2_rating = ShowRatingSerializer()

    class Meta:
        model = CategoryScore
        fields = ('id','show_1_rating','show_2_rating','category')

    def get_category(self,obj):
        return CategorySmashupSerializer(obj.categorysmashup,context=self.context).data


class ShowsAndSmashupsSerializer(serializers.Serializer):
    shows = serializers.ListField(child=TVShowSerializer())
    smashups = serializers.ListField(child=TVSmashupSerializer())

class ShowIndexSerializer(serializers.Serializer):
    showidx = serializers.CharField()
    count_shows = serializers.IntegerField()

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

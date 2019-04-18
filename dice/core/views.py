from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.views import View
from core import models

class IndexPage(View):
    def get(self, request):

        sum1 = 0
        sum2 = 0

        first_user_dices = []
        second_user_dices = []

        for user in range(1, 3):
            for dice_number in range(9):
                id = random.randint(1, 6)
                dice_photo = models.Dice.objects.get(id=id)

                if user == 1:
                    first_user_dices.append(dice_photo)
                    sum1 += id

                elif user == 2:
                    second_user_dices.append(dice_photo)
                    sum2 += id

        if sum1 > sum2:
            winner = 'user 1'
            result_winner = models.Result1(sum=str(sum1), user=winner)
            result_winner.save()
        else:
            winner = 'user 2'
            result_winner = models.Result1(sum=str(sum2), user=winner)
            result_winner.save()




        return render(request, 'index_page.html', {
            'dice_table_1': first_user_dices,
            'dice_table_2': second_user_dices,
            'winner': winner,

            'sum1': sum1,
            'sum2': sum2,

        })

class ResultForOne(View):
    def get(self, request):
        users = models.Result1.objects.all()

        list_of_winners = []
        for user in users:
            list_of_winners.append(user)

        return render(request, 'result_for_one.html', {
            'list_of_winners': list_of_winners
        })


class SecondPage(View):
    def get(self, request):

        #доки ці два рядки тут а не після запису іх в сесію то буде показуватсь попереднй результат
        prev_sum1 = request.session.get('sum1', 0)
        prev_sum2 = request.session.get('sum2', 0)

        sum1 = 0
        sum2 = 0

        first_user_dices = []
        second_user_dices = []



        for user in range(1, 3):
            for dice_number in range(9):
                id = random.randint(1, 6)
                dice_photo = models.Dice.objects.get(id=id)


                if user == 1:
                    first_user_dices.append(dice_photo)
                    sum1 += id

                elif user == 2:
                    second_user_dices.append(dice_photo)
                    sum2 += id



        request.session['sum1'] = sum1
        request.session['sum2'] = sum2

        list_of_winners = []
        winner_amount = []

        if sum1 > sum2:

            request.session['winner_sum'] = sum1
            winner_sum = request.session.get('winner_sum')
            winner = 'user1'

        else:
            request.session['winner_sum'] = sum2
            winner_sum = request.session.get('winner_sum')
            winner = 'user2'

        if not request.session.get('winner_amount'):
            request.session['winner_amount'] = [[winner_sum, winner]]

        else:
            request.session['winner_amount'].append([winner_sum, winner])

        return render(request, 'second_page.html', {
            'dice_table_1': first_user_dices,
            'dice_table_2': second_user_dices,
            'sum_one': sum1,
            'sum_two': sum2,
            'winner': winner,
            'winner_sum': winner_sum,

            'prev_sum1': prev_sum1,
            'prev_sum2': prev_sum2

        })

class ResultForTwo(View):
    def get(self, request):
        winner_amount = request.session.get('winner_amount')

        return render(request, 'result_for_two.html', {
            'winner_amount': winner_amount,


        })

class SignUp(View):
    def get(self, request):
        return render(request, 'sign_up.html')

    def post(self, request):

        login = request.POST['login']
        password = request.POST['password']

        if not models.User.objects.filter(login=login, password=password):
            new_user = models.User(login=login, password=password)
            new_user.save()

        else:
            login_exist = login
            print(login_exist)
            return HttpResponse(f' user {login_exist} already exist. try sign_in')


        request.session['user_id'] = new_user.id

        return redirect('/')

class SignIn(View):
    def get(self, request):
        return render(request, 'sign_in.html')

    def post(self, request):
        input_login = request.POST['login']
        input_password = request.POST['password']

        try:
            new_user = models.User.objects.get(login=input_login, password=input_password)

        except models.User.DoesNotExist as e:
            return HttpResponse(f'user {input_login} doesnt exist')

        request.session['user_id'] = new_user.id

        return redirect('/')

class Exit(View):
    def get(self, request):

        if request.session.get('user_id'):

            request.session.pop('user_id')

        return redirect('/')

import numpy as np
from collections import Counter
import strategies as stg
import copy
import tripwire
import pandas as pd
from openpyxl import Workbook

number_of_fights = 1
turn_min = 10
turn_max = 100
evolv_on = True
change_worest_by_best = True
tripwire_on = True
tripwire_error = 0.05
R, T, S, P = 3, 4, 1, 2
# 1) T > R > P > S
# 2) 2*R > T + S
if (T > R > P > S) is False:
    print "First condition of prisoner's dilemma is not met"
if (2*R > T + S) is False:
    print "Second condition of prisoner's dilemma is not met"
mac = {0: [R, R],
       1: [[T, S], [S, T]],
       2: [P, P]}


trap = tripwire.Tripwire(tripwire_error)

# list of tournament participants
good = stg.Good()
bad = stg.Bad()
titfortat = stg.TitForTat()
undecided = stg.Undecided()
grudger = stg.Grudger()
pavlov = stg.Pavlov()
adaptive = stg.Adaptive(mac)
bad_titfortat = stg.TitForTat(badly=True)
bad_undecided = stg.Undecided(badly=True)
bad_pavlov = stg.Pavlov(badly=True)
generous5_titfortat = stg.TitForTat(generous=5)
generous10_titfortat = stg.TitForTat(generous=10)
mistrustful = stg.Mistrustful()
titfortwotats = stg.TitForTat(tats=2)
titforthreetats = stg.TitForTat(tats=3)
generous02_titfortwotats = stg.TitForTat(generous=0.2, tats=2)
random = stg.Random()
random025 = stg.Random(defect_with=0.25)
generous033_titfortat = stg.TitForTat(generous=0.33)
undecidedtitfortat = stg.UndecidedTitForTat()
bandit = stg.Bandit()
softgrudger = stg.SoftGrudger()
detective = stg.Detective()
generous02pavlov = stg.Pavlov(generous=0.2)
simplythinker = stg.SimplyThinker()
hardlythinker = stg.HardlyThinker()
easygoingsimplythinker = stg.EasyGoingSimplyThinker()
easygoingsimplythinker2 = stg.EasyGoingTftSimplyThinker()
adaptive2 = stg.Adaptive(mac, len_adapt=2)
titfortattittat = stg.TitTatTitForTat()
twotitsfortat = stg.TwoTitsForTat()
delay3grudger = stg.Grudger(calm=3)
ceasefire = stg.LetsMakeCeaseFire()
ceasefire25055 = stg.LetsMakeCeaseFire(war=2, peace=5, intensity=0.55)
ceasefire52095 = stg.LetsMakeCeaseFire(war=5, peace=2, intensity=0.95)
titfortatwithoutlooping = stg.TitForTatWithoutLooping()
adaptivetitfortat = stg.AveragedTitForTat(mac)

list_of_tournament = [
                        ["Tit for tat", copy.deepcopy(titfortat), 0, 0],
                        ["Good", copy.deepcopy(good),0,0],
                        ["Bad", copy.deepcopy(bad),0,0],
                        ["Undecided", copy.deepcopy(undecided),0,0],
                        ["Grudger", copy.deepcopy(grudger),0,0],
                        ["Pavlov", copy.deepcopy(pavlov),0,0],
                        ["Adaptive", copy.deepcopy(adaptive),0,0],
                        ["Bad Tit for tat", copy.deepcopy(bad_titfortat),0,0],
                        ["Bad Undecided", copy.deepcopy(bad_undecided), 0,0],
                        ["Bad Pavlov", copy.deepcopy(bad_pavlov), 0,0],
                        ["Generous 5 Tit for tat", copy.deepcopy(generous5_titfortat), 0,0],
                        ["Generous 10 Tit for tat", copy.deepcopy(generous10_titfortat), 0,0],
                        ["Mistrustful", copy.deepcopy(mistrustful), 0, 0],
                        ["Tit for two tats", copy.deepcopy(titfortwotats),0,0],
                        ["Tit for three tats", copy.deepcopy(titforthreetats),0,0],
                        ["Generous 0.2 Tit for two tats", copy.deepcopy(generous02_titfortwotats),0,0],
                        ["Random", copy.deepcopy(random),0,0],
                        ["Random 0.25", copy.deepcopy(random025),0,0],
                        ["Generous 0.33 Tit for tat", copy.deepcopy(generous033_titfortat), 0, 0],
                        ["Undecided Tit for tat", copy.deepcopy(undecidedtitfortat), 0, 0],
                        ["Bandit", copy.deepcopy(bandit), 0, 0],
                        ["Soft grudger", copy.deepcopy(softgrudger), 0, 0],
                        ["Detective", copy.deepcopy(detective), 0, 0],
                        ["Generous 0.2 Pavlov", copy.deepcopy(generous02pavlov), 0, 0],
                        ["Simply Thinker", copy.deepcopy(simplythinker), 0, 0],
                        ["Hardly Thinker", copy.deepcopy(hardlythinker), 0, 0],
                        ["Easy Going Simply Thinker", copy.deepcopy(easygoingsimplythinker), 0, 0],
                        ["Easy Going Tft Simply Thinker", copy.deepcopy(easygoingsimplythinker2), 0, 0],
                        ["Adaptive 2", copy.deepcopy(adaptive2), 0, 0],
                        ["Two Tits For tat", copy.deepcopy(twotitsfortat), 0, 0],
                        ["Tit tat tit For Tat", copy.deepcopy(titfortattittat), 0, 0],
                        ["Delay 3 Grudger", copy.deepcopy(delay3grudger), 0, 0],
                        ["Let's make cease fire", copy.deepcopy(ceasefire), 0, 0],
                        ["Let's make cease fire - peaceful", copy.deepcopy(ceasefire25055), 0, 0],
                        ["Let's make cease fire - wardog", copy.deepcopy(ceasefire52095), 0, 0],
                        ["Averaged TFT", copy.deepcopy(adaptivetitfortat), 0, 0]
                        ,["Tft without looping", copy.deepcopy(titfortatwithoutlooping), 0, 0]
                      ]


uczestnik = []
game_count = []
score_sum = []
average = []

if evolv_on is False:
    evolv_len = 1
else:
    evolv_len = len(list_of_tournament)

# for i_p, pA in reversed(list(enumerate(list_of_tournament))):
#     for j_p, pB in reversed(list(enumerate(list_of_tournament))):
try:
    for i in range(1000):

        list_of_tournament = [
            ["Tit for tat", copy.deepcopy(titfortat), 0, 0],
            ["Good", copy.deepcopy(good), 0, 0],
            ["Bad", copy.deepcopy(bad), 0, 0],
            ["Undecided", copy.deepcopy(undecided), 0, 0],
            ["Grudger", copy.deepcopy(grudger), 0, 0],
            ["Pavlov", copy.deepcopy(pavlov), 0, 0],
            ["Adaptive", copy.deepcopy(adaptive), 0, 0],
            ["Bad Tit for tat", copy.deepcopy(bad_titfortat), 0, 0],
            ["Bad Undecided", copy.deepcopy(bad_undecided), 0, 0],
            ["Bad Pavlov", copy.deepcopy(bad_pavlov), 0, 0],
            ["Generous 5 Tit for tat", copy.deepcopy(generous5_titfortat), 0, 0],
            ["Generous 10 Tit for tat", copy.deepcopy(generous10_titfortat), 0, 0],
            ["Mistrustful", copy.deepcopy(mistrustful), 0, 0],
            ["Tit for two tats", copy.deepcopy(titfortwotats), 0, 0],
            ["Tit for three tats", copy.deepcopy(titforthreetats), 0, 0],
            ["Generous 0.2 Tit for two tats", copy.deepcopy(generous02_titfortwotats), 0, 0],
            ["Random", copy.deepcopy(random), 0, 0],
            ["Random 0.25", copy.deepcopy(random025), 0, 0],
            ["Generous 0.33 Tit for tat", copy.deepcopy(generous033_titfortat), 0, 0],
            ["Undecided Tit for tat", copy.deepcopy(undecidedtitfortat), 0, 0],
            ["Bandit", copy.deepcopy(bandit), 0, 0],
            ["Soft grudger", copy.deepcopy(softgrudger), 0, 0],
            ["Detective", copy.deepcopy(detective), 0, 0],
            ["Generous 0.2 Pavlov", copy.deepcopy(generous02pavlov), 0, 0],
            ["Simply Thinker", copy.deepcopy(simplythinker), 0, 0],
            ["Hardly Thinker", copy.deepcopy(hardlythinker), 0, 0],
            ["Easy Going Simply Thinker", copy.deepcopy(easygoingsimplythinker), 0, 0],
            ["Easy Going Tft Simply Thinker", copy.deepcopy(easygoingsimplythinker2), 0, 0],
            ["Adaptive 2", copy.deepcopy(adaptive2), 0, 0],
            ["Two Tits For tat", copy.deepcopy(twotitsfortat), 0, 0],
            ["Tit tat tit For Tat", copy.deepcopy(titfortattittat), 0, 0],
            ["Delay 3 Grudger", copy.deepcopy(delay3grudger), 0, 0],
            ["Let's make cease fire", copy.deepcopy(ceasefire), 0, 0],
            ["Let's make cease fire - peaceful", copy.deepcopy(ceasefire25055), 0, 0],
            ["Let's make cease fire - wardog", copy.deepcopy(ceasefire52095), 0, 0],
            ["Averaged TFT", copy.deepcopy(adaptivetitfortat), 0, 0]
            , ["Tft without looping", copy.deepcopy(titfortatwithoutlooping), 0, 0]
        ]


        # ## zmienna pozwalajaca usunac najgorsza strategie
        ###########
        # worest_stg = -1
        worest_stg = []
        # best_stg = -1
        best_stg = []
        ###########
        # ## petla ewelucyjna - usuwa po kazdej iteracji najgorsza strategie
        for evolv_turn in range(evolv_len):
            # ## warunek do usuwania najgorszej strategii. Jezeli =-1 to znaczy ze algorytmy byly rownie zle lub jest to pierwsza iteracja
            ###############
            # if worest_stg != -1:
            if worest_stg:
                worest_stg = np.random.choice(worest_stg)
                ###############
                if change_worest_by_best is True:
                    #################
                    # if best_stg != -1:
                    if best_stg:
                        best_stg = np.random.choice(best_stg)
                        #################
                        print "{0} is changed by {1}".format(list_of_tournament[worest_stg][0], list_of_tournament[best_stg][0])
                        list_of_tournament[worest_stg] = copy.deepcopy(list_of_tournament[best_stg])
                        list_of_tournament[worest_stg][0] = list_of_tournament[worest_stg][0]#+" {0}".format(np.round(np.random.rand(),decimals=2))
                else:
                    print "{0} drops out of the tournament".format(list_of_tournament[worest_stg][0])
                    list_of_tournament.remove(list_of_tournament[worest_stg])
            # ## toworzenie nowej listy turniejowej bazujacej na oryginalne, ale podatnej na zmiany ewolucyjne
            evolv_list_of_tournament = copy.deepcopy(list_of_tournament)
            # ## zwraca algorytm ktory pozostal jako ostatni
            if len(evolv_list_of_tournament) == 1:
                print "Evolutionarily stable strategy is {0}".format(evolv_list_of_tournament[0][0])
                break
            # ## zmienne do prowadzenia statystyk !!! cos nie tak z nimi
            con_tour = []
            tournament_result = []
            # ## podwojna petla konfrontujaca ze soba wszystkie strategie
            for i_p, pA in enumerate(evolv_list_of_tournament):
                for j_p, pB in enumerate(evolv_list_of_tournament):
                    # ## strategia nie walczy sama ze soba, bo podwyszyla by sobie statystyki
                    if i_p >= j_p:
                        continue
                    # ## zmienna do prowadzenia wyniku

                    win = []
                    # ## petla iteracyjna - ile razy dany pojedynek ma sie odbyc
                    for strg in range(number_of_fights):
                        # ## stos ruchow graczy
                        stock_d_A = []
                        stock_d_B = []
                        # ## zmienna wyniku: score[0] = Wynik A, score[1] = Wynik B
                        score = np.array([0, 0])
                        # ## losowanie liczby tur dla kazdej iteracji
                        round_length = np.random.randint(turn_min, turn_max)
                        # ## iteracyjny dylemat wieznia
                        for turn in range(round_length):
                            # ## zmienne pokazujace ruch gracza odwolujace sie do metody .decision(loyd,lood)
                            dA = pA[1].decision(stock_d_A, stock_d_B)
                            dB = pB[1].decision(stock_d_B, stock_d_A)
                            # ## Potykacz
                            if tripwire_on is True:
                                dA = trap.stumble(dA)
                                dB = trap.stumble(dB)
                            # ## zapisywanie historii ruchow graczy
                            stock_d_A.append(dA)
                            stock_d_B.append(dB)
                            # ## sprawdzanie rezultatow podjetych decyzji
                            conclusion = dA + dB
                            # ## Pokusa(1) i Frajer(0)
                            if conclusion == 1:
                                # A-T B-S
                                if dA > dB:
                                    # ## odpowiednia modyfikacja wyniku
                                    score += mac[conclusion][0]
                                    # ## prowadzenie sumy punktow ktore zdobyla dana strategia
                                    pA[2] += mac[conclusion][0][0]
                                    pB[2] += mac[conclusion][0][1]
                                # A-S B-T
                                else:
                                    score += mac[conclusion][1]
                                    pB[2] += mac[conclusion][1][1]
                                    pA[2] += mac[conclusion][1][0]
                            # ## Nagroda(0) lub Kara(2)
                            elif conclusion == 0 or conclusion == 2:
                                score += mac[conclusion]
                                pA[2] += mac[conclusion][0]
                                pB[2] += mac[conclusion][1]
                            # ## warunek sprawdzajacy poprawnosc conclusion
                            else:
                                print("incorrect index of decisions!!! \n"
                                      "score A:{0} B:{1}".format(score[0], score[1]))
                                break
                                # print (wynik)
                            # ## prowadzenie liczby wszystkich tur ktore dana strategia rozegrala
                            # print score
                            pA[3] += 1
                            pB[3] += 1
                        # print pA[2]
                        # print pB[2]
                        # print stock_d_A
                        # print stock_d_B
                        # ## dodawanie kolejnych wynikow danej iteracji
                        if score[0] > score[1]:
                            win.append('A')
                        if score[0] == score[1]:
                            win.append('D')
                        if score[0] < score[1]:
                            win.append('B')
                    # print (win)
                    # ## wynik wszystkich iteracji
                    con = Counter(win)
                    # print (con)
                    # ## dodawanie kooejnych wygranych danej strategii
                    if con['A']>con['B']:
                        # print 'The winner is {0} with {1} wins'.format(pA[0], con['A'])
                        tournament_result.append(pA[0])
                    elif con['A']<con['B']:
                        # print 'The winner is {0} with {1} wins'.format(pB[0], con['B'])
                        tournament_result.append(pB[0])
                    else:
                        # print 'Draw for {0} and {1}: {2}'.format(pA[0], pB[0], con['D'])
                        # ## Dodawanie remisow jako obustronnych zwyciestw
                        # tournament_result.append(pB[0])
                        # tournament_result.append(pA[0])
                        pass
                        # list_of_tournament.pop(i_p)
            # ## wynik wszystkich strategii
            con_tour = Counter(tournament_result)
            print con_tour

            # ## pobranie wartosci jaka srednia moze maksymalnie przyjac z macierzy wyplat
            worest_avg = T
            best_avg = S
            general_avg = []
            # ## lista najgorszych strategii jezeli jest ich kilka
            # worest_stg_list = []
            # ## algorytm wylaniajacy strategie z najgorszym srednim wynikiem.
            # ## W przypadku paru takich samych srednich nie wylania takowego
            for i, strg in enumerate(evolv_list_of_tournament):
                # ## Wylicz srednia
                avg_stg = float(strg[2]) / float(strg[3])
                # ## Pokaz ostateczny wynik
                # if strg[0] == "Simply Thinker" or strg[0] == "Hardly Thinker":
                print strg[2], strg[3], np.round(avg_stg, 6), strg[0]
                general_avg.append(np.round(avg_stg, 6))
                if avg_stg < worest_avg:
                    worest_avg = avg_stg
                    ################
                    # worest_stg = i
                    worest_stg = []
                    worest_stg.append(i)
                    ################
                elif avg_stg == worest_avg:
                    ################
                    # worest_stg = -1
                    worest_stg.append(i)
                    ################
                if avg_stg > best_avg:
                    best_avg = avg_stg
                    ################
                    # best_stg = i
                    best_stg = []
                    best_stg.append(i)
                    ################
                elif avg_stg == best_avg:
                    ################
                    # best_stg = -1
                    best_stg.append(i)
                    ################
            ###
            #Tworzenie Raportu
            for i in evolv_list_of_tournament:
                a, b = float(i[2]), float(i[3])
                uczestnik.append(i[0])
                game_count.append(b)
                score_sum.append(a)
                average.append(a / b)
            ###
            print "Average of all strategies: {0}".format(np.average(general_avg))
            print "The best algorithm is {0} with average score {1}".format(evolv_list_of_tournament[np.random.choice(best_stg)][0],best_avg)
            if len(best_stg) == len(evolv_list_of_tournament):
                break
    ###
    #Tworzenie raportu
    wyniki = {
        "Uczestnik": uczestnik,
        "Liczba gier": game_count,
        "Suma punktow": score_sum,
        "Srednia": average
    }
    df = pd.DataFrame(wyniki, columns=["Uczestnik", "Suma punktow", "Liczba gier", "Srednia"])
    print(df)
    # df.to_excel("C:\Users\FG\Desktop\seminarium\Raporty\\raport_1000_def_undecidedTft04_1.xlsx")
    df.to_csv("C:\Users\FG\Desktop\seminarium\Raporty\\raport_1000_tripwire_Evolv_1.csv")
    # df.to_sql("C:\Users\FG\Desktop\seminarium\Raporty\\raport_1000_def_Evolv_1.sql")
    ###
# ## jesli cos sie zepsuje pokaz biezacy ostateczny wynik
except IndexError:
    print IndexError
# except IOError:
#     print "some error appear"
#     for strg in list_of_tournament:
#         print strg[2], strg[3], float(strg[2]) / float(strg[3]), strg[0]

from django.shortcuts import render
from crypto.services.import_currency import import_candles
from datetime import datetime as dt

# def page_list(request):
#     pages = Page.objects.all()

#     context = {"pages": pages}

#     return render(request, "page/list.html", context)


# def page_detail(request, page_id):
#     page = get_object_or_404(Page, id=page_id)

#     context = {"page": page}

#     return render(request, "page/detail.html", context)


def page_home(request):
    date_start = dt(2017, 1, 1, 0, 0, 0, 0)

    import_candles(symbol="btc/usdt", since=date_start)
    # page = get_object_or_404(Page, slug="home")
    # data = {
    #     "subtitle": "Que vous soyez chez vous, en terrasse ou au travail, nous récupérons votre appareil sur le lieu de votre choix, et nous vous le livrons réparé... dans la même journée.",
    #     "bloc_1_title": "Comment ça marche ?",
    #     "bloc_1_card_1_title": "Récupérer",
    #     "bloc_1_card_1_description": "En un rien de temps où vous voulez*, grâce à notre partenaire STUART.",
    #     "bloc_1_card_2_title": "Réparer",
    #     "bloc_1_card_2_description": "Par les meilleurs experts réparateurs de Paris ! Aucune panne ne leur fait peur 💪.",
    #     "bloc_1_card_3_title": "Livrer",
    #     "bloc_1_card_3_description": "À l'endroit qui vous convient*, Retrouvez votre précieux mobile, fonctionnel 🥰 !",
    #     "bloc_1_annotation": "*Dans Paris et la petite couronne, d'autres villes arrivent bientôt !",
    #     "bloc_2_title": "Nos engagements",
    #     "bloc_2_card_1_title": "Garantie 12 mois",
    #     "bloc_2_card_1_description": "Peu de chance que cela vous serve, mais rassurez-vous, toutes nos réparations sont garanties pendant 1 an. Pièces et main d'œuvres comprises.",
    #     "bloc_2_card_2_title": "Paiement sécurisé",
    #     "bloc_2_card_2_description": "Nous prenons la sécurité des transactions très au sérieux. C'est pour cela que nous avons choisi de travailler avec Stripe, certifiée selon les normes les plus élevées du secteur.",
    #     "bloc_2_card_3_title": "Suivi en temps réel",
    #     "bloc_2_card_3_description": "Suivez en temps réel l’acheminement et la réparation de votre smartphone sur votre . Chaque étape de la réparation.",
    #     "bloc_2_card_4_title": "A l'écoute",
    #     "bloc_2_card_4_description": "Nous restons à l'écoute pour toutes les questions avant, pendant et après votre demande de réparation.",
    #     "bloc_3_title": "FAQ",
    #     "bloc_3_content": """1. COMBIEN DE TEMPS DURE LA PRESTATION ?
    #             La réparation dure en moyenne de 1h30 à 3h en fonction de la panne. En cas de soucis majeurs, nous vous avertirons par mail/téléphone.
    #             2. A QUOI M’ENGAGE LE DEVIS ?
    #             La tarification étant immédiate, absolument rien, vous avez la possibilité de faire autant de recherche de prix que vous le souhaitez !
    #             3. QUE FAIRE SI MON SMARTPHONE N’EST PAS RÉPARABLE ?
    #             Si la panne n’est pas réparable et correspond à votre déclaration initiale, nous vous renvoyons votre téléphone.
    #             Nous vous proposerons également une sélection de smartphones reconditionnés équivalent via notre partenaire.
    #             4. QUE SE PASSE-T-IL SI D’AUTRES PANNES SONT CONSTATÉES ?
    #             Nous vous envoyons un nouveau devis mis à jour. Vous pouvez toutefois refuser le devis, auquel cas, seule la prestation initiale sera effectuée.
    #             Vous avez également la possibilité d’annuler totalement la prestation. Les frais de gestion resteront dans ce cas à votre charge (30€ TTC).
    #             5. QUES SE PASSE T’IL SI JE NE PEUX PAS RÉCUPÉRER MON TÉLÉPHONE LE
    #             JOUR MÊME ?
    #             Nous vous proposerons un autre créneau (du lundi au samedi de 11h à 17h).
    #             6. PUIS-JE MODIFIER L’ADRESSE DE RETOUR DU SMARTPHONE ?
    #             Oui bien sûr! Le retour peut se faire n’importe où dans Paris et la petite couronne.""",
    # }

    context = {
        #     "page": page,
        #     "data": data,
    }

    return render(request, "page/home.html", context)

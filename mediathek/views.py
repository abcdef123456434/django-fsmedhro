from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from mediathek.models import Kunde, Bestellung, Sammelbestellung, Ware, Angebot
from fsmedhrocore.models import BasicHistory
from django.contrib import messages


def check_mediathek_mitarbeiter(user):
    return user.groups.filter(name='mediathek').exists()


def check_created_by(user, auftrag):
    if isinstance(auftrag, BasicHistory):
        return auftrag.created_by == user
    else:
        # no BosicHistory-object passed
        return None


@login_required
def index(request):

    user = request.user

    # Kundendaten abfragen. Wenn noch kein Kundenprofil, dann neu anlegen
    try:
        kunde = user.kunde
    except ObjectDoesNotExist:
        kunde = Kunde(user=user, modified_by=user)
        kunde.save()

    context = {'kunde': kunde, }

    return render(request, 'mediathek/index.html', context)


@login_required
def sammelbest_auftrag_detail(request, auftrag_id):
    """
    Eine Bestellung aufgeben/ansehen/bearbeiten
    :param request:
    :param auftrag_id:
    :return:
    """
    bestellung = get_object_or_404(Bestellung, pk=auftrag_id)

    if check_created_by(user=request.user, auftrag=bestellung):
        # nur der Eigentümer darf Bestellung  einsehen
        messages.add_message(request, messages.INFO, 'Diese Bestellung ist nicht von dir.')
        return redirect('mediathek:index')

    context = {'bestellung': bestellung}

    return render(request, 'mediathek/sammelbest_auftrag_detail.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def verwaltung(request):
    """
    Verwaltung-Übersicht
    :param request:
    :return:
    """

    aktuelle_sammelbest = Sammelbestellung.objects.filter(active=True)

    context = {'aktuelle_sammelbest': aktuelle_sammelbest}

    return render(request, 'mediathek/verwaltung.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def sammelbest_list(request):
    return render(request, 'mediathek/sammelbest_list.html')


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def sammelbest_detail(request, sammelbest_id):
    """
    Sammelbestellung bearbeiten (Angebote hinzufügen, Frist setzen etc.)
    :param request:
    :param sammelbest_id:
    :return:
    """

    sammelbest = get_object_or_404(Sammelbestellung, pk=sammelbest_id)

    context = {'sammelbest': sammelbest}

    return render(request, 'mediathek/sammelbest_detail.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def sammelbest_auftraege_list(request, sammelbest_id):
    """
    Alle Bestellungen zu einer Sammelbestellung
    :param request:
    :param sammelbest_id:
    :return:
    """

    sammelbest = get_object_or_404(Sammelbestellung, pk=sammelbest_id)

    context = {'sammelbest': sammelbest}

    return render(request, 'mediathek/sammelbest_auftraege_list.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def sammelbest_auftrag_edit(request, auftrag_id):
    """
    Eine Bestellung aufgeben/ansehen/bearbeiten
    :param request:
    :param auftrag_id:
    :return:
    """
    bestellung = get_object_or_404(Bestellung, pk=auftrag_id)
    
    context = {'bestellung': bestellung}
       
    return render(request, 'mediathek/sammelbest_auftrag_edit.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def waren_list(request):
    """
    Alle Bestellungen zu einer Sammelbestellung
    :param request:
    :return:
    """
    return render(request, 'mediathek/waren_list.html')


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def ware_detail(request, ware_id):
    """
    Sammelbestellung bearbeiten (Angebote hinzufügen, Frist setzen etc.)
    :param request:
    :param ware_id:
    :return:
    """

    ware = get_object_or_404(Ware, pk=ware_id)

    context = {'ware': ware}

    return render(request, 'mediathek/ware_detail.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def angebot_detail(request, angebot_id):
    """
    Sammelbestellung bearbeiten (Angebote hinzufügen, Frist setzen etc.)
    :param request:
    :param angebot_id:
    :return:
    """

    angebot = get_object_or_404(Angebot, pk=angebot_id)

    context = {'angebot': angebot}

    return render(request, 'mediathek/angebot_detail.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:index', redirect_field_name=None)
def ausleihe(request):
    return render(request, 'mediathek/ausleihe.html')
